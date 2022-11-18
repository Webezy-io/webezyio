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
from pathlib import Path
import sys
from typing import Dict, List, Literal
from webezyio.architect import WebezyArchitect
import webezyio.builder as builder
from webezyio.commons import helpers, file_system, resources, errors
from webezyio.commons.pretty import print_error, print_info, print_note, print_success, print_warning
from webezyio.commons.protos.webezy_pb2 import Descriptor, Language, Project, ServiceDescriptor, WebezyClient, WebezyDeploymentType, WebezyServer, WzResourceWrapper,google_dot_protobuf_dot_struct__pb2


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Finished webezyio build process %s plugin" % (__name__))


_WELL_KNOWN_LANGUAGED = Literal["python", "typescript"]


@builder.hookimpl
def parse_protos_to_resource(protos_dir, project_name, server_language, clients: List[str],domain=None):
    
    resources_added = []
    pkgs = {}
    services = []
    prj = {}
    
    project_path = str(Path(protos_dir).parents[0])

    print_info(project_path,True,tag='migrating project at path:')

    temp_clients = []
    print_info(clients,True,"Clients languages")

    for c in clients:
        temp_clients.append(WebezyClient(language=c, out_dir=file_system.join_path(project_path, 'clients', c)))

    srvr = WebezyServer(language=server_language)
    print_info(srvr,True,"Server language")
    prj = Project(uri=project_path, name=project_name, package_name=project_name.replace('-', '').replace('_', ''), version='0.0.1',
                  type=resources.ResourceTypes.project.value, kind=resources.ResourceKinds.ezy_1.value, server=srvr, clients=temp_clients)
    resources_added.append(WzResourceWrapper(project=prj))

    if file_system.walkFiles(protos_dir) is None:
        raise errors.WebezyProtoError(
            "File", "Error on parsing proto files. make sure you have a protos dir under current location.")

    for f in file_system.walkFiles(protos_dir):

        try:
            """Init parse protos"""
            protos = resources.parse_proto(f)
            # pool = resources.parse_pool(protos.pool)
            # print_info(dir(protos[0]),True,'Proto Module')
            # print_info(dir(protos[1]),True,'Service Module')

            proto_module = protos[0].DESCRIPTOR
            domain = proto_module.package.split('.')[0]

            """File options"""
            proto_file_opt = proto_module.GetOptions()
            proto_file_depend = proto_module.dependencies

            _services = proto_module.services_by_name
            _package = proto_module.package

            # print_note({'file_options':proto_file_opt,'file_dependencies':proto_file_depend},True)
           
            """Validations"""
            # TODO Handle project with no service (For future use of protobuf as standalone feature)

            if _services != {} and proto_module.message_types_by_name != {}:
                raise errors.WebezyProtoError(
                    'Service', 'Service MUST NOT hold messages ! Please de-attach the messages to stand-alone package')
            
            # Service
            if _services != {}:
                print_info("Parsing \"Service\" proto file\n\t-> Services : {0}".format(len(_services)))

                for svc in _services:

                    service_name = _services[svc].name
                    service_full_name = _services[svc].full_name
                    service_methods = _services[svc].methods_by_name
                    service = helpers.WZService(service_name,methods=[],dependencies=[])

                    for rpc in service_methods:
                        proto_rpc = service_methods[rpc]
                        service_rpc = helpers.WZRPC(proto_rpc.name,proto_rpc.input_type.full_name,proto_rpc.output_type.full_name,proto_rpc.client_streaming,proto_rpc.server_streaming)
                        service._methods.append(service_rpc)
                    
                    # print_note({'index':_services[svc].index,'has_options':_services[svc].has_options},True,'[{0}] Service expanded'.format(service_full_name))
                    services.append(service)

            # Package
            if proto_module.package is not None and proto_module.package != '':
                pkg_name = proto_module.package.split('.')[1]
                pkg_messages = proto_module.message_types_by_name
                pkg_enums = proto_module.enum_types_by_name
                package = helpers.WZPackage(pkg_name,messages=[],enums=[])
                # print_note({'has_options':proto_module.has_options,'extensions':proto_module.extensions_by_name},True,'[{0}] Service expanded'.format(service_full_name))
                print_info("Parsing \"Package\" proto file\n\t-> Messages : {}\n\t-> Enums : {}".format(len(pkg_messages),len(pkg_enums)))

                # Iterating package messages
                for msg in pkg_messages:
                    message = helpers.WZMessage(pkg_messages[msg].name,fields=[])
                    # print_note(dir(pkg_messages[msg]))
                    # print_note(pkg_messages[msg].extensions,True,msg)
                    # print_note(dir(pkg_messages[msg]),True)

                    for ext in pkg_messages[msg].extensions:
                        # print_info(ext.GetOptions().Extensions._extended_message.DESCRIPTOR.name,True)
                        # print_info(ext.extension_scope.extensions[0].name,True)
                        extension_type = resources.Options.Value(ext.GetOptions().Extensions._extended_message.DESCRIPTOR.name)
                        message._extension_type = extension_type
                        for field_extended in ext.extension_scope.extensions:
                            extended_field_desc = helpers.WZField(field_extended.name,
                                type=resources.WZFieldDescriptor.Type.Name(field_extended.type),
                                label=resources.WZFieldDescriptor.Label.Name(field_extended.label),
                                enum_type=field_extended.enum_type.full_name if field_extended.enum_type is not None else None,message_type=field_extended.message_type.full_name if field_extended.message_type is not None else None)
                            
                            message._fields.append(extended_field_desc)

                    for field in pkg_messages[msg].fields:
                        is_map_field = False
                        field_extensions = None
                        field_key_type = None
                        field_value_type = None
                        
                        # print_note(resources.WZFieldDescriptor.Type.Name(f.type),True,f.full_name)
                        # Handle message as field
                        if field.message_type is not None:

                            # Handle map special field type
                            if 'Entry' == field.message_type.name[-5:]:
                                is_map_field = True
                                for entry in field.message_type.fields_by_name:
                                    if 'key' == entry:
                                        field_key_type = resources.WZFieldDescriptor.Type.Name(field.message_type.fields_by_name[entry].type)
                                    elif 'value' == entry:
                                        field_value_type = resources.WZFieldDescriptor.Type.Name(field.message_type.fields_by_name[entry].type)
                                    else:
                                        # Not a map message
                                        field_key_type = None
                                        field_value_type = None
                                        break
                            else:
                                pass

                        # Handle field extensions
                        if field.has_options:
                            field_extensions = {}
                            field_options = field.GetOptions()
                            
                            # print_note(field_options.Extensions,True,'Extensions {}'.format(f.name))
                            # print_note(field_options.Extensions._extended_message.ListFields())

                            for f_ext in field_options.Extensions._extended_message.ListFields():
                                field_opt_type = resources.WZFieldDescriptor.Type.Name(f_ext[0].type)
                                field_opt_label = resources.WZFieldDescriptor.Label.Name(f_ext[0].label)
                                if 'REPEATED' in field_opt_label:
                                    list_values_temp = []
                                    for field_opt_value in f_ext[1]:
                                        if 'BOOL' in field_opt_type:
                                            list_values_temp.append( google_dot_protobuf_dot_struct__pb2.Value(bool_value=field_opt_value))
                                        elif 'STRING' in field_opt_type:
                                            list_values_temp.append( google_dot_protobuf_dot_struct__pb2.Value(string_value=field_opt_value))
                                        elif 'INT' in field_opt_type:
                                            list_values_temp.append( google_dot_protobuf_dot_struct__pb2.Value(number_value=field_opt_value))
                                        elif 'MESSAGE' in field_opt_type:
                                            struct_temp = google_dot_protobuf_dot_struct__pb2.Struct()
                                            for field_ext_temp in f_ext[0].message_type.fields:
                                                if field_ext_temp.type == 'TYPE_MESSAGE' or field_ext_temp.type == 'TYPE_MAP' or field_ext_temp.type == 'TYPE_ENUM':
                                                    raise errors.WebezyValidationError('Extension values parse error','There are too many nested levels for {}'.format(field_ext_temp.full_name))
                                                struct_temp.update({field_ext_temp.name:getattr(field_opt_value,field_ext_temp.name)})
                                            list_values_temp.append(google_dot_protobuf_dot_struct__pb2.Value(struct_value=struct_temp))
                                        elif 'ENUM' in field_opt_type:
                                            list_values_temp.append(google_dot_protobuf_dot_struct__pb2.Value(string_value=f_ext[0].enum_type.values_by_number[field_opt_value].name))
                                        else:
                                            print_warning("Not supporting field type [{0}] for field extensions {1}".format(field_opt_type,f_ext[0].full_name))

                                    list_values = google_dot_protobuf_dot_struct__pb2.ListValue(values=list_values_temp)
                                    field_extensions[f_ext[0].full_name] = google_dot_protobuf_dot_struct__pb2.Value(list_value=list_values)
                                else:
                                    if 'BOOL' in field_opt_type:
                                        field_extensions[f_ext[0].full_name] = google_dot_protobuf_dot_struct__pb2.Value(bool_value=f_ext[1])
                                    elif 'STRING' in field_opt_type:
                                        field_extensions[f_ext[0].full_name] = google_dot_protobuf_dot_struct__pb2.Value(string_value=f_ext[1])
                                    elif 'INT' in field_opt_type:
                                        field_extensions[f_ext[0].full_name] = google_dot_protobuf_dot_struct__pb2.Value(number_value=f_ext[1])
                                    elif 'MESSAGE' in field_opt_type:
                                            struct_temp = google_dot_protobuf_dot_struct__pb2.Struct()
                                            for field_ext_temp in f_ext[0].message_type.fields:
                                                if field_ext_temp.type == 'TYPE_MESSAGE' or field_ext_temp.type == 'TYPE_MAP' or field_ext_temp.type == 'TYPE_ENUM':
                                                    raise errors.WebezyValidationError('Extension values parse error','There are too many nested levels for {}'.format(field_ext_temp.full_name))
                                                struct_temp.update({field_ext_temp.name:getattr(f_ext[1],field_ext_temp.name)})
                                            field_extensions[f_ext[0].full_name] = google_dot_protobuf_dot_struct__pb2.Value(struct_value=struct_temp)
                                    elif 'ENUM' in field_opt_type:
                                        field_extensions[f_ext[0].full_name] = google_dot_protobuf_dot_struct__pb2.Value(string_value=f_ext[0].enum_type.values_by_number[f_ext[1]].name)
                                    else:
                                        print_warning("Not supporting field type [{0}] for field extensions {1}".format(field_opt_type,f_ext[0].full_name))
                        

                        field_message_type = field.message_type.full_name if hasattr(field.message_type,'full_name') else None
                        field_message_type = field_message_type if field_message_type is not None and field_message_type[-5:] != 'Entry' else None
                        field_enum_type = field.enum_type.full_name if hasattr(field.enum_type,'full_name') else None
                        if field_message_type == None:
                            if hasattr(field.message_type,'fields_by_name'):
                                if resources.WZFieldDescriptor.Type.Name(field.message_type.fields_by_name.get('value').type) == 'TYPE_MESSAGE':
                                    field_message_type = field.message_type.fields_by_name.get('value').message_type.full_name
                                elif resources.WZFieldDescriptor.Type.Name(field.message_type.fields_by_name.get('value').type) == 'TYPE_ENUM':
                                    field_enum_type = field.message_type.fields_by_name.get('value').enum_type.full_name
                                
                                # field_message_type = f.message_type.fields_by_name.get('value')
                                # print_info(field_message_type.full_name,field_message_type.type)

                        field = helpers.WZField(field.name,
                                                type=resources.WZFieldDescriptor.Type.Name(field.type if is_map_field == False else resources.WZFieldDescriptor.Type.TYPE_MAP),
                                                label=resources.WZFieldDescriptor.Label.Name(field.label if field_key_type is None else 1),
                                                message_type=field_message_type,
                                                enum_type=field_enum_type,
                                                extensions=field_extensions,key_type=field_key_type,value_type=field_value_type
                                                )
                        message._fields.append(field)
                    package._messages.append(message)

                # Iterating package enums
                for en in pkg_enums:
                    e_values = []
                    for ev in pkg_enums[en].values:
                        e_value = helpers.WZEnumValue(ev.name,ev.number)
                        e_values.append(e_value)
                    enum_desc = helpers.WZEnum(pkg_enums[en].name,enum_values=e_values)
                    package._enums.append(enum_desc)

                pkgs['protos/v1/{0}.proto'.format(package.name)] = package
                # package = helpers.WZPackage(pkg_name,messages=[],enums=[])
            
        except Exception as e:
            print_error(
                f'Migration Exception occured during handling of [{f}] : {e}')

    # for f in file_system.walkFiles(protos_dir):
    #     index = 0
    #     temp_file = file_system.rFile(f'{protos_dir}/{f}')
    #     for l in temp_file:
    #         if 'import "protos/' in l and 'google/protobuf' not in l:
    #             temp_file[index] = l.replace('import "protos/', 'import "')
    #         index += 1
    #     file_system.wFile(f'{protos_dir}/{f}', ''.join(temp_file), True)
    _migrate_to_webezy_json(file_system.join_path(project_path,'webezy.json'),domain if domain is not None else 'webezy',prj,pkgs,services)
    return resources_added

