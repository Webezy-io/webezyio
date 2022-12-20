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
from webezyio.commons import helpers,resources,errors,protos
from inquirer import errors as inquirerErrors
from webezyio.commons.pretty import print_error, print_info,bcolors, print_note, print_success,print_warning
log = logging.getLogger('webezyio.cli.main')


def edit_message(resource,action,sub_actions,wz_json:helpers.WZJson,architect:WebezyArchitect,expand):
    """A function to edit a webezy.io message resource
    Args:
    ----
    resource - a dictionary full resource description to be edited
    action - remove / edit
    sub_action - Deeper action fo edit option: fields / name
    wz_json - webezy.json context
    architect - The architect class instantiated to the webezy.json context
    expand - If expanding optional inputs
    """

    if action is None:
        if sub_actions is not None:
            print_warning("Passed sub actions before passing action")
        action = choose_action()

    # Remove message
    if action.lower() == 'remove':
        # Getting dependencies for resources
        dependencies = get_dependencies(full_name=resource.get('fullName'),wz_json=wz_json)
        display_dependencies(dependencies,resource,'delete')
        
        # Prompting for deletion confirm
        confirm = inquirer.prompt(questions=[
            inquirer.Text('delete', bcolors.WARNING+'Please enter "{0}" to confirm delete'.format(resource.get('fullName'))+bcolors.ENDC)
        ],theme=WebezyTheme())

        if confirm is None:
            print_error("\nCancelling deletion process")
            exit(1)
        # Deletion process
        else:
            if confirm.get('delete') == resource.get('fullName'):
                # Removing resources that dependent on
                if dependencies is not None:
                    for d in dependencies:
                        for k in d:
                            # Remove RPC that have input / output type of the deleted message
                            if isinstance(d[k],str) == False and  isinstance(d[k],list) == False and isinstance(d[k],int) == False:
                                if d[k].get('kind') == resources.ResourceKinds.method.value:
                                    architect.RemoveRpc(k+'.'+d[k].get('name'))
                                    print_info("Removed {0} [{1}]".format(d[k].get('name'),d[k].get('kind')))
                            else:
                                if k == 'kind':
                                    # Remove Messages that have only 1 field and is type of the deleted message
                                    print_warning("[{}] Removing -> {}".format(d[k],d.get('fullName')))
                                    if d[k] == resources.ResourceKinds.message.value:
                                        architect.RemoveMessage(d.get('fullName'))
                                    # Remove fields that have type of the deleted message
                                    elif d[k] == resources.ResourceKinds.field.value:
                                        architect.RemoveField(d.get('fullName'))
                                    else:
                                        print_error('Not supporting dependency removal for {} of kind {}'.format(k,d))
                    
                # Removing message
                architect.RemoveMessage(resource.get('fullName'))
                architect.Save()
                print_success("Removed {0} [{1}] and all dependent resources".format(resource.get('fullName'),resource.get('kind')))
            else:
                print_error("Cancelling deletion process")
    # Edit
    else:
        # Prompting for sub-action
        if sub_actions is None:
            sub_actions = modify_resource([('Add fields','fields'),('Rename','name')])
        # Edit fields
        if sub_actions[0] == 'fields' :
            add_fields(resource,wz_json,architect=architect,expand=expand)
        # Renaming message
        elif sub_actions[0] == 'name':
            # Getting dependencies for resources
            dependencies = get_dependencies(full_name=resource.get('fullName'),wz_json=wz_json)
            display_dependencies(dependencies,resource,'rename')
            rename_message(resource,wz_json,architect,dependencies)
        # Not supporting option
        else:
            print_error("Not supporting editing {}".format(sub_actions))
            exit(1)

