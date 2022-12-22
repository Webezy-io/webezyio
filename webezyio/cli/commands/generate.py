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
from pprint import pprint
import webezyio
from webezyio.architect import WebezyArchitect
from webezyio.cli.theme import WebezyTheme
from webezyio.commons.helpers import WZJson, WZField, WZEnumValue
from webezyio.commons.pretty import print_info, print_warning, print_error, print_note, print_success, bcolors
from webezyio.commons.protos import WebezyFieldType, WebezyFieldLabel, WebezyExtension
from webezyio.commons.errors import WebezyProtoError
import inquirer
from inquirer import errors
import re

fields_opt = [
    WebezyFieldType.Name(WebezyFieldType.TYPE_DOUBLE),
    WebezyFieldType.Name(WebezyFieldType.TYPE_FLOAT),
    WebezyFieldType.Name(WebezyFieldType.TYPE_INT64),
    WebezyFieldType.Name(WebezyFieldType.TYPE_INT32),
    WebezyFieldType.Name(WebezyFieldType.TYPE_BOOL),
    WebezyFieldType.Name(WebezyFieldType.TYPE_STRING),
    WebezyFieldType.Name(WebezyFieldType.TYPE_MESSAGE),
    WebezyFieldType.Name(WebezyFieldType.TYPE_BYTES),
    WebezyFieldType.Name(WebezyFieldType.TYPE_ENUM),
    WebezyFieldType.Name(WebezyFieldType.TYPE_ONEOF),
    WebezyFieldType.Name(WebezyFieldType.TYPE_MAP),

]
field_label = [
    WebezyFieldLabel.Name(WebezyFieldLabel.LABEL_OPTIONAL),
    WebezyFieldLabel.Name(WebezyFieldLabel.LABEL_REPEATED),
]

well_known_type = ['google.protobuf.Timestamp', 'google.protobuf.Struct']


def package(results, webezy_json: WZJson, architect: WebezyArchitect, expand=False, verbose=False):
    pkg = results['package']
    if pkg.lower() == 'package':
        print_error(
            "Do not name your package as 'package' it can cause issues down the road\n\t-> please choose another name for your package")
        exit(1)
    list_depend = well_known_type
    prj_name = webezy_json.project.get('name')
    description = None
    if webezy_json.packages is not None:
        try:
            if webezy_json.get_package(pkg):
                print_error(
                    f'Package [{pkg}] is already defined under "{prj_name}" project')
                exit(1)
        except Exception:
            logging.debug("Package not found continuing...")
        for p in webezy_json.packages:
            list_depend.append(webezy_json.packages[p]['package'])
    temp_d_list = []
    if expand:
        description = inquirer.prompt([inquirer.Text(
            'description', 'Enter package description', '')], theme=WebezyTheme())
        description = description.get('description')
        dependencies = inquirer.prompt([
            inquirer.Checkbox(
                'dependencies', 'Choose package dependencies', choices=list_depend)
        ], theme=WebezyTheme())
        temp_d_list = dependencies['dependencies']

    if verbose:
        print_note(pkg, True, 'Added package')

    architect.AddPackage(pkg, temp_d_list, description=description)
    architect.Save()
    print_success(f'Success !\n\tCreated new package "{pkg}"')


def service(results, webezy_json: WZJson, architect: WebezyArchitect, expand=False, verbose=False):
    svc = results['service']
    if svc.lower() == 'service':
        print_error(
            "Do not set service name as 'service' it can cause issues down the road\n\t-> Please choose another name for your service")
        exit(1)
    list_depend = []
    if expand:
        if webezy_json.packages is not None:
            for p in webezy_json.packages:
                if webezy_json.packages[p]['name'].lower() == svc:
                    print_error(
                        f"Cannot create service {svc}, package by the same name is already exists !")
                    exit(1)
                list_depend.append(webezy_json.packages[p]['package'])
            depend = inquirer.prompt([
                inquirer.Checkbox(
                    'dependencies', 'Choose service dependencies', choices=list_depend),
            ], theme=WebezyTheme())
            if depend is not None:
                list_depend = depend['dependencies']

    if webezy_json.services is not None:
        if svc in webezy_json.services:
            print_error(
                f"Service '{svc}' already exists under '{webezy_json.project.get('name')}'")
            exit(1)

    if verbose:
        print_note(svc, True, 'Added Service')

    architect.AddService(svc, list_depend, None, [])
    architect.Save()

    print_success(f'Success !\n\tCreated new service "{svc}"')


