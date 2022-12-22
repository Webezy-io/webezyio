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
import os
import sys
from typing import List
from enum import Enum

import grpc
from google.protobuf.descriptor_pool import DescriptorPool
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.descriptor import Descriptor
from google.protobuf.descriptor_pb2 import DescriptorProto, FieldDescriptorProto
from google.protobuf.descriptor import FileDescriptor, Descriptor, MethodDescriptor,\
    FieldDescriptor, ServiceDescriptor, EnumDescriptor
from grpc_tools import command
from webezyio.cli import prompter
from webezyio.commons import errors
from webezyio.commons.pretty import print_error, print_info, print_note, print_warning
from webezyio.commons.protos.WebezyPackage_pb2 import UNKNOWN_WEBEZYEXTENSION, WebezyExtension, WebezyField, WebezyOneOfField

from webezyio.commons.protos import WebezyJson, \
    WebezyProject, \
    WebezyService, \
    WebezyPackage, \
    WebezyConfig, \
    WebezyEnumValue, \
    WebezyServer, \
    WebezyClient, \
    WebezyMethod, \
    WebezyMessage, \
    WebezyEnum, \
    WebezyFieldType, \
    WebezyFieldLabel, \
    python, typescript, go, webpack, javascript, csharp, java, \
    WebezyLanguage, \
    UNKNOWN_WEBEZYEXTENSION, \
    google_dot_protobuf_dot_struct__pb2

class ResourceTypes(Enum):
    project = 'projects'
    service = 'services'
    package = 'packages'
    files = 'files'
    server = 'servers'
    client = 'clients'
    descriptor = 'descriptors'


class ResourceKinds(Enum):
    ezy_1 = 'Webezy.project/tier1'
    service_srvr_js = 'Webezy.service/server/javascript'
    service_client_js = 'Webezy.service/client/javascript'
    service_srvr_ts = 'Webezy.service/server/typescript'
    service_client_ts = 'Webezy.service/client/typescript'
    service_srvr_py = 'Webezy.service/server/python'
    service_client_py = 'Webezy.service/client/python'
    service_srvr_cs = 'Webezy.service/server/csharp'
    service_client_cs = 'Webezy.service/client/csharp'
    service_srvr_cpp = 'Webezy.service/server/cpp'
    service_client_cpp = 'Webezy.service/client/cpp'
    service_srvr_java = 'Webezy.service/server/java'
    service_client_java = 'Webezy.service/client/java'
    service_client_webpack = 'Webezy.service/client/webpack'
    file_proto = 'Webezy.file/proto'
    file_js = 'Webezy.file/javascript'
    file_ts = 'Webezy.file/typescript'
    file_py = 'Webezy.file/python'
    file_cs = 'Webezy.file/csharp'
    file_go = 'Webezy.file/go'
    file_cpp = 'Webezy.file/cpp'
    file_java = 'Webezy.file/java'
    file_webpack = 'Webezy.file/webpack'
    method = 'Webezy.descriptor/method'
    field = 'Webezy.descriptor/field'
    oneof_field = 'Webezy.descriptor/oneof_field'
    message = 'Webezy.descriptor/message'
    enum = 'Webezy.descriptor/enum'
    enum_value = 'Webezy.descriptor/enum_value'
    health = 'Webezy.health/check'


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
    WebezyFieldLabel.Name(WebezyFieldLabel.LABEL_REPEATED)
]

def get_blank_webezy_json(json=False):
    webezyJson = WebezyJson(domain='domain', project=WebezyProject(), services={},
                            packages={}, config=WebezyConfig())
    return webezyJson if json == False else MessageToDict(webezyJson)


