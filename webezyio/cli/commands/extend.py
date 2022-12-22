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
from typing import Literal
import inquirer
from webezyio.architect import WebezyArchitect
from webezyio.cli.theme import WebezyTheme
from webezyio.commons import file_system, helpers,resources,errors
from inquirer import errors as inquirerErrors
from webezyio.commons.pretty import print_error, print_info,bcolors, print_note, print_success,print_warning
from webezyio.commons.protos import google_dot_protobuf_dot_struct__pb2
log = logging.getLogger('webezyio.cli.main')

def extend_resource(resource,extension,wz_json:helpers.WZJson):
    """
    Extend any Webezy.io resource
    """
    ARCHITECT = WebezyArchitect(
        path=file_system.join_path(wz_json.path,'webezy.json'),domain=wz_json.domain,project_name=wz_json.project.get('name'))

    print_note(resource.get('fullName'),True,'Extending resource \'{}\' - \'{}\''.format(resource.get('type'),resource.get('kind')))
    
    if resource.get('type') == 'packages':
        results = handle_extension_by_type(resource,extension,wz_json,'package')
        extend_package(results,resource,extension,wz_json,ARCHITECT)    
    elif resource.get('type') == 'descriptors':
        if resource.get('kind') == resources.ResourceKinds.field.value:
            results = handle_extension_by_type(resource,extension,wz_json,'field')
            extend_field(results,resource,extension,wz_json,ARCHITECT)    
        elif resource.get('kind') == resources.ResourceKinds.message.value:
            results = handle_extension_by_type(resource,extension,wz_json,'message')
            extend_message(results,resource,extension,wz_json,ARCHITECT)    

def extend_message(results,resource,extension,wz_json:helpers.WZJson,ARCHITECT:WebezyArchitect):
    """
    Extending message
    
    Parameters:
    -----------

        results (dict): 
            The dictionary representation for extension message descriptor
        resource (dict): 
            The dictionary representation for the extended message descriptor
        extension 
            TODO
        wz_json: 
            Webezy json file object
        ARCHITECT: 
            The architect object

    """
    if results is not None:
        list_of_ext_fields = []
        for ext_field in results.get('fields'):
            list_of_ext_fields.append((ext_field.get('name'),ext_field.get('fullName')))
        
        field_extension_result = inquirer.prompt([inquirer.List('extension_field','Chose which field you want to add / edit?',list_of_ext_fields)],theme=WebezyTheme())
        if resource.get('extensions') is None:
            resource['extensions'] = {}
        if field_extension_result is not None:
            temp_field_ext = next((f for f in results.get('fields') if f.get('fullName') == field_extension_result['extension_field']),None)
            if temp_field_ext.get('fieldType') == 'TYPE_MESSAGE':
                value = handle_ext_field_message(temp_field_ext.get('messageType'),wz_json,resource['extensions'][temp_field_ext.get('fullName')] if resource['extensions'].get(temp_field_ext.get('fullName')) is not None else None)
            else:
                value = handle_ext_field(temp_field_ext,wz_json,resource['extensions'][temp_field_ext.get('fullName')] if resource['extensions'].get(temp_field_ext.get('fullName')) is not None else None)
        temp_pkg_desc = wz_json.get_package(resource.get('fullName').split(".")[1],False)
        resource['extensions'][temp_field_ext.get('fullName')] = value

        ARCHITECT.EditMessage(temp_pkg_desc,resource.get('name'),resource.get('fields'),resource.get('description'),resource.get('extensionType'),extensions=resource.get('extensions'))
        ARCHITECT.Save()