def _migrate_to_template(template_name:str,template_path:str):
    pass

def _migrate_to_webezy_json(webezy_json_path:str,domain,project,packages:Dict[str,helpers.WZPackage],services:List[helpers.WZService]):
    msgs_map = {}

    ARCHITECT = WebezyArchitect(
        path=webezy_json_path, domain=domain, project_name=project.name)
    c_languages = []
    for client in project.clients:
        c_languages.append({'language':resources.Language.Name(client.language)})
        # if type(client) == str:
        #     client_lang = client
        # else:
        #     client_lang = Language.Name(client)
        # out_dir = file_system.join_path(
        #     webezy_json_path.replace('webezy.json',''), 'clients', client_lang)
        # print_info(f'Adding client: {client_lang}')
        # c_languages.append(
        #     {'out_dir': out_dir, 'language': client_lang})
    ARCHITECT.AddProject(server_language=resources.Language.Name(project.server.language), clients=c_languages)
    ARCHITECT.SetDomain(domain)
    ARCHITECT.SetConfig({'host': 'localhost', 'port': 50051, 'deployment': WebezyDeploymentType.Name(WebezyDeploymentType.LOCAL) })

    for p in packages:
        package_name, package_messages, package_enums = packages[p].to_tuple()

        package_temp = ARCHITECT.AddPackage(package_name)
        for m in package_messages:
            msg_name, msg_fields, msg_desc, msg_opt = m
            msg_temp = ARCHITECT.AddMessage(package_temp, msg_name, msg_fields, msg_desc, msg_opt)
            msgs_map[msg_temp.full_name] = msg_temp

        for e in package_enums:
            enum_name, enum_values, enum_desc = e
            ARCHITECT.AddEnum(package_temp, enum_name, enum_values, enum_desc)

    for servc in services:
        svc_name, svc_methods, svc_dependencies, svc_desc = servc.to_tuple()
        temp_service = ARCHITECT.AddService(svc_name,svc_dependencies,svc_desc,[])
        for rpc in svc_methods:
            rpc_name, rpc_in_out, rpc_desc = rpc
            ARCHITECT.AddRPC(temp_service,rpc_name,rpc_in_out,rpc_desc)

    ARCHITECT.Save()
    print_success("Migrate process done !\n\t-> now you can create and edit resources with your new 'webezy.json' file.")