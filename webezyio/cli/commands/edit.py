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
from posixpath import split
import re
import inquirer
from webezyio.architect import WebezyArchitect
from webezyio.cli.theme import WebezyTheme
from webezyio.commons import helpers,resources,errors
from inquirer import errors as inquirerErrors
from webezyio.commons.pretty import print_error, print_info,bcolors, print_success,print_warning
log = logging.getLogger('webezyio.cli.main')


def edit_message(resource,action,sub_action,wz_json:helpers.WZJson,architect:WebezyArchitect,expand):
    if action is None:
        action = choose_action()

    if action.lower() == 'remove':
        dependencies = get_dependencies(full_name=resource.get('fullName'),wz_json=wz_json)
        display_dependencies(dependencies,resource,wz_json)
       
        confirm = inquirer.prompt(questions=[
            inquirer.Text('delete', bcolors.WARNING+'Please enter "{0}" to confirm delete'.format(resource.get('fullName'))+bcolors.ENDC)
        ],theme=WebezyTheme())

        if confirm is None:
            print_error("\nCancelling deletion process")
            exit(1)

        else:
            print('')
            if confirm.get('delete') == resource.get('fullName'):
                for d in dependencies:
                    for k in d:
                        if d[k].get('kind') == resources.ResourceKinds.method.value:
                            architect.RemoveRpc(k+'.'+d[k].get('name'))
                            print_info("Removed {0} [{1}]".format(d[k].get('name'),d[k].get('kind')))
                        else:
                            print_error('Nout supported yet !')
                architect.RemoveMessage(resource.get('fullName'))
                architect.Save()
                print_success("Removed {0} [{1}] and all dependent resources".format(resource.get('fullName'),resource.get('kind')))
            else:
                print_error("Cancelling deletion process")

    else:
        if sub_action is None:
            sub_action = modify_resource([('Add fields','fields'),('Rename','name')])
        if sub_action == 'fields' :
            add_fields(resource,wz_json,architect=architect,expand=expand)
        else:
            print_error('Not supported yet !')
            exit(1)

def edit_enum(resource,action,sub_action,wz_json:helpers.WZJson,architect:WebezyArchitect,expand):
    if action is None:
        action = choose_action()

    if action.lower() == 'remove':
        dependencies = get_dependencies(full_name=resource.get('fullName'),wz_json=wz_json)
        display_dependencies(dependencies,resource,wz_json)
        confirm = inquirer.prompt(questions=[
            inquirer.Text('delete', bcolors.WARNING+'Please enter "{0}" to confirm delete'.format(resource.get('fullName'))+bcolors.ENDC)
        ],theme=WebezyTheme())

        if confirm is None:
            print_error("\nCancelling deletion process")
            exit(1)

        else:
            print('')
            if confirm.get('delete') == resource.get('fullName'):
                architect.RemoveEnum(resource.get('fullName'))
                architect.Save()
                print_success("Removed {0} [{1}] and all dependent resources".format(resource.get('fullName'),resource.get('kind')))
            else:
                print_error("Cancelling deletion process")
    else:
        if sub_action is None:
            sub_action = modify_resource([('Add values','values'),('Rename','name')])
        if sub_action == 'values' :
            add_values(resource,wz_json,architect=architect,expand=expand)
        else:
            print_error('Not supported yet !')
            exit(1)

def edit_rpc(resource,action,sub_action,wz_json:helpers.WZJson,architect:WebezyArchitect,expand):
    if action is None:
        action = choose_action()

    temp_full_name = None
    
    for s in wz_json.services:
        method = next((r for r in wz_json.services[s].get('methods') if r.get('name') == resource.get('name')),None)
        if method is not None:
            temp_full_name = wz_json.services[s].get('fullName') + '.' + resource.get('name')
    
    if temp_full_name is None:
        print_error("Canot find RPC {0}".format(resource.get('name')))
        exit(1)
    
    if action.lower() == 'remove':
        confirm = inquirer.prompt(questions=[
            inquirer.Text('delete', bcolors.WARNING+'Please enter "{0}" to confirm delete'.format(temp_full_name)+bcolors.ENDC)
        ],theme=WebezyTheme())

        if confirm is None:
            print_error("\nCancelling deletion process")
            exit(1)
        else:
            print('')
            if confirm.get('delete') == temp_full_name:
                architect.RemoveRpc(temp_full_name)
                architect.Save()
                print_success("Removed {0} [{1}]".format(temp_full_name,resource.get('kind')))
            else:
                print_error("Cancelling deletion process")
    else:
        print_error('Not supported yet !')
        exit(1)