def edit_enum(resource,action,sub_actions,wz_json:helpers.WZJson,architect:WebezyArchitect,expand):
    """A function to edit enum resource type"""

    if action is None:
        if sub_actions is not None:
            print_warning("Passed sub actions before passing action")
        action = choose_action()

    # Remove enum
    if action.lower() == 'remove':
        # Getting all dependent resources
        dependencies = get_dependencies(full_name=resource.get('fullName'),wz_json=wz_json)
        display_dependencies(dependencies,resource,'delete')
        
        # Prompting for deletion confirm
        confirm = inquirer.prompt(questions=[
            inquirer.Text('delete', bcolors.WARNING+'Please enter "{0}" to confirm delete'.format(resource.get('fullName'))+bcolors.ENDC)
        ],theme=WebezyTheme())

        if confirm is None:
            print_error("\nCancelling deletion process")
            exit(1)
        
        # Deletion process
        else:
            print('')
            # TODO add dependent fields removal
            if confirm.get('delete') == resource.get('fullName'):
                if dependencies is not None:
                    for d in dependencies:
                        print_warning("[{}] Removing -> {}".format(d.get('kind'),d.get('fullName')))
                        if d.get('kind') == resources.ResourceKinds.field.value:
                            architect.RemoveField(d.get('fullName'))
                        elif d.get('kind') == resources.ResourceKinds.message.value:
                            architect.RemoveMessage(d.get('fullName'))

                architect.RemoveEnum(resource.get('fullName'))
                architect.Save()
                print_success("Removed {0} [{1}] and all dependent resources".format(resource.get('fullName'),resource.get('kind')))
            else:
                print_error("Cancelling deletion process")
    # Edit enum
    else:
        # Prompting for sub-action
        if sub_actions is None:
            sub_actions = modify_resource([('Add values','values'),('Rename','name')])
        # Add values
        if sub_actions[0] == 'values' :
            add_values(resource,wz_json,architect=architect,expand=expand)
        # Not supported option for enum editing
        else:
            print_error('{} Not supported yet !'.format(sub_actions[0]))
            exit(1)

def edit_rpc(resource,action,sub_actions,wz_json:helpers.WZJson,architect:WebezyArchitect,expand):
    """A function to edit RPC resource type"""

    if action is None:
        if sub_actions is not None:
            print_warning("Passed sub actions before passing action")
        action = choose_action()

    # Constructing temporary RPC "full_name"
    temp_full_name = None
    if wz_json.services is not None:
        for s in wz_json.services:
            method = next((r for r in wz_json.services[s].get('methods') if r.get('name') == resource.get('name')),None)
            if method is not None:
                temp_full_name = wz_json.services[s].get('fullName') + '.' + resource.get('name')
    else:
        print_error("No available RPC's to edit under {} project".format(wz_json.project.get('name')))
        exit(1)

    if temp_full_name is None:
        print_error("Canot find RPC {0}".format(resource.get('name')))
        exit(1)
    
    # Remove RPC
    if action.lower() == 'remove':
        
        # Prompting for deletion confirm
        confirm = inquirer.prompt(questions=[
            inquirer.Text('delete', bcolors.WARNING+'Please enter "{0}" to confirm delete'.format(temp_full_name)+bcolors.ENDC)
        ],theme=WebezyTheme())

        if confirm is None:
            print_error("\nCancelling deletion process")
            exit(1)

        # Deletion process of RPC
        # TODO check if RPC is the last one available on service and handle that
        else:
            print('')
            if confirm.get('delete') == temp_full_name:
                architect.RemoveRpc(temp_full_name)
                architect.Save()
                print_success("Removed {0} [{1}]".format(temp_full_name,resource.get('kind')))
            else:
                print_error("Cancelling deletion process")
    # Editing RPC
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