def generate_project(path, name, server_langauge='python', clients=[], package_name=None, json=False):
    path = path.split('/webezy.json')[0]
    # Init server
    if server_langauge == 'python':
        temp_langugae = python
    elif server_langauge == 'typescript':
        temp_langugae = typescript
    elif server_langauge == 'go':
        temp_langugae = go
    # Add more language support here...
    else:
        raise errors.WebezyValidationError('Server Language Error','Must pass a valid server language for your new project')
    server = WebezyServer(language=WebezyLanguage.Name(temp_langugae))
    
    # Creating packaeg name for project
    if package_name is None:
        package_name = name.replace('-', '').replace('_', '').lower()

    # Parse clients languages
    go_package = None
    temp_clients = []
    if len(clients) > 0:
        for c in clients:
            if c['language'] == 'python':
                temp_c_lang = python
            elif c['language'] == 'typescript':
                temp_c_lang = typescript
            elif c['language'] == 'go':
                temp_c_lang = go
                if json:
                    go_package_input = prompter.QText(name='go_package',message='Enter a prefix to support Go package',default='github.com')
                    go_package = prompter.ask_user_question(questions=[go_package_input])
                if go_package is not None:
                    go_package = '{}/{}'.format(go_package['go_package'],package_name)
                else:
                    go_package = 'github.com/{}'.format(package_name)
            elif c['language'] == 'webpack':
                temp_c_lang = webpack
            # TODO Add more client supported languages
            else:
                raise errors.WebezyValidationError('Client Language Error','Client {} is not supported'.format(c['language']))
            client = WebezyClient(out_dir=get_uri_client(
                path, c['language']), language=WebezyLanguage.Name(temp_c_lang))
            temp_clients.append(client)
    # Default client
    else:
        client = WebezyClient(out_dir=get_uri_client(
            path, 'python'), language='python')
        temp_clients.append(client)
  
    # Init project
    project = WebezyProject(uri=get_uri_project(path, name), name=name, package_name=package_name,
                      version='0.0.1', type=ResourceTypes.project.value, kind=ResourceKinds.ezy_1.value,
                      server=server, clients=temp_clients,go_package=go_package)
    # Return project as message or dict
    return project if json == False else MessageToDict(project)

 
def generate_service(path, domain, name, service_language, dependencies, description=None,methods=[],extensions=None, json=False):
    path = path.split('/webezy.json')[0]
    # Init service
    temp_methods = []
    if methods:
        for m in methods:
            temp_methods.append(ParseDict(m,WebezyMethod()))
    service = WebezyService(uri=get_uri_service(path, name, service_language.lower()),
                                  name=name, full_name=get_service_full_name(domain, name), dependencies=dependencies,
                                  methods=temp_methods,
                                  description=description,
                                  type= ResourceTypes.service.value,
                                  version='0.0.1',
                                  extensions=extensions)
    # Init methods
    # service.methods = dependencies

    # Init dependencies
    # dependencies = []
    # service.dependencies = dependencies
    return service if json == False else MessageToDict(service)


def generate_package(path, domain, name, dependencies=[],messages=[],enums=[],description=None,extensions=None, json=False,wz_json=None):
    path = path.split('/webezy.json')[0]
    temp_msgs = []
    temp_enums = []
    for m in messages:
        temp_msgs.append(ParseDict(m,WebezyMessage()))
    if enums is not None:
        for e in enums:
            temp_enums.append(ParseDict(e,WebezyEnum()))
 
    full_name = get_package_full_name(domain, name)
    temp_ext = None
    if extensions is not None:
        temp_ext = {}
        for ext in extensions:
            if '.'.join(ext.split('.')[:3]) not in dependencies and '.'.join(ext.split('.')[:3]) != full_name:
                depend_name = '.'.join(ext.split('.')[:3])
                print_warning("Adding depndency {}".format(depend_name))
                dependencies.append(depend_name)
            if wz_json is not None:
                pkg_path = 'protos/{}/{}.proto'.format(ext.split('.')[2],ext.split('.')[1])
                if  wz_json.get('packages'):
                    ext_package = wz_json.get('packages').get(pkg_path)
                    ext_msg = next((m for m in ext_package.get('messages') if m.get('fullName') == '.'.join(ext.split('.')[:-1])),None)
                    if ext_msg is not None:
                        ext_field = next((f_ext for f_ext in ext_msg.get('fields') if f_ext.get('fullName') == ext),None)
                        if ext_field is not None:
                            temp_ext = parse_proto_extension(ext_field.get('fieldType'),ext_field.get('label'),ext_field,extensions[ext],temp_ext,wz_json=wz_json)
            else:
                print_error("Cannot parse extension value without context to webezy.json file !")
                exit(1)

    package = WebezyPackage(uri=get_uri_package(
        path, full_name),type= ResourceTypes.package.value, name=name, package=full_name, version='0.0.1', dependencies=dependencies, messages=temp_msgs,enums=temp_enums,description=description,extensions=temp_ext)

    return package if json == False else MessageToDict(package)