def edit_package():
    print_error('Not supported yet !')
    exit(1)


def edit_service():
    print_error('Not supported yet !')
    exit(1)


def edit_project():
    print_error('Not supported yet !')
    exit(1)


def edit_enum_value():
    print_error('Not supported yet !')
    exit(1)


def edit_field():
    print_error('Not supported yet !')
    exit(1)


def choose_action():
    action = inquirer.prompt([
        inquirer.List('action',message='Choose an action on resource',choices=['Remove','Modify'])
    ],theme=WebezyTheme())

    if action is None:
        print_error("Must choose an action for editing resource")
        exit(1)

    else:
        action = action['action']
        if action == 'Modify':
            log.debug("Modifing resource")
        elif action == 'Remove':
            log.debug("Removing resource")

        return action

def modify_resource(choices):
    
    mod = inquirer.prompt([
        inquirer.List('sub_action','Choose a modification',choices=choices)
    ])

    if mod is None:
        print_error("Must choose an modification type for editing resource")
        exit(1)

    else:
        return mod['sub_action']

def add_fields(resource,wz_json:helpers.WZJson,architect=WebezyArchitect,expand=False):
    add_field = True
    msg_full_name = resource.get('fullName')
    avail_msgs = []
    avail_field_ext = []
    package = wz_json.get_package(msg_full_name.split('.')[1], False)
    pkg = package.package
    description = resource.get('description')
    add_field = True
    temp_fields = []
    msg_fields =[]
    for f in resource.get('fields'):
        msg_fields.append(helpers.WZField(f.get('name'),f.get('fieldType'),f.get('label'),f.get('messageType'),f.get('enumType'),f.get('extensions'),f.get('description'),key_type=f.get('keyType'),value_type=f.get('valueType'),oneof_fields=f.get('oneofFields')).to_dict())
    for msg in package.messages:
        if msg.extension_type == 0 and msg.full_name != msg_full_name:
            if msg.description is not None:
                desc = f' - '+bcolors.OKBLUE+msg.description+ bcolors.ENDC
            else:
                desc=''
            avail_msgs.append((f'{msg.name}{desc}', msg.full_name))
        else:
            if resources.Options.Name(msg.extension_type) == 'FieldOptions':
                for f in msg.fields:
                    avail_field_ext.append((f.name,f.full_name))

    avail_enums = []
    for enum in package.enums:
        avail_enums.append((enum.name, enum.full_name))
    for d in package.dependencies:

        if 'google.protobuf' in d:
            # webezy_json.get_package()
            ext_msg_pkg = '.'.join(d.split('.')[:-1])
            avail_msgs.append(
                (d.split('.')[-1], '{0}.{1}'.format(ext_msg_pkg, d.split('.')[-1])))
        else:
            d_package = wz_json.get_package(
                d.split('.')[1],False)
            if d_package is not None:
                for msg in d_package.messages:
                    if msg.description is not None:
                        desc =' - '+bcolors.OKBLUE+msg.description  + bcolors.ENDC
                    else:
                        desc = ''
                    avail_msgs.append((f'{msg.name} [{msg.full_name}]'+desc, msg.full_name))
    
            for m in d_package.messages:
                if m.extension_type is not None:
                    if resources.Options.Name(m.extension_type) == 'FieldOptions':
                        for f in m.fields:
                            avail_field_ext.append((f.name,f.full_name))
    extend = None
    if expand:
        extend = inquirer.prompt([inquirer.Confirm('extend',message='Do you want to extend a message?')],theme=WebezyTheme())
        if extend.get('extend'):
            extend = inquirer.prompt([inquirer.List('extend','Choose message extension',choices=[resources.Options.Name(resources.Options.FieldOptions),resources.Options.Name(resources.Options.MessageOptions),resources.Options.Name(resources.Options.FileOptions)])],theme=WebezyTheme())
            extend=resources.Options.Value(extend['extend'])
        else:
            extend = None
        description = inquirer.prompt([inquirer.Text('description','Enter message description','')],theme=WebezyTheme())
        if description is not None:
            description = description['description']

    while add_field == True:
        opt = []
        for f in resources.fields_opt:
            opt.append((f.split('_')[1].lower(), f))
        labels = []

        for l in resources.field_label:
            labels.append((l.split('_')[1].lower(), l))
        field = inquirer.prompt([
            inquirer.Text(
                'field', 'Enter field name', validate=helpers.validation),
            inquirer.List(
                'fieldType', 'Choose field type', choices=opt)
        ], theme=WebezyTheme())

        label = None
        if field is not None:
            if field.get('fieldType') != 'TYPE_MAP' and field.get('fieldType') != 'TYPE_ONEOF':
                label = inquirer.prompt([inquirer.List(
                    'fieldLabel', 'Choose field label', choices=labels)], theme=WebezyTheme())

        message_type = None
        enum_type = None

        if field['fieldType'] == resources.WZFieldDescriptor.Type.Name(resources.WZFieldDescriptor.Type.TYPE_MESSAGE):
            if len(avail_msgs) == 0:
                print_warning("No messages availabe for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'message', 'Choose available messages', choices=avail_msgs)
                ], theme=WebezyTheme())
                message_type = message['message']

        elif field['fieldType'] == resources.WZFieldDescriptor.Type.Name(resources.WZFieldDescriptor.Type.TYPE_ENUM):
            if len(avail_enums) == 0:
                print_warning("No enums available for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'enum', 'Choose available enums', choices=avail_enums)
                ], theme=WebezyTheme())
                enum_type = message['enum']

        if field is None:
            add_field = False
        else:
            new_field = field['field']
            helpers.field_exists_validation(
                new_field, temp_fields, msg_full_name)
            f_ext = None
            if expand:
                if len(avail_field_ext) > 0 and extend == None:
                    extend_field = inquirer.prompt([inquirer.Confirm('extend',message='Do you want to add field extension?')],theme=WebezyTheme())
                    if extend_field.get('extend'):
                        f_ext = inquirer.prompt([inquirer.List('extensions','Choose extension',choices=avail_field_ext)],theme=WebezyTheme())
                        temp_pkg = wz_json.get_package(f_ext['extensions'].split('.')[1],False)
                        temp_msg = next((m for m in temp_pkg.messages if m.name == f_ext['extensions'].split('.')[3]),None)
                        temp_field = next((f for f in temp_msg.fields if f.name == f_ext['extensions'].split('.')[-1]),None)
                        if resources.WZFieldDescriptor.Type.Name(temp_field.field_type) == 'TYPE_BOOL':
                            f_ext_v = inquirer.prompt([inquirer.Confirm('ext_value','Enter extension bool value',default=False)],theme=WebezyTheme())
                        elif resources.WZFieldDescriptor.Type.Name(temp_field.field_type) == 'TYPE_DOUBLE' or resources.WZFieldDescriptor.Type.Name(temp_field.field_type) == 'TYPE_FLOAT':
                            f_ext_v = inquirer.prompt([inquirer.Text('ext_value','Enter extension float value',validate=helpers.float_value_validate)],theme=WebezyTheme())
                            try:
                                f_ext_v = float(f_ext_v['ext_value'])
                            except Exception as e:
                                logging.exception(e)
                                exit(1)
                        elif resources.WZFieldDescriptor.Type.Name(temp_field.field_type) == 'TYPE_INT32' or resources.WZFieldDescriptor.Type.Name(temp_field.field_type) == 'TYPE_INT64':
                            f_ext_v = inquirer.prompt([inquirer.Text('ext_value','Enter extension integer value',validate=helpers.int_value_validate)],theme=WebezyTheme())
                            try:
                                f_ext_v = int(f_ext_v['ext_value'])
                            except Exception as e:
                                logging.exception(e)
                                exit(1)
                        elif resources.WZFieldDescriptor.Type.Name(temp_field.field_type) == 'TYPE_STRING':
                            f_ext_v = inquirer.prompt([inquirer.Text('ext_value','Enter extension string value')],theme=WebezyTheme())
                        temp_ext_name = f_ext['extensions'].split('.')
                        if '.'.join(temp_ext_name[:-2]) == pkg:
                           f_ext  = {'.'.join(temp_ext_name[-2:]):f_ext_v}
                        else:
                           f_ext  = {f_ext['extensions']:f_ext_v}

                f_description = inquirer.prompt([inquirer.Text('description','Enter field description','')],theme=WebezyTheme())                                
                if f_description is not None:
                    f_description = f_description['description']
            else:
                f_description = ''        
                
            temp_fields.append(new_field)
            map_types = None
            oneof_fields = []
            if field['fieldType'] == 'TYPE_MAP':
                map_types = inquirer.prompt([
                    inquirer.List(
                        'keyType', '[MAP] Choose key type', choices=[o for o in opt if o[1] != 'TYPE_BOOL' and  o[1] != 'TYPE_FLOAT' and o[1] != 'TYPE_DOUBLE' and o[1] != 'TYPE_ENUM' and o[1] != 'TYPE_MESSAGE' and o[1] != 'TYPE_MAP' and o[1] != 'TYPE_ONEOF' and o[1] != 'TYPE_BYTES']),
                    inquirer.List(
                        'valueType', '[MAP] Choose value type', choices=[o for o in opt if o[1] != 'TYPE_MAP' and o[1] != 'TYPE_ONEOF'])
                ], theme=WebezyTheme())
                
                if map_types.get('valueType') == 'TYPE_MESSAGE' or map_types.get('valueType') == 'TYPE_ENUM':
                    if map_types.get('valueType') == 'TYPE_MESSAGE':
                        if len(avail_msgs) == 0:
                            print_warning("[MAP] No messages availabe for field")
                            exit(1)
                        else:
                            message = inquirer.prompt([
                                inquirer.List(
                                    'message', '[MAP] Choose available messages', choices=avail_msgs)
                            ], theme=WebezyTheme())
                            message_type = message['message']
                    elif map_types.get('valueType') == 'TYPE_ENUM':
                        if len(avail_enums) == 0:
                            print_warning("[MAP] No enums available for field")
                            exit(1)
                        else:
                            message = inquirer.prompt([
                                inquirer.List(
                                    'enum', '[MAP] Choose available enums', choices=avail_enums)
                            ], theme=WebezyTheme())
                            enum_type = message['enum']
            elif field['fieldType'] == 'TYPE_ONEOF':
                temp_fields_oneof = []
                add_field_oneof = True
                oneof_fields = add_fields_oneof(add_field_oneof,avail_msgs=avail_msgs,avail_enums=avail_enums,pre_fields=temp_fields_oneof,msg_full_name=msg_full_name)

            msg_fields.append(helpers.WZField(
                new_field, field['fieldType'], label['fieldLabel'] if label is not None else 'LABEL_OPTIONAL',
                message_type=message_type, enum_type=enum_type, description=f_description,
                extensions=f_ext, key_type=map_types.get('keyType') if map_types is not None else None, value_type=map_types.get('valueType') if map_types is not None else None, oneof_fields=oneof_fields).to_dict())

            nextfield = inquirer.prompt([
                inquirer.Confirm(
                    'continue', message='Add more fields?', default=True)
            ], theme=WebezyTheme())
            if nextfield is None:
                add_field = False
            else:
                if nextfield['continue'] == False:
                    add_field = False
    architect.EditMessage(package, resource.get('name'),
                            msg_fields, description, extend)
    architect.Save()