def edit_field(resource,action,sub_actions,wz_json:helpers.WZJson,architect:WebezyArchitect,expand,no_save=False):
    if action is None:
        if sub_actions is not None:
            print_warning("Passed sub actions before passing action")
        action = choose_action()
    # Remove Field
    if action.lower() == 'remove':

       # Prompting for deletion confirm
        confirm = inquirer.prompt(questions=[
            inquirer.Text('delete', bcolors.WARNING+'Please enter "{0}" to confirm delete'.format(resource.get('fullName'))+bcolors.ENDC)
        ],theme=WebezyTheme())

        if confirm is None:
            print_error("\nCancelling deletion process")
            exit(1)
        else:
            # TODO Check if message holding other field and handle it
            if confirm.get('delete') == resource.get('fullName'):
                architect.RemoveField(resource.get('fullName'))
                architect.Save()
                print_success("Removed {0} [{1}]".format(resource.get('fullName'),resource.get('kind')))
            else:
                print_error("Cancelling deletion process")

    elif action.lower() == 'modify':
        resource_full_name = resource.get('fullName')
        print_note('[{}] Sub Actions: {}'.format(resource_full_name,sub_actions),True,'Modifying field')
        # Prompting for sub-action
        if sub_actions is None:
            # Not supporting by intention changing label for ONEOF + MAP fields
            if resource.get('fieldType') != 'TYPE_ONEOF' and resource.get('fieldType') != 'TYPE_MAP':
                sub_actions = [('Change Label','label'),('Change Type','type'),('Rename','name')]
            else:
                sub_actions = [('Rename','name')]

            # TODO add handling of map type TYPE_MAP
            # One of type handling
            if resource.get('fieldType') == 'TYPE_ONEOF':
                sub_actions.append(('Modify oneof fields','oneof_modify'))
            # Message type handling
            if resource.get('fieldType') == 'TYPE_MESSAGE':
                sub_actions.append(('Change Message Type','message_type'))
            # Enum type handling
            if resource.get('fieldType') == 'TYPE_ENUM':
                sub_actions.append(('Change Enum Type','enum_type'))
            sub_actions = modify_resource(sub_actions)
        # Edit field type
        if sub_actions[0] == 'type' :
            print_error("Not supporting editing {}".format(sub_actions))
            exit(1)

        # Renaming field
        elif sub_actions[0] == 'name':
            print_error("Not supporting editing {}".format(sub_actions))
            exit(1)

        # Changing message_type if field type is TYPE_MESSAGE
        elif sub_actions[0] == 'message_type':
            # Getting message dict
            msg_name = '.'.join(resource.get('fullName').split('.')[:-1])
            _msg = wz_json.get_message(msg_name)

            # Getting package descriptor
            _pkg = wz_json.get_package(resource.get('fullName').split('.')[1],False)
            if _msg is not None:
                if len(sub_actions) > 1 :
                    if len(sub_actions[1].split('.')) == 4:
                        # if wz_json.get_message(sub_actions[1]) is not None:
                        # TODO check for dependecy
                        for f in _msg.get('fields'):
                            if f.get('fullName') == resource.get('fullName'):
                                f['messageType'] = sub_actions[1]
                                print_success("Changing message type for {} -> {}".format(f.get('fullName'),f['messageType']))
                        architect.EditMessage(_pkg, _msg.get('name'),
                            _msg.get('fields'), _msg.get('description'), _msg.get('extensionType'),extensions=_msg.get('extensions'))
                        if no_save==False:
                            architect.Save()
                        # else:
                        #     print_error('Message {} not exists under project !'.format(sub_actions[1]))
                        #     exit(1)
                    else:
                        print_error('Message type {} is not valid !'.format(sub_actions[1]))
                else:
                    _pkg_name = resource.get('fullName').split('.')[1]
                    _list_of_avail_messages = []
                    _field_msg_name = '.'.join(resource.get('fullName').split('.')[:-1])
                    if _pkg is not None:
                        if _pkg.dependencies is not None:
                            # Iterating pakcge dependencies
                            for dep in _pkg.dependencies:
                                if 'google.protobuf' not in dep:
                                    temp_pkg = wz_json.get_package(dep.split('.')[1])
                                    if temp_pkg.get('messages') is not None:
                                        for m in temp_pkg.get('messages'):
                                            if m.get('fullName') != resource.get('messageType'):
                                                _list_of_avail_messages.append(('{} [{}]'.format(m.get('name'),dep),m.get('fullName')))
                                else:
                                    if resource.get('messageType') != dep:
                                        _list_of_avail_messages.append(('{} [{}]'.format(dep.split('.')[-1],dep),dep))
                                    
                        # Adding own package messages
                        for m in _pkg.messages:

                            if m.full_name != resource.get('messageType') and m.full_name != _field_msg_name:
                                _list_of_avail_messages.append(('{} [{}]'.format(m.name,_pkg.package),m.full_name))

                        if len(_list_of_avail_messages) > 0 :
                            message_type = inquirer.prompt([inquirer.List('message_type','Choose message type',_list_of_avail_messages)],theme=WebezyTheme())
                            if message_type is not None:
                                for f in _msg.get('fields'):
                                    if f.get('fullName') == resource.get('fullName'):
                                        f['messageType'] = message_type['message_type']
                                        print_success("Changing message type for {} -> {}".format(f.get('fullName'),f['messageType']))
                                    architect.EditMessage(_pkg, _msg.get('name'),
                                        _msg.get('fields'), _msg.get('description'), _msg.get('extensionType'),extensions=_msg.get('extensions'))
                                    if no_save==False:
                                        architect.Save()
                            # Handling user cancellation
                            else:
                                print_error('Must choose a valid message type to change field')
                                exit(1)
                        # Handling no available messages
                        else:
                            print_error("Canot find any available messages to change field {} [message_type] into".format(resource.get('fullName')))
                    # Handling package not found - SHOULD NOT HAPPEN !
                    else:
                        print_error("Pakcgae {} is not found !".format(_pkg_name))
            # Handling message not found - SHOULD NOT HAPPEN !
            else:
                print_error("Getting message {} has failed !".format('.'.join(resource.get('fullName').split('.')[:-1])))
                exit(1)

        # Changing enum_type if field type is TYPE_ENUM
        elif sub_actions[0] == 'enum_type':
            # Getting message dict
            _msg = wz_json.get_message('.'.join(resource.get('fullName').split('.')[:-1]))
            # Getting package descriptor
            _pkg = wz_json.get_package(resource.get('fullName').split('.')[1],False)
            if _msg is not None:
                if len(sub_actions) > 1 :
                    if len(sub_actions[1].split('.')) == 4:
                        # TODO check for dependecy
                        if wz_json.get_enum(sub_actions[1]) is not None:
                            for f in _msg.get('fields'):
                                if f.get('fullName') == resource.get('fullName'):
                                    f['enumType'] = sub_actions[1]
                                    print_success("Changing enum type for {} -> {}".format(f.get('fullName'),f['enumType']))
                            architect.EditMessage(_pkg, _msg.get('name'),
                                _msg.get('fields'), _msg.get('description'), _msg.get('extensionType'))
                            if no_save==False:
                                architect.Save()
                        else:
                            print_error('Message {} not exists under project !'.format(sub_actions[1]))
                            exit(1)
                    else:
                        print_error('Message type {} is not valid !'.format(sub_actions[1]))
                else:
                    _pkg_name = resource.get('fullName').split('.')[1]
                    _list_of_avail_enums = []
                    _field_msg_name = '.'.join(resource.get('fullName').split('.')[:-1])
                    if _pkg is not None:
                        if _pkg.dependencies is not None:
                            # Iterating pakcge dependencies
                            for dep in _pkg.dependencies:
                                if 'google.protobuf' not in dep:
                                    temp_pkg = wz_json.get_package(dep.split('.')[1])
                                    if temp_pkg.get('enums') is not None:
                                        for e in temp_pkg.get('enums'):
                                            if e.get('fullName') != resource.get('enumType'):
                                                _list_of_avail_enums.append(('{} [{}]'.format(e.get('name'),dep),e.get('fullName')))
                                    
                        # Adding own package messages
                        for e in _pkg.enums:

                            if e.full_name != resource.get('enumType') and e.full_name != _field_msg_name:
                                _list_of_avail_enums.append(('{} [{}]'.format(e.name,_pkg.package),e.full_name))

                        if len(_list_of_avail_enums) > 0 :
                            enum_type = inquirer.prompt([inquirer.List('enum_type','Choose enum type',_list_of_avail_enums)],theme=WebezyTheme())
                            if enum_type is not None:
                                for f in _msg.get('fields'):
                                    if f.get('fullName') == resource.get('fullName'):
                                        f['enumType'] = enum_type['enum_type']
                                        print_success("Changing enum type for {} -> {}".format(f.get('fullName'),f['enumType']))
                                    architect.EditMessage(_pkg, _msg.get('name'),
                                        _msg.get('fields'), _msg.get('description'), _msg.get('extensionType'),extensions=_msg.get('extensions'))
                                    if no_save==False:
                                        architect.Save()
                            # Handling user cancellation
                            else:
                                print_error('Must choose a valid message type to change field')
                                exit(1)
                        # Handling no available messages
                        else:
                            print_error("Canot find any available messages to change field {} [message_type] into".format(resource.get('fullName')))
                    # Handling package not found - SHOULD NOT HAPPEN !
                    else:
                        print_error("Pakcgae {} is not found !".format(_pkg_name))
            # Handling message not found - SHOULD NOT HAPPEN !
            else:
                print_error("Getting message {} has failed !".format('.'.join(resource.get('fullName').split('.')[:-1])))
                exit(1)

            print_error("Not supporting editing {}".format(sub_actions))
            exit(1)
        # Changing label type
        elif sub_actions[0] == 'label': 
            # Getting message dict
            msg_name = '.'.join(resource.get('fullName').split('.')[:-1])
            _msg = wz_json.get_message(msg_name)
            # Getting package descriptor
            _pkg = wz_json.get_package(resource.get('fullName').split('.')[1],False)
            if _msg is not None:
                _list_of_avail_labels = [('Optional',protos.LABEL_OPTIONAL),('Repeated',protos.LABEL_REPEATED)]
                label = inquirer.prompt([inquirer.List('label','Choose field label',_list_of_avail_labels)],theme=WebezyTheme())
                if label is not None:
                    label = label['label']
                    for f in _msg.get('fields'):
                        if f.get('fullName') == resource.get('fullName'):
                            f['label'] = protos.WebezyFieldLabel.Name(label)
                            print_success("Changing field label for {} -> {}".format(f.get('fullName'),f['label']))

                    architect.EditMessage(_pkg, _msg.get('name'),
                        _msg.get('fields'), _msg.get('description'), _msg.get('extensionType'),extensions=_msg.get('extensions'))
                    if no_save==False:
                        architect.Save()
                else:
                    print_error('Must choose a label type')
                    exit(1)
            else:
                print_error("Getting message {} has failed !".format('.'.join(resource.get('fullName').split('.')[:-1])))
                exit(1)
        # Changing oneof field
        elif sub_actions[0] == 'oneof_modify':
            
            oneof_sub_action = inquirer.prompt([inquirer.List('oneof_sub_action','Choose an action on oneof fields',[('Modify existing fields','modify_oneof_field'),('Add new fields','add_oneof_field'),('Remove oneof field','remove_oneof_field')])],theme=WebezyTheme())
            if oneof_sub_action is not None:
                if oneof_sub_action['oneof_sub_action'] == 'modify_oneof_field' or oneof_sub_action['oneof_sub_action'] == 'remove_oneof_field':
                    _list_of_avail_oneof_fields = list(map(lambda x: (x.get('name'),x.get('fullName')), resource.get('oneofFields')))
                    oneof_field = inquirer.prompt([inquirer.List('oneof_field','Choose which field to modify',_list_of_avail_oneof_fields)],theme=WebezyTheme())
                    print_note(f'{oneof_field=}')
                    if oneof_field is not None:
                        if oneof_sub_action['oneof_sub_action'] == 'remove_oneof_field':
                            if len(resource.get('oneofFields')) == 1:
                                print_error("Can not remove the last oneof field under {}".format(resource.get('fullName')))
                                exit(1)
                            else:
                                architect.RemoveOneofField(oneof_field['oneof_field'])
                                architect.Save()
                                print_success('Removed {} from oneof fields'.format(resource.get('fullName')))
                        else:
                            # TODO
                            print_error("Not supporting editing {}:{}".format(sub_actions,oneof_sub_action['oneof_sub_action']))
                            exit(1)
                    else:
                        print_error("Aborting process of deletion [one of field]")
                        exit(1)
                    

                # TODO oneof_sub_action['oneof_sub_action'] == 'add_oneof_field':
                else:
                    print_error("Not supporting editing {}:{}".format(sub_actions,oneof_sub_action['oneof_sub_action']))
                    exit(1)
            else:
                print_error('Must choose a oneof field action')
                exit(1)
           
        # Not supporting option
        else:
            print_error("Not supporting editing {}".format(sub_actions))
            exit(1)