def extend_field(results,resource,extension,wz_json:helpers.WZJson,ARCHITECT:WebezyArchitect):
    if results is not None:
        list_of_ext_fields = []
        
        for ext_field in results.get('fields'):
            list_of_ext_fields.append((ext_field.get('name'),ext_field.get('fullName')))
        
        field_extension_result = inquirer.prompt([inquirer.List('extension_field','Chose which field you want to add / edit?',list_of_ext_fields)],theme=WebezyTheme())
        if resource.get('extensions') is None:
                resource['extensions'] = {}
        if field_extension_result is not None:
            temp_field_ext = next((f for f in results.get('fields') if f.get('fullName') == field_extension_result['extension_field']),None)
            if temp_field_ext.get('fieldType') == 'TYPE_MESSAGE':
                value = handle_ext_field_message(temp_field_ext.get('messageType'),wz_json,resource['extensions'][temp_field_ext.get('fullName')] if resource['extensions'].get(temp_field_ext.get('fullName')) is not None else None)
            else:
                value = handle_ext_field(temp_field_ext,wz_json,resource['extensions'][temp_field_ext.get('fullName')] if resource['extensions'].get(temp_field_ext.get('fullName')) is not None else None)

        temp_msg = wz_json.get_message('.'.join(resource.get('fullName').split('.')[:-1]))
        temp_pkg_desc = wz_json.get_package(resource.get('fullName').split(".")[1],False)
        resource['extensions'][temp_field_ext.get('fullName')] = value

        ARCHITECT.EditMessage(temp_pkg_desc,temp_msg.get('name'),temp_msg.get('fields'),temp_msg.get('description'),temp_msg.get('extensionType'),extensions=temp_msg.get('extensions'))
        ARCHITECT.Save()

def extend_package(results,resource,extension,wz_json:helpers.WZJson,ARCHITECT:WebezyArchitect):
    """
    Extending a Webezy.io package resource
    """
    if results is not None:
        list_of_ext_fields = []
        
        for ext_field in results.get('fields'):
            list_of_ext_fields.append((ext_field.get('name'),ext_field.get('fullName')))
        
        field_extension_result = inquirer.prompt([inquirer.List('extension_field','Chose which field you want to add / edit?',list_of_ext_fields)],theme=WebezyTheme())
        
        if field_extension_result is not None:
            temp_field_ext = next((f for f in results.get('fields') if f.get('fullName') == field_extension_result['extension_field']),None)
            if temp_field_ext is not None:
                if resource.get('extensions') is None:
                    resource['extensions'] = {}

                if temp_field_ext.get('fieldType') == 'TYPE_MESSAGE':
                    value = handle_ext_field_message(temp_field_ext.get('messageType'),wz_json,resource['extensions'][temp_field_ext.get('fullName')] if resource['extensions'].get(temp_field_ext.get('fullName')) is not None else None)
                else:
                    value = handle_ext_field(temp_field_ext,wz_json,resource['extensions'][temp_field_ext.get('fullName')] if resource['extensions'].get(temp_field_ext.get('fullName')) is not None else None)
                    # raise errors.WebezyValidationError('Handle Extension Editing Failed','Error occured during handling of extensions {}'.format(temp_field_ext.get('fullName')))
                resource['extensions'][temp_field_ext.get('fullName')] = value

                ARCHITECT.EditPackage(resource.get('name'),resource.get('dependencies'),resource.get('messages'),resource.get('enums'),resource.get('description'),resource.get('extensions'))
                ARCHITECT.Save()

def _get_extensions(messages, type):
    """Helper function for getting extensions from messages array"""
    return [m for m in messages if m.get('extensionType') == type]