def generate_message(path, domain, package, name, fields=[], option=UNKNOWN_WEBEZYEXTENSION, description=None,extensions=None, json=False,wz_json=None):
    path = path.split('/webezy.json')[0]
    temp_fields = []
    msg_fName = get_message_full_name(domain, package.name, name)
    msg_uri = get_uri_message(path, msg_fName)
    if option is None:
        option = UNKNOWN_WEBEZYEXTENSION
    else:
        if 'google.protobuf.Descriptor' not in package.dependencies:
            package.dependencies.append('google.protobuf.Descriptor')
    index = 0 if option == UNKNOWN_WEBEZYEXTENSION else 55555
    for f in fields:
        if next((n for n in temp_fields if n.name == f.get('name')), None) is None:
            index += 1
            f_fName = get_field_full_name(
                domain, package.name, name, f.get('name'))
            msg_type = None
            msg_type_temp  = f.get('message_type') if f.get('message_type') is not None else f.get('messageType')
            if msg_type_temp is not None:
                package_name = '.'.join(msg_type_temp.split('.')[:3])
                if package_name not in package.dependencies and package.package not in msg_type_temp:
                    package.dependencies.append(package_name)
                if 'google.protobuf' in msg_type_temp:
                    msg_type = '{0}.{1}.{2}'.format(msg_type_temp.split('.')[0],msg_type_temp.split('.')[1],msg_type_temp.split('.')[-1].capitalize()) if msg_type_temp is not None else None
                else:
                    msg_type = msg_type_temp
            f_uri = get_uri_field(path, f_fName)
            fields_oneof = []
            oneofs_fields = f.get('oneof_fields') if f.get('oneof_fields')  is not None else f.get('oneofFields') 
            if oneofs_fields :
                for f_oneof in oneofs_fields:
                    f_oneof_full_name = get_oneof_field_full_name(domain=domain,package=package.name,message=name,parent_field=f.get('name'),name=f_oneof.get('name'))
                    f_oneof_uri = get_uri_oneof_field(path, f_oneof_full_name)
                    fields_oneof.append(WebezyOneOfField(uri=f_oneof_uri,
                        name=f_oneof.get('name'),
                        full_name=f_oneof_full_name,
                        description=f_oneof.get('description'),
                        index=index,
                        field_type=f_oneof.get('fieldType') if f_oneof.get('fieldType') is not None else f_oneof.get('field_type'),
                        enum_type=f_oneof.get('enumType') if f_oneof.get('enumType') is not None else f_oneof.get('enum_type'),
                        type=ResourceTypes.descriptor.value,
                        kind=ResourceKinds.oneof_field.value,
                        message_type=f_oneof.get('messageType')  if f_oneof.get('messageType') is not None else f_oneof.get('message_type')))
                    index += 1
            temp_ext = None
            if f.get('extensions') is not None:
                temp_ext = {}
                for ext in f.get('extensions'):
                    if '.'.join(ext.split('.')[:3]) not in package.dependencies:
                        depend_name = '.'.join(ext.split('.')[:3])
                        print_warning("Adding depndency {}".format(depend_name))
                        package.dependencies.append(depend_name)

                    if wz_json is not None:
                        pkg_path = 'protos/{}/{}.proto'.format(ext.split('.')[2],ext.split('.')[1])
                        if  wz_json.get('packages'):
                            ext_package = wz_json.get('packages').get(pkg_path)
                            ext_msg = next((m for m in ext_package.get('messages') if m.get('fullName') == '.'.join(ext.split('.')[:-1])),None)
                            if ext_msg is not None:
                                ext_field = next((f_ext for f_ext in ext_msg.get('fields') if f_ext.get('fullName') == ext),None)
                                if ext_field is not None:
                                    temp_ext = parse_proto_extension(ext_field.get('fieldType'),ext_field.get('label'),ext_field,f.get('extensions')[ext],temp_ext,wz_json=wz_json)
                    else:
                        print_error("Cannot parse extension value without context to webezy.json file !")
                        exit(1)
                    
            temp_fields.append(WebezyField(uri=f_uri, name=f.get('name'), full_name=f_fName,
                                                 description=f.get(
                                                     'description'),
                                                 index=index, field_type=f.get(
                                                     'field_type') if f.get(
                                                     'field_type') is not None else f.get(
                                                     'fieldType'),
                                                 label=f.get('label'),
                                                 enum_type=f.get('enum_type') if f.get('enum_type') is not None else f.get('enumType'),
                                                 type=ResourceTypes.descriptor.value,
                                                 kind=ResourceKinds.field.value,
                                                 message_type=msg_type,
                                                 extensions=temp_ext,
                                                 key_type=f.get('key_type') if f.get('key_type') is not None else f.get('keyType'),
                                                 value_type=f.get('value_type') if f.get('value_type') is not None else f.get('valueType'),
                                                 oneof_fields=fields_oneof))
        else:
            logging.warning(
                f"Cannot insert field {f.get('name')} already exists under {name} message")
    
    temp_ext = None
    if extensions is not None:
        temp_ext = {}
        for ext in extensions:
            if '.'.join(ext.split('.')[:3]) not in package.dependencies and '.'.join(ext.split('.')[:3]) != package.package:
                depend_name = '.'.join(ext.split('.')[:3])
                print_warning("Adding depndency {}".format(depend_name))
                package.dependencies.append(depend_name)
            if wz_json is not None:
                pkg_path = 'protos/{}/{}.proto'.format(ext.split('.')[2],ext.split('.')[1])
                if  wz_json.get('packages'):
                    ext_package = wz_json.get('packages').get(pkg_path)
                    ext_msg = next((m for m in ext_package.get('messages') if m.get('fullName') == '.'.join(ext.split('.')[:-1])),None)
                    if ext_msg is not None:
                        ext_field = next((f_ext for f_ext in ext_msg.get('fields') if f_ext.get('fullName') == ext),None)
                        if ext_field is not None:
                            temp_ext = parse_proto_extension(ext_field.get('fieldType'),ext_field.get('label'),ext_field,extensions[ext],temp_ext,wz_json=wz_json)
            else:
                print_error("Cannot parse extension value without context to webezy.json file !")
                exit(1)
    msg = WebezyMessage(uri=msg_uri, name=name, full_name=msg_fName, fields=temp_fields, type=ResourceTypes.descriptor.value,extensions=temp_ext,
                       kind=ResourceKinds.message.value, extension_type=WebezyExtension.Name(option) if isinstance(option,int) else option, description=description)
    return msg if json == False else MessageToDict(msg)


