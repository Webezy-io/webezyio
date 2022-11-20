# Copyright (c) 2022 Webezy.io.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
import inquirer
from webezyio.architect import WebezyArchitect
from webezyio.cli.theme import WebezyTheme
from webezyio.commons import file_system, helpers,resources,errors
from inquirer import errors as inquirerErrors
from webezyio.commons.pretty import print_error, print_info,bcolors, print_note, print_success,print_warning
from webezyio.commons.protos.webezy_pb2 import Descriptor, Language, Project, ServiceDescriptor, WebezyClient, WebezyDeploymentType, WebezyServer, WzResourceWrapper,google_dot_protobuf_dot_struct__pb2
log = logging.getLogger('webezyio.cli.main')

def extend_resource(resource,extension,wz_json:helpers.WZJson):
    """
    Extend any Webezy.io resource
    """
    ARCHITECT = WebezyArchitect(
        path=file_system.join_path(wz_json.path,'webezy.json'),domain=wz_json.domain,project_name=wz_json.project.get('name'))

    print_note(resource.get('name'),True,'Extending resource \'{}\''.format(resource.get('type')))
    
    if resource.get('type') == 'packages':
        extend_package(resource,extension,wz_json,ARCHITECT)    

    

def extend_package(resource,extension,wz_json:helpers.WZJson,ARCHITECT:WebezyArchitect):
    """
    Extending a Webezy.io package resource
    """
    
    pkg_dependencies = resource.get('dependencies')
    pkg_messages = resource.get('messages')
    
    # Iterating available packages and extendable messages
    avail_extensions = []
    for pkg in pkg_dependencies:
        if 'google.protobuf.' not in pkg:
            temp_pkg = wz_json.get_package(pkg.split('.')[1])
            avail_extensions.append(*get_extensions(temp_pkg.get('messages'),'FileOptions'))
    avail_extensions.append(*get_extensions(pkg_messages,'FileOptions'))

    # Check for valid extension for package resource
    list_avail_ext = []
    for avail_ext in avail_extensions:
        avail_ext_display_name = avail_ext.get('name') if avail_ext.get('description') is None or avail_ext.get('description') == 'None' else '{} - {}'.format(avail_ext.get('name'),avail_ext.get('description'))
        list_avail_ext.append((avail_ext_display_name,avail_ext.get('fullName')))
   
    # If extension argument value has not passed into function
    if extension is None:
        results = inquirer.prompt([inquirer.List('extension','Chose extension to use',choices=list_avail_ext)],theme=WebezyTheme())
        if results is not None:
            results = next((ext for ext in avail_extensions if ext.get('fullName') == results['extension']))
    
    # Handle argument passed
    else:
        results = next((ext for ext in avail_extensions if ext.get('fullName') == extension),None)
    
    if results is not None:
        list_of_ext_fields = []
        
        for ext_field in results.get('fields'):
            list_of_ext_fields.append((ext_field.get('name'),ext_field.get('fullName')))
        
        field_extension_result = inquirer.prompt([inquirer.List('extension_field','Chose which field you want to add / edit?',list_of_ext_fields)],theme=WebezyTheme())
        
        if field_extension_result is not None:
            temp_field_ext = next((f for f in results.get('fields') if f.get('fullName') == field_extension_result['extension_field']),None)
            if temp_field_ext is not None:
                if temp_field_ext.get('fieldType') == 'TYPE_MESSAGE':
                    value = handle_ext_field_message(temp_field_ext.get('messageType'),wz_json)
                else:
                    raise errors.WebezyValidationError('Handle Extension Editing Failed','Error occured during handling of extensions {}'.format(temp_field_ext.get('fullName')))

                if resource.get('extensions') is None:
                    resource['extensions'] = {}
                resource['extensions'][temp_field_ext.get('fullName')] = value
                print_note(resource,True)
                ARCHITECT.EditPackage(resource.get('name'),resource.get('dependencies'),resource.get('messages'),resource.get('enums'),resource.get('description'),resource.get('extensions'))
                ARCHITECT.Save()

def get_extensions(messages, type):
    """Helper function for getting extensions from messages array"""
    return [m for m in messages if m.get('extensionType') == type]

def handle_ext_field_message(message_full_name,wz_json:helpers.WZJson):
    value = None
    temp_msg = wz_json.get_message(message_full_name)
    avail_extension_message_fields = []

    for f in temp_msg.get('fields'):
        avail_extension_message_fields.append((f.get('name'),f.get('fullName')))
    
    extended_message_field = inquirer.prompt([inquirer.List('extension_message_field','Enter an extension value for',avail_extension_message_fields)],theme=WebezyTheme())
    if extended_message_field is not None:
        temp_extended_field = next((f for f in temp_msg.get('fields') if f.get('fullName') == extended_message_field['extension_message_field']))
        
        if 'LABEL_OPTIONAL' == temp_extended_field.get('label'):
            # Recursive for nested messages
            if temp_extended_field.get('fieldType') == 'TYPE_MESSAGE':
                temp_extended_field = handle_ext_field_message(temp_extended_field.get('messageType'),wz_json)
            
            # Handle enums
            elif temp_extended_field.get('fieldType') == 'TYPE_ENUM':
                enum_message = wz_json.get_enum(temp_extended_field.get('enumType'))
                enum_values = []
                for v in enum_message.get('values'):
                    enum_values.append(v.get('name'))
                value = inquirer.prompt([inquirer.List('enum_value','Chose enum value for {}'.format(temp_extended_field.get('fullName')),enum_values)],theme=WebezyTheme())  
                if value is not None:
                    value = value['enum_value']
                
            else:
                raise errors.WebezyValidationError('Extension field type not valid','Unsupported {} field type for extensions'.format(temp_extended_field.get('fieldType')))
            
            temp_struct = google_dot_protobuf_dot_struct__pb2.Struct()
            temp_struct.update({temp_extended_field.get('name'):value})
            return google_dot_protobuf_dot_struct__pb2.Value(struct_value=temp_struct)
                
        elif 'LABEL_REPEATED' == temp_extended_field.get('label'):
            pass
        else:
            raise errors.WebezyValidationError('Unsupported label type','Unsupporting label {} for extensions'.format(temp_extended_field.get('label'))) 
        