def handle_extension_by_type(resource,extension,wz_json:helpers.WZJson,type:Literal['package','service','message','field','method']):
    """Package extensions"""
    ext_type = None

    if type == 'package':
        pkg_dependencies = resource.get('dependencies')
        pkg_messages = resource.get('messages')
        ext_type = 'FileOptions'

    elif type == 'field':
        temp_pkg = wz_json.get_package(resource.get('fullName').split('.')[1])
        pkg_dependencies = temp_pkg.get('dependencies')
        pkg_messages = temp_pkg.get('messages') 
        ext_type = 'FieldOptions'
    
    elif type == 'message':
        temp_pkg = wz_json.get_package(resource.get('fullName').split('.')[1])
        pkg_dependencies = temp_pkg.get('dependencies')
        pkg_messages = temp_pkg.get('messages') 
        ext_type = 'MessageOptions'

    # Iterating available packages and extendable messages
    avail_extensions = []
    for pkg in pkg_dependencies:
        if 'google.protobuf.' not in pkg:
            temp_pkg = wz_json.get_package(pkg.split('.')[1])
            for ext in _get_extensions(temp_pkg.get('messages'),ext_type):
                avail_extensions.append(ext)
    for ext in _get_extensions(pkg_messages,ext_type):
        avail_extensions.append(ext)
    if len(avail_extensions) == 0:
        print_error("Make sure your package / service has been imported with the package wrapper for extensions !",True,"No available messages to extend")
    # Insert into prompt
    list_avail_ext = []
    for avail_ext in avail_extensions:
        avail_ext_display_name = avail_ext.get('name') if avail_ext.get('description') is None or avail_ext.get('description') == 'None' else '{} - {}'.format(avail_ext.get('name'),avail_ext.get('description'))
        list_avail_ext.append((avail_ext_display_name,avail_ext.get('fullName')))
    if len(list_avail_ext) > 0:
        # If extension argument value has not passed into function
        if extension is None:
            results = inquirer.prompt([inquirer.List('extension','Chose extension to use',choices=list_avail_ext)],theme=WebezyTheme())
            if results is not None:
                results = next((ext for ext in avail_extensions if ext.get('fullName') == results['extension']))
        
        # Handle argument passed
        else:
            results = next((ext for ext in avail_extensions if ext.get('fullName') == extension),None)
    else:
        results = None
        
    return results


def handle_ext_field_message(message_full_name,wz_json:helpers.WZJson,old_ext=None):
    value = None
    temp_msg = wz_json.get_message(message_full_name)
    avail_extension_message_fields = []

    for f in temp_msg.get('fields'):
        avail_extension_message_fields.append((f.get('name'),f.get('fullName')))
    
    extended_message_field = inquirer.prompt([inquirer.List('extension_message_field','Enter an extension value for',avail_extension_message_fields)],theme=WebezyTheme())
    if extended_message_field is not None:
        for f in temp_msg.get('fields'):
            if f.get('fullName') == extended_message_field['extension_message_field']:
                if 'LABEL_OPTIONAL' == f.get('label'):
                    # Recursive for nested messages
                    if f.get('fieldType') == 'TYPE_MESSAGE':
                        f = handle_ext_field_message(f.get('messageType'),wz_json)
                    
                    # Handle enums
                    elif f.get('fieldType') == 'TYPE_ENUM':
                        enum_message = wz_json.get_enum(f.get('enumType'))
                        enum_values = []
                        for v in enum_message.get('values'):
                            enum_values.append(v.get('name'))
                        value = inquirer.prompt([inquirer.List('enum_value','Chose enum value for {}'.format(f.get('fullName')),enum_values)],theme=WebezyTheme())  
                        if value is not None:
                            value = value['enum_value']
                    elif f.get('fieldType') == 'TYPE_STRING':
                        value = inquirer.prompt([inquirer.Text('string_value','Enter string value for {}'.format(f.get('fullName')))],theme=WebezyTheme())  
                        if value is not None:
                            value = value['string_value']
                    elif f.get('fieldType') == 'TYPE_FLOAT' or f.get('fieldType') == 'TYPE_DOUBLE':
                        value = inquirer.prompt([inquirer.Text('float_value','Enter double/float value for {}'.format(f.get('fullName')))],theme=WebezyTheme())  
                        if value is not None:
                            value = float(value['float_value'])
                    elif 'TYPE_INT' in f.get('fieldType'):
                        value = inquirer.prompt([inquirer.Text('int_value','Enter integer value for {}'.format(f.get('fullName')))],theme=WebezyTheme())  
                        if value is not None:
                            value = int(value['int_value'])
                    elif 'TYPE_BOOL' in f.get('fieldType'):
                        value = inquirer.prompt([inquirer.Confirm('bool_value','Enter boolean value for {}'.format(f.get('fullName')))],theme=WebezyTheme())  
                        if value is not None:
                            value = value['bool_value']
                    else:
                        raise errors.WebezyValidationError('Extension field type not valid','Unsupported {} field type for extensions'.format(f.get('fieldType')))
                    
                    temp_struct = google_dot_protobuf_dot_struct__pb2.Struct()
                    temp_dict = {}
                    if old_ext is not None:
                        for k in old_ext:
                            if k != f.get('name'):
                                temp_struct.update({k:old_ext[k]})
                            temp_dict[k]=old_ext[k]
                    # print_error(temp_dict,True,'old')
                    # print_error(temp_struct,True,'current state')
                    # print_error(value,True,'current value')
                    temp_struct_2 = google_dot_protobuf_dot_struct__pb2.Struct()
                    temp_struct_2.update({f.get('name'):value})
                    temp_struct.MergeFrom(temp_struct_2)
                    # print_error(temp_struct,True,'Merged state')

                    return google_dot_protobuf_dot_struct__pb2.Value(struct_value=temp_struct)
                        
                elif 'LABEL_REPEATED' == f.get('label'):
                    print_error("Not supporting repeated type yet")
                    exit(1)
                else:
                    raise errors.WebezyValidationError('Unsupported label type','Unsupporting label {} for extensions'.format(temp_extended_field.get('label'))) 
            else:
                print_warning("Not supporting editing extensions from CLI yet")