def generate_enum(path, domain, package, name, enum_values, json=False,description=None):
    path = path.split('/webezy.json')[0]

    e_fName = get_enum_full_name(domain, package, name)
    e_uri = get_uri_enum(path, e_fName)
    temp_values = []
    index = 0
    for ev in enum_values:
        ev_fName = get_enum_value_full_name(
            domain, package, name, ev.get('name'))
        ev_uri = get_uri_enum_value(path, ev_fName)
        temp_values.append(WebezyEnumValue(uri=ev_uri, name=ev.get(
            'name'), number=ev.get('number'), index=index,type=ResourceTypes.descriptor.value,kind=ResourceKinds.enum_value.value,description=ev.get('description')))
        index = + 1

    ENUM = WebezyEnum(uri=e_uri, name=name,type=ResourceTypes.descriptor.value,kind=ResourceKinds.enum.value,
                            full_name=e_fName, values=temp_values,description=description)
    return ENUM if json == False else MessageToDict(ENUM)


def generate_rpc(path, name, client_streaming, server_streaming, in_type, out_type, description=None, json=False):
    path = path.split('/webezy.json')[0]
    RPC = WebezyMethod(uri=get_uri_rpc(path, name), name=name, full_name=get_method_full_name(name), type=ResourceTypes.descriptor.value, kind=ResourceKinds.method.value,
                             input_type=in_type, output_type=out_type, client_streaming=client_streaming, server_streaming=server_streaming, description=description)
    return RPC if json == False else MessageToDict(RPC)