def add_fields_oneof(add_field:bool,avail_msgs,avail_enums,pre_fields,msg_full_name):
    final_fields = pre_fields
    while add_field:
        opt = []
        for f in resources.fields_opt:
            opt.append((f.split('_')[1].lower(), f))
        labels = []
        for l in resources.field_label:
            labels.append((l.split('_')[1].lower(), l))

        field = inquirer.prompt([
            inquirer.Text(
                'field', '[ONEOF] Enter field name', validate=helpers.validation),
            inquirer.List(
                'fieldType', '[ONEOF] Choose field type', choices=[o for o in opt if o != 'TYPE_MAP' and o != 'TYPE_ONEOF']),

        ], theme=WebezyTheme())

        label = None
        message_type = None
        enum_type = None

        if field['fieldType'] == resources.FieldDescriptor.Type.Name(resources.FieldDescriptor.Type.TYPE_MESSAGE):
            if len(avail_msgs) == 0:
                print_warning("[ONEOF] No messages availabe for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'message', '[ONEOF] Choose available messages', choices=avail_msgs)
                ], theme=WebezyTheme())
                message_type = message['message']

        elif field['fieldType'] == resources.FieldDescriptor.Type.Name(resources.FieldDescriptor.Type.TYPE_ENUM):
            if len(avail_enums) == 0:
                print_warning("[ONEOF] No enums available for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'enum', '[ONEOF] Choose available enums', choices=avail_enums)
                ], theme=WebezyTheme())
                enum_type = message['enum']

        if field is None:
            add_field = False
        else:
            new_field = field['field']
            helpers.field_exists_validation(
                new_field, final_fields, msg_full_name+'.'+new_field)

        final_fields.append(helpers.WZField(
                new_field, field['fieldType'], label['fieldLabel'] if label is not None else 'LABEL_OPTIONAL',
                message_type=message_type, enum_type=enum_type, description=None,
                extensions=None, key_type=None, value_type=None, oneof_fields=[]).to_dict())

        nextfield = inquirer.prompt([
            inquirer.Confirm(
                'continue', message='[ONEOF] Add more fields?', default=True)
        ], theme=WebezyTheme())
        if nextfield is None:
            add_field = False
        else:
            if nextfield['continue'] == False:
                add_field = False
    return final_fields