def choose_action():
    """A function to choose action for edit command"""

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
    """A function to prompt for sub action"""

    mod = inquirer.prompt([
        inquirer.List('sub_action','Choose a modification',choices=choices)
    ],theme=WebezyTheme())

    if mod is None:
        print_error("Must choose an modification type for editing resource")
        exit(1)

    else:
        return [mod['sub_action']]

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
            if protos.WebezyExtension.Name(msg.extension_type) == 'FieldOptions':
                for f in msg.fields:
                    avail_field_ext.append((f.name,f.full_name))

    avail_enums = []
    for enum in package.enums:
        avail_enums.append((enum.name, enum.full_name))
    for d in package.dependencies:

        if 'google.protobuf' in d:
            # Override to omit the Descriptor package
            if 'Descriptor' not in d:
                ext_msg_pkg = '.'.join(d.split('.')[:-1])
                avail_msgs.append(
                    ('{} [Google]'.format(d.split('.')[-1]), '{0}.{1}'.format(ext_msg_pkg, d.split('.')[-1])))
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
                    if protos.WebezyExtension.Name(m.extension_type) == 'FieldOptions':
                        for f in m.fields:
                            avail_field_ext.append((f.name,f.full_name))
    extend = None
    if resource.get('extensionType') is not None:
        extend=protos.WebezyExtension.Value(resource.get('extensionType'))

    if expand:
        extend = inquirer.prompt([inquirer.Confirm('extend',message='Do you want to extend a message?')],theme=WebezyTheme())
        if extend.get('extend'):
            extend = inquirer.prompt([inquirer.List('extend','Choose message extension',choices=[protos.WebezyExtension.Name(protos.WebezyExtension.FieldOptions),protos.WebezyExtension.Name(protos.WebezyExtension.MessageOptions),protos.WebezyExtension.Name(protos.WebezyExtension.FileOptions),protos.WebezyExtension.Name(protos.WebezyExtension.ServiceOptions)])],theme=WebezyTheme())
            extend=protos.WebezyExtension.Value(extend['extend'])
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

        if field['fieldType'] == protos.WebezyFieldType.Name(protos.WebezyFieldType.TYPE_MESSAGE):
            if len(avail_msgs) == 0:
                print_warning("No messages availabe for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'message', 'Choose available messages', choices=avail_msgs)
                ], theme=WebezyTheme())
                message_type = message['message']

        elif field['fieldType'] == protos.WebezyFieldType.Name(protos.WebezyFieldType.TYPE_ENUM):
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
                        if protos.WebezyFieldType.Name(temp_field.field_type) == 'TYPE_BOOL':
                            f_ext_v = inquirer.prompt([inquirer.Confirm('ext_value','Enter extension bool value',default=False)],theme=WebezyTheme())
                        elif protos.WebezyFieldType.Name(temp_field.field_type) == 'TYPE_DOUBLE' or protos.WebezyFieldType.Name(temp_field.field_type) == 'TYPE_FLOAT':
                            f_ext_v = inquirer.prompt([inquirer.Text('ext_value','Enter extension float value',validate=helpers.float_value_validate)],theme=WebezyTheme())
                            try:
                                f_ext_v = float(f_ext_v['ext_value'])
                            except Exception as e:
                                logging.exception(e)
                                exit(1)
                        elif protos.WebezyFieldType.Name(temp_field.field_type) == 'TYPE_INT32' or protos.WebezyFieldType.Name(temp_field.field_type) == 'TYPE_INT64':
                            f_ext_v = inquirer.prompt([inquirer.Text('ext_value','Enter extension integer value',validate=helpers.int_value_validate)],theme=WebezyTheme())
                            try:
                                f_ext_v = int(f_ext_v['ext_value'])
                            except Exception as e:
                                logging.exception(e)
                                exit(1)
                        elif protos.WebezyFieldType.Name(temp_field.field_type) == 'TYPE_STRING':
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
    architect.EditMessage(package=package, name=resource.get('name'),
                            fields=msg_fields, description=description, options=extend,extensions=resource.get('extensions'))
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

        if field['fieldType'] == resources.WebezyFieldType.Name(resources.WebezyFieldType.TYPE_MESSAGE):
            if len(avail_msgs) == 0:
                print_warning("[ONEOF] No messages availabe for field")
                exit(1)
            else:
                message = inquirer.prompt([
                    inquirer.List(
                        'message', '[ONEOF] Choose available messages', choices=avail_msgs)
                ], theme=WebezyTheme())
                message_type = message['message']

        elif field['fieldType'] == resources.WebezyFieldType.Name(resources.WebezyFieldType.TYPE_ENUM):
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
    """A function for getting a resource dependencies"""

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
        if wz_json.packages is not None:
            for p in wz_json.packages:
                pkg = wz_json.packages[p]

                if pkg.get('dependencies'):
                    if pkg_name in pkg.get('dependencies'):
                        for m in pkg.get('messages'):
                            if len(m.get('fields')) > 1:
                                for f in m.get('fields'):
                                    if f.get('messageType'):
                                        if full_name in f.get('messageType'):
                                            dependent_resources.append(f)
                                    if f.get('enumType'):
                                        if full_name in f.get('enumType'):
                                            dependent_resources.append(f)
                            else:
                                if next((f for f in m.get('fields') if f.get('messageType') == full_name),None) is not None:
                                    dependent_resources.append(m)
                                elif next((f for f in m.get('fields') if f.get('enumType') == full_name),None) is not None:
                                    dependent_resources.append(m)
                                    
                                    
                    
                if pkg_name == pkg.get('package'):
                    for m in pkg.get('messages'):
                        if len(m.get('fields')) > 1:
                            for f in m.get('fields'):
                                if f.get('messageType'):
                                    if full_name in f.get('messageType'):
                                        dependent_resources.append(f)
                                if f.get('enumType'):
                                    if full_name in f.get('enumType'):
                                        dependent_resources.append(f)
                        else:
                            if next((f for f in m.get('fields') if f.get('messageType') == full_name),None) is not None:
                                dependent_resources.append(m)
                            elif next((f for f in m.get('fields') if f.get('enumType') == full_name),None) is not None:
                                dependent_resources.append(m) 


        if wz_json.services is not None:
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
    