def parse_proto(proto_path) -> FileDescriptor:
    print_note(f"Parsing proto file into python module -> {proto_path}")
    # command.build_package_protos(proto_path)
    # os.chdir(os.getcwd()+'/protos')
    try:
        sys.path.index(os.getcwd()+'/protos')
    except:
        sys.path.append(os.getcwd()+'/protos')

    proto = grpc.protos_and_services(proto_path)
    return proto


def parse_pool(pool) -> DescriptorPool:
    return pool


def parse_message(message_by_names, name) -> Descriptor:
    return message_by_names[name]


def parse_method(message_by_names, name) -> MethodDescriptor:
    return message_by_names[name]


def parse_field(fields_by_name, name) -> FieldDescriptor:
    return fields_by_name[name]


def parse_service(service) -> ServiceDescriptor:
    return service


def parse_enum(enums_by_name, name) -> EnumDescriptor:
    return enums_by_name[name]


def list_fields(fields) -> List[FieldDescriptor]:
    return fields


def find_message(full_name: str, pool: DescriptorPool) -> Descriptor:
    return pool.FindMessageTypeByName(full_name=full_name)


def find_method(full_name: str, pool: DescriptorPool) -> MethodDescriptor:
    return pool.FindMethodByName(full_name)


def find_enum(full_name: str, pool: DescriptorPool) -> EnumDescriptor:
    return pool.FindEnumTypeByName(full_name)


def find_field(full_name: str, pool: DescriptorPool) -> FieldDescriptor:
    return pool.FindFieldByName(full_name)


def find_file(file_name: str, pool: DescriptorPool) -> FileDescriptor:
    return pool.FindFileByName(file_name)


def get_uri_project(path, name):
    return construct_uri(path, ResourceTypes.project, ResourceKinds.ezy_1, name)


def get_uri_client(path, language):
    uri = 'unknown'
    if language == 'python':
        uri = construct_uri(path, ResourceTypes.client, ResourceKinds.file_py)
    elif language == 'typescript':
        uri = construct_uri(path, ResourceTypes.client, ResourceKinds.file_ts)
    elif language == 'go':
        uri = construct_uri(path, ResourceTypes.client, ResourceKinds.file_go)
    elif language == 'webpack':
        uri = construct_uri(path, ResourceTypes.client, ResourceKinds.file_webpack)
    else:
        raise errors.WebezyValidationError('Client Not Supported','Client of type {} is not supported yet !'.format(language))
    return uri


def get_uri_service(path, name, language):
    kind = None
    if language == 'python':
        kind = ResourceKinds.service_srvr_py
    elif language == 'typescript':
        kind = ResourceKinds.service_srvr_ts

    return construct_uri(path, ResourceTypes.service, kind, name)


def get_uri_rpc(path, name):
    return construct_uri(path, ResourceTypes.descriptor, ResourceKinds.method, name)