def add_values(resource,wz_json:helpers.WZJson,architect=WebezyArchitect,expand=False):
    enum_name = resource['name']
    pkg = resource['fullName'].split('.')[1]
    package = wz_json.get_package(pkg, False)
    if package.enums:
        if next((e for e in package.enums if e.name == enum_name),None) is None:
            print_error(f'Enum "{enum_name}" not exists under "{pkg}" package')
            exit(1)
    add_value = True
    e_values = []
    for ev in resource.get('values'):
        e_values.append(helpers.WZEnumValue(ev.get('name'),ev.get('number')).to_dict())
    print_info(e_values)
    while add_value:
        ev = inquirer.prompt([
            inquirer.Text(
                'name', 'Enter value name', validate=helpers.validation),
            inquirer.Text(
                'value', 'Enter enum value',validate=helpers.enum_value_validate),
        ], theme=WebezyTheme())
        if ev is not None:
            if int(ev['value']) == 0:
                print_warning('Enum values with 0 will be ignored by gRPC and should be used only as default value')
            confirm = inquirer.prompt([inquirer.Confirm('continue',message='Add more values?',default=True)],theme=WebezyTheme())
            v_name = ev['name']
            
            if confirm.get('continue') == False or confirm.get('continue') == None:
                add_value = False
            if next((v for v in e_values if v['name'] == ev['name']),None) is not None:
                print_error(f'Enum values names must be unique ! {v_name} appears already in {enum_name}')
                exit(1)
            if next((v for v in e_values if v.get('number') == int(ev.get('value'))),None) is not None:
                print_error('Enum values must be unique inside the enum scope !')
                exit(1)

            for e in package.enums:
                if next((v for v in e.values if v.name == ev['name']),None):
                    print_error(f'Enum values names must be unique in all enums in package ! {v_name} appears already in {e.full_name}')
                    exit(1)
            

            e_values.append(helpers.WZEnumValue(ev['name'],int(ev['value'])).to_dict())
        else:
            print_error("Enum values are required")
            exit(1)
    if next((v for v in e_values if v['number'] == None or v['number'] == 0),None) is None:
        e_values.insert(0,helpers.WZEnumValue(f'UNKNOWN_{enum_name.upper()}',0).to_dict())
        print_warning(f'Adding default enum value "UNKNOWN_{enum_name.upper()}" : 0')

    architect.EditEnum(package, enum_name, e_values)
    architect.Save()