def handle_ext_field(ext_field,wz_json:helpers.WZJson,old_ext=None):
    value = None
    # temp_msg = wz_json.get_message(message_full_name)
    # avail_extension_message_fields = []

    # for f in temp_msg.get('fields'):
        # avail_extension_message_fields.append((f.get('name'),f.get('fullName')))
    if ext_field.get('fieldType') == 'TYPE_STRING':
        
        value = inquirer.prompt([inquirer.Text('string_value','Enter string value for {}'.format(ext_field.get('fullName')))],theme=WebezyTheme())  
        
        if value.get('string_value') is not None:
            return google_dot_protobuf_dot_struct__pb2.Value(string_value=value.get('string_value'))
        else:
            print_error("Must enter a valid string !")
            exit(1)
    elif ext_field.get('fieldType') == 'TYPE_INT32' or ext_field.get('fieldType') == 'TYPE_INT64':
        value = inquirer.prompt([inquirer.Text('num_value','Enter integer value for {}'.format(ext_field.get('fullName')))],theme=WebezyTheme())  
        
        if value.get('num_value') is not None:
            return google_dot_protobuf_dot_struct__pb2.Value(number_value=int(value.get('num_value')))
        else:
            print_error("Must enter a valid integer !")
            exit(1)
    elif ext_field.get('fieldType') == 'TYPE_FLOAT' or ext_field.get('fieldType') == 'TYPE_DOUBLE':
        value = inquirer.prompt([inquirer.Text('num_value','Enter float value for {}'.format(ext_field.get('fullName')))],theme=WebezyTheme())  
        
        if value.get('num_value') is not None:
            return google_dot_protobuf_dot_struct__pb2.Value(number_value=float(value.get('num_value')))
        else:
            print_error("Must enter a valid float !")
            exit(1)
    elif ext_field.get('fieldType') == 'TYPE_BOOL':
        value = inquirer.prompt([inquirer.Confirm('bool_value',message='Enter a bool value for {}'.format(ext_field.get('fullName')))],theme=WebezyTheme())  
        if value.get('bool_value') is not None:
            return google_dot_protobuf_dot_struct__pb2.Value(bool_value=value.get('bool_value'))
        else:
            print_error("Must enter a valid boolean !")
            exit(1)
    # extended_message_field = inquirer.prompt([inquirer.List('extension_message_field','Enter an extension value for',avail_extension_message_fields)],theme=WebezyTheme())
    # return google_dot_protobuf_dot_struct__pb2.Value()