def get_uri_package(path, full_name):
    return construct_uri(path, ResourceTypes.package, ResourceKinds.file_proto, full_name)


def get_uri_message(path, full_name):
    return construct_uri(path, ResourceTypes.descriptor, ResourceKinds.message, full_name)


def get_uri_enum(path, full_name):
    return construct_uri(path, ResourceTypes.descriptor, ResourceKinds.enum, full_name)


def get_uri_enum_value(path, full_name):
    return construct_uri(path, ResourceTypes.descriptor, ResourceKinds.enum_value, full_name)


def get_uri_field(path, full_name):
    return construct_uri(path, ResourceTypes.descriptor, ResourceKinds.field, full_name)

def get_uri_oneof_field(path, full_name):
    return construct_uri(path, ResourceTypes.descriptor, ResourceKinds.oneof_field, full_name)

def construct_uri(path, resource_type: ResourceTypes, resource_kind: ResourceKinds, full_name=None):
    uri = 'unknown'
    # Project
    if resource_type == ResourceTypes.project:
        uri = f'{path}'
    # Client
    elif resource_type == ResourceTypes.client:
        client_kind = resource_kind.value.split('/')[-1]
        uri = f'{path}/{ResourceTypes.client.value}/{client_kind}'
    # Server
    elif resource_type == ResourceTypes.server:
        pass
    # Service
    elif resource_type == ResourceTypes.service:
        uri = f'{path}/protos/{full_name}.proto'
    # Package
    elif resource_type == ResourceTypes.package:
        uri = f'{path}/{resource_type.value}/{full_name}'
    # Descriptors
    elif resource_type == ResourceTypes.descriptor:
        # Method
        if resource_kind == ResourceKinds.method:
            uri = f'{path}/methods/{full_name}'
        # Message
        elif resource_kind == ResourceKinds.message:
            uri = f'{path}/messages/{full_name}'
        # Enum
        elif resource_kind == ResourceKinds.enum:
            uri = f'{path}/enums/{full_name}'
        # Enum
        elif resource_kind == ResourceKinds.enum_value:
            uri = f'{path}/enums/{full_name}'
        # Field
        elif resource_kind == ResourceKinds.field:
            uri = f'{path}/fields/{full_name}'
        # Oneof Field
        elif resource_kind == ResourceKinds.oneof_field:
            uri = f'{path}/oneof_field/{full_name}'

    return uri


def get_service_full_name(domain, name):
    return construct_full_name(ResourceTypes.service, ResourceKinds.file_proto, domain, name=name)


def get_package_full_name(domain, name):
    return construct_full_name(ResourceTypes.package, ResourceKinds.file_proto, domain, name=name)


def get_method_full_name(name):
    pass


def get_message_full_name(domain, package, name):
    return construct_full_name(ResourceTypes.descriptor, ResourceKinds.message, domain, parent_name=package, name=name)

def get_field_full_name(domain, package, message, name):
    return construct_full_name(ResourceTypes.descriptor, ResourceKinds.field, domain, parent_name=[package, message], name=name)

def get_oneof_field_full_name(domain, package, message,parent_field, name):
    return construct_full_name(ResourceTypes.descriptor, ResourceKinds.oneof_field, domain, parent_name=[package, message, parent_field], name=name)

def get_enum_full_name(domain, package, enum):
    return construct_full_name(ResourceTypes.descriptor, ResourceKinds.enum, domain, parent_name=package, name=enum)


def get_enum_value_full_name(domain, package, enum, name):
    return construct_full_name(ResourceTypes.descriptor, ResourceKinds.enum_value, domain, parent_name=[package, enum], name=name)