def get_dependencies(full_name,wz_json:helpers.WZJson):
    log.debug(f"Getting dependent resources on {full_name}")
    dependent_resources = []
    if len(full_name.split('.')) == 3:
        # Package

        for s in wz_json.services:
            svc = wz_json.services[s]
            if svc.get('dependencies'):
                if full_name in svc.get('dependencies'):
                    for rpc in svc.get('methods'):
                        if full_name in rpc.get('outputType'):
                            dependent_resources.append({ svc.get('name') : rpc})
                        elif full_name in rpc.get('inputType'):
                            dependent_resources.append({ svc.get('name') : rpc})
                else:
                    pass
            else:
                log.debug(f"Service {s} not holding any dependencies !")

    elif len(full_name.split('.')) == 4:
        pkg_name = '.'.join(full_name.split('.')[:-1])
        # Descriptors
        log.debug(f'Got descriptor resource to check {pkg_name}')
        for p in wz_json.packages:
            pkg = wz_json.packages[p]

            if pkg.get('dependencies'):
                if pkg_name in pkg.get('dependencies'):
                    for m in pkg.get('messages'):
                        for f in m.get('fields'):
                            if f.get('messageType'):
                                if full_name in f.get('messageType'):
                                    dependent_resources.append(m)
                                    break
                elif pkg_name == pkg.get('package'):
                    for m in pkg.get('messages'):
                        for f in m.get('fields'):
                            if f.get('messageType'):
                                if full_name in f.get('messageType'):
                                    dependent_resources.append(m)
                                    break
            elif pkg_name == pkg.get('package'):
                for m in pkg.get('messages'):
                    for f in m.get('fields'):
                        if f.get('messageType'):
                            if full_name in f.get('messageType'):
                                dependent_resources.append(m)
                                break
            else:
                pass

        for s in wz_json.services:
            svc = wz_json.services[s]
            if svc.get('dependencies'):
                if pkg_name in svc.get('dependencies'):
                    for rpc in svc.get('methods'):
                        if full_name in rpc.get('outputType'):
                            dependent_resources.append({ svc.get('fullName') : rpc})
                        elif full_name in rpc.get('inputType'):
                            dependent_resources.append({ svc.get('fullName') : rpc})

        if len(full_name.split('.')) > 4:
            """Unknown"""
            pass
    
    return dependent_resources
    

def display_dependencies(dependencies,resource,wz_json):
    if len(dependencies) > 0:
        print_info("The following resources are going to be affected from deleting {0}:\n".format(resource.get('fullName')))
        for d in get_dependencies(full_name=resource.get('fullName'),wz_json=wz_json):
            if d.get('name') is not None:
                print_warning('- {0} [{1}]'.format(d.get('name'),d.get('kind')))
            else:
                for k in d:
                    depend = (k,d[k])

                print_warning('- {0} -> {1} [{2}]'.format(depend[0],depend[1].get('name'),depend[1].get('kind')))
    print('')