def display_dependencies(dependencies,resource,action):
    """Display the depndencies for the specified resources"""

    if len(dependencies) > 0:
        print_warning("The following resources are going to be affected from {0} {1}:\n".format(action,resource.get('fullName')))
        for d in dependencies:
            if d.get('name') is not None:
                print_warning('- {0} [{1}]'.format(d.get('name'),d.get('kind')))
            else:
                for k in d:
                    depend = (k,d[k])

                print_warning('- {0} -> {1} [{2}]'.format(depend[0],depend[1].get('name'),depend[1].get('kind')))
    print('')


def rename_message(resource,wz_json:helpers.WZJson,architect:WebezyArchitect,dependencies):
    """A function to rename the message"""

    message_name = inquirer.prompt([inquirer.Text('message_name','Enter new name for the message',validate=message_name_validation)],theme=WebezyTheme())
    if message_name is None:
        print_warning("Exiting editing process for message {}".format(resource.get('fullName')))
        exit(1)
    else:
        message_name = message_name['message_name']
    
    _pkg = wz_json.get_package(resource.get('fullName').split('.')[1],False)
    new_full_name = '{}.{}'.format('.'.join(resource.get('fullName').split('.')[:-1]),message_name)

   

    if next((msg for msg in _pkg.messages if msg.name == message_name),None) is None:
        print_success("Renaming {} -> {}".format(resource.get('fullName'),new_full_name))
        # Handling all dependencies and rename the type as well
        for d in dependencies:
            if d.get('kind') == resources.ResourceKinds.field.value:
                edit_field(d,'modify',['message_type',new_full_name],wz_json,architect,False,True)

        old_name = resource['name']
        resource['name'] = message_name
        resource['fullName'] = new_full_name
        architect.EditMessage(_pkg, resource.get('name'),
                            resource.get('fields'), resource.get('description'), resource.get('extensionType'),old_name=old_name,extensions=resource.get('extensions'))
        architect.Save()
    else:
        print_error("{} is already existing under {} package !".format(message_name,resource.get('fullName').split('.')[1]))
        exit(1)
    

    

def message_name_validation(answers, current):
    """Validate renaming of messages"""

    if len(current) == 0:
        raise inquirerErrors.ValidationError(
            current, reason='Resource name must not be blank')
    if len(re.findall('\s', current)) > 0:
        raise inquirerErrors.ValidationError(
            current, reason='Resource name must not include blank spaces')
    if len(re.findall('-', current)) > 0:
        raise inquirerErrors.ValidationError(
            current, reason='Resource name must not include hyphens, underscores are allowed')
    return True