def construct_full_name(resource_type: ResourceTypes, resource_kind: ResourceKinds, domain=None, parent_name=None, name=None, version='v1'):
    full_name = 'unknown'
    # Service
    if resource_type == ResourceTypes.service:
        full_name = f'{domain}.{name}.{version}'
    # Package
    elif resource_type == ResourceTypes.package:
        full_name = f'{domain}.{name}.{version}'
    # Descriptors
    elif resource_type == ResourceTypes.descriptor:
        # Method
        if resource_kind == ResourceKinds.method:
            full_name = f'{domain}.{parent_name}.{version}.{name}'
        # Message
        elif resource_kind == ResourceKinds.message:
            full_name = f'{domain}.{parent_name}.{version}.{name}'
        # Enum
        elif resource_kind == ResourceKinds.enum:
            full_name = f'{domain}.{parent_name}.{version}.{name}'
         # EnumValue
        elif resource_kind == ResourceKinds.enum_value:
            full_name = f'{domain}.{parent_name[0]}.{version}.{parent_name[1]}.{name}'
        # Field
        elif resource_kind == ResourceKinds.field:
            full_name = f'{domain}.{parent_name[0]}.{version}.{parent_name[1]}.{name}'
        # Oneof Field
        elif resource_kind == ResourceKinds.oneof_field:
            full_name = f'{domain}.{parent_name[0]}.{version}.{parent_name[1]}.{parent_name[2]}.{name}'

    return full_name


def proto_to_dict(proto):
    return MessageToDict(proto)