def message(results, webezy_json: WZJson, architect: WebezyArchitect, expand=False, verbose=False, parent: str = None):
    msg_name = results['message']
    if msg_name.lower() == 'message':
        print_error(
            "Do not name your message as 'message' it can cause issues down the road\n\t-> please choose another name for your message")
        exit(1)

    pkg = results.get('package') if parent is None else parent
    msg_full_name = '{0}.{1}'.format(pkg, msg_name)
    description = ''
    add_field = True
    temp_fields = []
    msg_fields = []
    package = webezy_json.get_package(pkg.split('.')[1], False)
    avail_msgs = []
    avail_field_ext = []
    avail_msg_ext = []

    for msg in package.messages:
        if msg.extension_type == 0:
            if msg.description is not None and msg.full_name != msg_full_name:
                desc = f' - '+bcolors.OKBLUE+msg.description + bcolors.ENDC
            else:
                desc = ''
            avail_msgs.append((f'{msg.name}{desc}', msg.full_name))
        else:
            if WebezyExtension.Name(msg.extension_type) == 'FieldOptions':
                for f in msg.fields:
                    avail_field_ext.append((f'FieldOptions | {f.name}', f.full_name))
            elif WebezyExtension.Name(msg.extension_type) == 'MessageOptions':
                for f in msg.fields:
                    avail_msg_ext.append((f'MessageOptions | {f.name}', f.full_name))

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
            d_package = webezy_json.get_package(
                d.split('.')[1], False)
            if d_package is not None:
                for msg in d_package.messages:
                    if msg.description is not None:
                        desc = ' - '+bcolors.OKBLUE+msg.description + bcolors.ENDC
                    else:
                        desc = ''
                    avail_msgs.append(
                        (f'{msg.name} [{msg.full_name}]'+desc, msg.full_name))

            for m in d_package.messages:
                if m.extension_type is not None:
                    if WebezyExtension.Name(msg.extension_type) == 'FieldOptions':
                        for f in msg.fields:
                            avail_field_ext.append((f'FieldOptions | {f.name}', f.full_name))
                    elif WebezyExtension.Name(msg.extension_type) == 'MessageOptions':
                        for f in msg.fields:
                            avail_msg_ext.append((f'MessageOptions | {f.name}', f.full_name))
    extend = None
    if expand:
        extend = inquirer.prompt([inquirer.Confirm(
            'extend', message='Do you want to extend a message?')], theme=WebezyTheme())
        
        if extend.get('extend'):
            extend = inquirer.prompt([inquirer.List('extend', 'Choose message extension', choices=[WebezyExtension.Name(
                WebezyExtension.FieldOptions), WebezyExtension.Name(WebezyExtension.MessageOptions), WebezyExtension.Name(WebezyExtension.FileOptions),WebezyExtension.Name(WebezyExtension.ServiceOptions),WebezyExtension.Name(WebezyExtension.MethodOptions)])], theme=WebezyTheme())
            extend = WebezyExtension.Value(extend['extend'])
        else:
            extend = None
            # add_extension = inquirer.prompt([inquirer.List('add_message_extension','Do you want to add message level extension?')],theme=WebezyTheme())
        
        description = inquirer.prompt([inquirer.Text(
            'description', 'Enter message description', '')], theme=WebezyTheme())
        if description is not None:
            description = description['description']

    while add_field == True:

        opt = []
        for f in fields_opt:
            opt.append((f.split('_')[1].lower(), f))
        labels = []
        for l in field_label:
            labels.append((l.split('_')[1].lower(), l))

        field = inquirer.prompt([
            inquirer.Text(
                'field', 'Enter field name', validate=validation),
            inquirer.List(
                'fieldType', 'Choose field type', choices=opt),

        ], theme=WebezyTheme())
        label = None
        if field is not None:
            if field.get('fieldType') != 'TYPE_MAP' and field.get('fieldType') != 'TYPE_ONEOF':
                label = inquirer.prompt([inquirer.List(
                    'fieldLabel', 'Choose field label', choices=labels)], theme=WebezyTheme())

        message_type = None
        enum_type = None

        if field['fieldType'] == WebezyFieldType.Name(WebezyFieldType.TYPE_MESSAGE):
            if len(avail_msgs) == 0:
                print_warning("No messages availabe for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'message', 'Choose available messages', choices=avail_msgs)
                ], theme=WebezyTheme())
                message_type = message['message']

        elif field['fieldType'] == WebezyFieldType.Name(WebezyFieldType.TYPE_ENUM):
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
            field_exists_validation(
                new_field, temp_fields, msg_full_name)
            f_ext = None
            if expand:
                if len(avail_field_ext) > 0 and extend == None:
                    extend_field = inquirer.prompt([inquirer.Confirm(
                        'extend', message='Do you want to add field extension?')], theme=WebezyTheme())
                    if extend_field.get('extend'):
                        f_ext = inquirer.prompt([inquirer.List(
                            'extensions', 'Choose extension', choices=avail_field_ext)], theme=WebezyTheme())
                        temp_pkg = webezy_json.get_package(
                            f_ext['extensions'].split('.')[1], False)
                        temp_msg = next(
                            (m for m in temp_pkg.messages if m.name == f_ext['extensions'].split('.')[3]), None)
                        temp_field = next(
                            (f for f in temp_msg.fields if f.name == f_ext['extensions'].split('.')[-1]), None)
                        if WebezyFieldType.Name(temp_field.field_type) == 'TYPE_BOOL':
                            f_ext_v = inquirer.prompt([inquirer.Confirm(
                                'ext_value', 'Enter extension bool value', default=False)], theme=WebezyTheme())
                        elif WebezyFieldType.Name(temp_field.field_type) == 'TYPE_DOUBLE' or WebezyFieldType.Name(temp_field.field_type) == 'TYPE_FLOAT':
                            f_ext_v = inquirer.prompt([inquirer.Text(
                                'ext_value', 'Enter extension float value', validate=float_value_validate)], theme=WebezyTheme())
                            try:
                                f_ext_v = float(f_ext_v['ext_value'])
                            except Exception as e:
                                logging.exception(e)
                                exit(1)
                        elif WebezyFieldType.Name(temp_field.field_type) == 'TYPE_INT32' or WebezyFieldType.Name(temp_field.field_type) == 'TYPE_INT64':
                            f_ext_v = inquirer.prompt([inquirer.Text(
                                'ext_value', 'Enter extension integer value', validate=int_value_validate)], theme=WebezyTheme())
                            try:
                                f_ext_v = int(f_ext_v['ext_value'])
                            except Exception as e:
                                logging.exception(e)
                                exit(1)
                        elif WebezyFieldType.Name(temp_field.field_type) == 'TYPE_STRING':
                            f_ext_v = inquirer.prompt([inquirer.Text(
                                'ext_value', 'Enter extension string value')], theme=WebezyTheme())
                        temp_ext_name = f_ext['extensions'].split('.')
                        if '.'.join(temp_ext_name[:-2]) == pkg:
                            f_ext = {'.'.join(temp_ext_name[-2:]): f_ext_v}
                        else:
                            f_ext = {f_ext['extensions']: f_ext_v}

                f_description = inquirer.prompt([inquirer.Text(
                    'description', 'Enter field description', '')], theme=WebezyTheme())
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
                        'keyType', '[MAP] Choose key type', choices=[o for o in opt if  o[1] != 'TYPE_BOOL' and o[1] != 'TYPE_FLOAT' and o[1] != 'TYPE_DOUBLE' and o[1] != 'TYPE_ENUM' and o[1] != 'TYPE_MESSAGE' and o[1] != 'TYPE_MAP' and o[1] != 'TYPE_ONEOF' and o[1] != 'TYPE_BYTES']),
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
            msg_fields.append(WZField(
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

        if verbose:
            print_note(field, True, 'Added field')
    package = webezy_json.get_package(pkg.split('.')[1], False)
    if next((m for m in package.messages if m.name == msg_name), None) is None:
        if verbose:
            print_note(msg_name, True, 'Added Message')

        architect.AddMessage(package, msg_name,
                             msg_fields, description, extend)
        architect.Save()
        print_success("Created Message !\n")
    else:
        print_error(
            f'Message "{msg_name}" already exists under "{package.package}"')


def add_fields_oneof(add_field:bool,avail_msgs,avail_enums,pre_fields,msg_full_name):
    final_fields = pre_fields
    while add_field:
        opt = []
        for f in fields_opt:
            opt.append((f.split('_')[1].lower(), f))
        labels = []
        for l in field_label:
            labels.append((l.split('_')[1].lower(), l))

        field = inquirer.prompt([
            inquirer.Text(
                'field', '[ONEOF] Enter field name', validate=validation),
            inquirer.List(
                'fieldType', '[ONEOF] Choose field type', choices=[o for o in opt if o != 'TYPE_MAP' and o != 'TYPE_ONEOF']),

        ], theme=WebezyTheme())

        label = None
        message_type = None
        enum_type = None

        if field['fieldType'] == WebezyFieldType.Name(WebezyFieldType.TYPE_MESSAGE):
            if len(avail_msgs) == 0:
                print_warning("[ONEOF] No messages availabe for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'message', '[ONEOF] Choose available messages', choices=avail_msgs)
                ], theme=WebezyTheme())
                message_type = message['message']

        elif field['fieldType'] == WebezyFieldType.Name(WebezyFieldType.TYPE_ENUM):
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
            field_exists_validation(
                new_field, final_fields, msg_full_name+'.'+new_field)

        final_fields.append(WZField(
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

def rpc(results, webezy_json: WZJson, architect: WebezyArchitect, expand=None, parent: str = None):
    rpc = results['rpc']
    svc = results.get(
        'service') if parent is None else f'{webezy_json.domain}.{parent}.v1'
    full_name = '{0}.{1}'.format(svc, rpc)

    if webezy_json.get_rpc(full_name) is not None:
        print_error(
            f'RPC [{rpc}] is already defined under "{svc}" service')
        exit(1)

    dependencies = webezy_json.services[svc.split(
        '.')[1]].get('dependencies')

    if dependencies is None:
        svc_name = svc.split('.')[1]
        print_error(
            f'Dependencies not listed under "{svc}"\n\tTry attache first a packge to service\n\tRun: \'wz package <some.package.v1> {svc_name}\'')
        exit(1)

    avail = []
    for d in dependencies:
        pkg = webezy_json.get_package(d.split('.')[1])
        msgs = pkg.get('messages')
        if msgs is not None:
            for m in msgs:
                avail.append(m['fullName'])
    if len(avail) == 0:
        print_error('Messages not listed under packages')
        exit(1)

    description = None
    if expand:
        description = inquirer.prompt(
            [inquirer.Text('description', 'Enter RPC description', '')], theme=WebezyTheme())
        if description is not None:
            description = description['description']

    inputs_outputs = inquirer.prompt([
        inquirer.List(
            "input_type", message="Choose the input type", choices=avail),
        inquirer.List(
            "output_type", message="Choose the output type", choices=avail),
    ], theme=WebezyTheme())
    if inputs_outputs is None:
        print_error('IN/OUT Types are required for RPC')
        exit(1)
    architect.AddRPC(webezy_json.get_service(svc.split('.')[1], False), rpc, [
        (results['type'][0], inputs_outputs['input_type']), (results['type'][1], inputs_outputs['output_type'])], description)
    architect.Save()
    print_success(f'Success !\n\tCreated new RPC "{rpc}"')
    lang = webezy_json.project.get('server').get('language')
    lang_suffix = 'ts' if lang == 'typescript' else 'py' if lang == 'python' else 'Unknown'
    path_to_svc = webezy_json.path+'/services/' + \
        svc.split('.')[1]+'.'+lang_suffix
    print_warning(
        f'\t- Make sure you are adding the new RPC "{rpc}" method to your service implemantation file at {path_to_svc}')
    print_warning(
        f'\t- For more information on how to edit your service implemantation files see https://www.webezy.io/tutorial/add-new-rpc?lang='+lang)


def enum(results, webezy_json: WZJson, architect: WebezyArchitect, parent: str):
    enum_name = results['enum']
    pkg = results['package'] if parent is None else parent
    package = webezy_json.get_package(pkg.split('.')[1], False)
    if package.enums:
        if next((e for e in package.enums if e.name == enum_name), None) is not None:
            print_error(
                f'Enum "{enum_name}" already exists under "{pkg}" package')
            exit(1)
    add_value = True
    e_values = []
    while add_value:
        ev = inquirer.prompt([
            inquirer.Text(
                'name', 'Enter value name', validate=validation),
            inquirer.Text(
                'value', 'Enter enum value', validate=enum_value_validate),
        ], theme=WebezyTheme())
        if ev is not None:
            if int(ev['value']) == 0:
                print_warning(
                    'Enum values with 0 will be ignored by gRPC and should be used only as default value')
            confirm = inquirer.prompt([inquirer.Confirm(
                'continue', message='Add more values?', default=True)], theme=WebezyTheme())
            v_name = ev['name']

            if confirm.get('continue') == False or confirm.get('continue') == None:
                add_value = False
            if next((v for v in e_values if v['name'] == ev['name']), None) is not None:
                print_error(
                    f'Enum values names must be unique ! {v_name} appears already in {enum_name}')
                exit(1)
            if next((v for v in e_values if v.get('number') == int(ev.get('value'))), None) is not None:
                print_error(
                    'Enum values must be unique inside the enum scope !')
                exit(1)

            for e in package.enums:
                if next((v for v in e.values if v.name == ev['name']), None):
                    print_error(
                        f'Enum values names must be unique in all enums in package ! {v_name} appears already in {e.full_name}')
                    exit(1)

            e_values.append(WZEnumValue(
                ev['name'], int(ev['value'])).to_dict())
        else:
            print_error("Enum values are required")
            exit(1)
    if next((v for v in e_values if v['number'] == 0), None) is None:
        e_values.insert(0, WZEnumValue(
            f'UNKNOWN_{enum_name.upper()}', 0).to_dict())
        print_warning(
            f'Adding default enum value "UNKNOWN_{enum_name.upper()}" : 0')
    architect.AddEnum(package, enum_name, e_values)
    architect.Save()


def field_exists_validation(new_field, fields, msg):
    if new_field in fields:
        raise WebezyProtoError(
            'Message', f'Field {new_field} already exits under {msg}')
    return True


def enum_value_validate(answers, current):
    try:
        int(current)
    except Exception:
        raise errors.ValidationError(
            current, reason='Enum Value MUST be an integer value')
    return True


def float_value_validate(answers, current):
    try:
        float(current)
    except Exception:
        raise errors.ValidationError(
            current, reason='Value must be valid float type')
    return True


def int_value_validate(answers, current):
    try:
        int(current)
    except Exception:
        raise errors.ValidationError(
            current, reason='Value must be valid integer type')
    return True


def validation(answers, current):

    if len(current) == 0:
        raise errors.ValidationError(
            current, reason='Resource name must not be blank')
    if len(re.findall('\s', current)) > 0:
        raise errors.ValidationError(
            current, reason='Resource name must not include blank spaces')
    if len(re.findall('-', current)) > 0:
        raise errors.ValidationError(
            current, reason='Resource name must not include hyphens, underscores are allowed')
    return True