def parse_proto_extension(field_opt_type,field_opt_label,description,value,field_extensions,wz_json):
    if 'REPEATED' in field_opt_label:
        list_values_temp = []
        for field_opt_value in value:
            if 'BOOL' in field_opt_type:
                list_values_temp.append( google_dot_protobuf_dot_struct__pb2.Value(bool_value=field_opt_value))
            elif 'STRING' in field_opt_type:
                list_values_temp.append( google_dot_protobuf_dot_struct__pb2.Value(string_value=field_opt_value))
            elif 'INT' in field_opt_type:
                list_values_temp.append( google_dot_protobuf_dot_struct__pb2.Value(number_value=field_opt_value))
            elif 'MESSAGE' in field_opt_type:
                struct_temp = google_dot_protobuf_dot_struct__pb2.Struct()
                ext_package_path = 'protos/{}/{}.proto'.format(description.get('fullName').split('.')[2],description.get('fullName').split('.')[1])
                message_type = next((m for m in wz_json.get('packages').get(ext_package_path).get('messages') if m.get('fullName') == '.'.join(description.get('fullName').split('.')[:-1])),None)
                for field_ext_temp in message_type.get('fields'):
                    if field_ext_temp.get('fieldType') == 'TYPE_MESSAGE' or field_ext_temp.get('fieldType') == 'TYPE_MAP' or field_ext_temp.get('fieldType') == 'TYPE_ENUM':
                        raise errors.WebezyValidationError('Extension values parse error','There are too many nested levels for {}'.format(field_ext_temp.full_name))
                    struct_temp.update({field_ext_temp.get('name'):getattr(field_opt_value,field_ext_temp.get('name'))})
                list_values_temp.append(google_dot_protobuf_dot_struct__pb2.Value(struct_value=struct_temp))
            elif 'ENUM' in field_opt_type:
                ext_package_path = 'protos/{}/{}.proto'.format(description.get('fullName').split('.')[2],description.get('fullName').split('.')[1])
                enum_type = next((e for e in wz_json.get('packages').get(ext_package_path).get('enums') if e.get('fullName') == '.'.join(description.get('fullName').split('.')[:-1])),None)
                enum_value = next((ev for ev in enum_type.get('values') if ev.get('number') == field_opt_value),None)
                list_values_temp.append(google_dot_protobuf_dot_struct__pb2.Value(string_value=enum_value.get('name')))
            else:
                print_warning("Not supporting field type [{0}] for field extensions {1}".format(field_opt_type,description.get('fullName')))

        list_values = google_dot_protobuf_dot_struct__pb2.ListValue(values=list_values_temp)
        field_extensions[description.get('fullName')] = google_dot_protobuf_dot_struct__pb2.Value(list_value=list_values)
    else:
        if 'BOOL' in field_opt_type:
            if hasattr(value,'bool_value'):
                value = value.bool_value
            field_extensions[description.get('fullName')] = google_dot_protobuf_dot_struct__pb2.Value(bool_value=value)
        elif 'STRING' in field_opt_type:
            if hasattr(value,'string_value'):
                value = value.string_value
            field_extensions[description.get('fullName')] = google_dot_protobuf_dot_struct__pb2.Value(string_value=getattr(value,'string_value') if hasattr(value,'string_value') != False else value)
        elif 'INT' in field_opt_type or 'FLOAT' in field_opt_type  or 'DOUBLE' in field_opt_type:
            if hasattr(value,'number_value'):
                value = value.number_value
            field_extensions[description.get('fullName')] = google_dot_protobuf_dot_struct__pb2.Value(number_value=value)
        elif 'MESSAGE' in field_opt_type:

                struct_temp = google_dot_protobuf_dot_struct__pb2.Struct()
                ext_package_path = 'protos/{}/{}.proto'.format(description.get('messageType').split('.')[2],description.get('messageType').split('.')[1])

                message_type = next((m for m in wz_json.get('packages').get(ext_package_path).get('messages') if m.get('fullName') == description.get('messageType')),None)
                temp_dict = {}
                
                for field_ext_temp in message_type.get('fields'):

                    if field_ext_temp.get('fieldType') == 'TYPE_MESSAGE' or field_ext_temp.get('fieldType') == 'TYPE_MAP' or field_ext_temp.get('fieldType') == 'TYPE_ENUM':
                        raise errors.WebezyValidationError('Extension values parse error','There are too many nested levels for {}'.format(field_ext_temp.full_name))
                    try:
                        if isinstance(value,dict):
                            temp_value = value.get(field_ext_temp.get('name'))
                        else:
                            temp_value = getattr(value,field_ext_temp.get('name'))
                        temp_dict[field_ext_temp.get('name')] = temp_value
                        # struct_temp.update({:temp_value})
                    except AttributeError:
                        if hasattr(value,'struct_value'):
                            f = field_ext_temp.get('name')
                            if 'BOOL' in field_ext_temp.get('fieldType'):
                                temp_dict[field_ext_temp.get('name')]= value.struct_value.fields[f].bool_value
                            elif 'INT' in field_ext_temp.get('fieldType') or 'FLOAT' in field_ext_temp.get('fieldType') or 'DOUBLE' in field_ext_temp.get('fieldType'):
                                temp_dict[field_ext_temp.get('name')] = value.struct_value.fields[f].number_value
                            elif 'STRING' in field_ext_temp.get('fieldType'):
                                temp_dict[field_ext_temp.get('name')] = value.struct_value.fields[f].string_value
                                # struct_temp.update({field_ext_temp.get('name'):value.struct_value.fields[f].string_value})
                            
                            # TODO handle enum type for nested object field
                    except Exception as e:
                        print_info(e)

                struct_temp.update(temp_dict)
                field_extensions[description.get('fullName')] = google_dot_protobuf_dot_struct__pb2.Value(struct_value=struct_temp)
        elif 'ENUM' in field_opt_type:
            ext_package_path = 'protos/{}/{}.proto'.format(description.get('fullName').split('.')[2],description.get('fullName').split('.')[1])
            enum_type = next((e for e in wz_json.get('packages').get(ext_package_path).get('enums') if e.get('fullName') == '.'.join(description.get('fullName').split('.')[:-1])),None)
            enum_value = next((ev for ev in enum_type.get('values') if ev.get('number') == field_opt_value),None)
            field_extensions[description.get('fullName')] = google_dot_protobuf_dot_struct__pb2.Value(string_value=enum_value.get('name'))
        else:
            print_warning("Not supporting field type [{0}] for field extensions {1}".format(field_opt_type,description.get('fullName')))
    
    return field_extensions

def add_field_to_message():
    pass