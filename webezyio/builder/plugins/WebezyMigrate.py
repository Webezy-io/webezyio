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
from typing import List, Literal
import webezyio.builder as builder
from webezyio.commons import helpers, file_system, resources, errors
from webezyio.commons.pretty import print_info, print_success
from webezyio.commons.protos.webezy_pb2 import Descriptor, Language, Project, ServiceDescriptor, WebezyClient, WebezyServer, WzResourceWrapper


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Finished webezyio build process %s plugin" % (__name__))


_WELL_KNOWN_LANGUAGED = Literal["python", "typescript"]


@builder.hookimpl
def parse_protos_to_resource(protos_dir, project_name, server_language, clients: List[int] = [Language.python]):
    resources_added = []
    pkgs = {}
    services = {}
    prj = {}
    path = protos_dir.replace('/protos', '')
    print_info(path,tag='path')
    print_info(protos_dir)

    temp_clients = []
    for c in clients:
        temp_clients.append(WebezyClient(language=Language.Name(
            c), out_dir=file_system.join_path(path, 'clients', Language.Name(c))))
    srvr = WebezyServer(language=Language.Name(Language.python))
    prj = Project(uri=path, name=project_name, package_name=project_name.replace('-', '').replace('_', ''), version='0.0.1',
                  type=resources.ResourceTypes.project.name, kind=resources.ResourceKinds.ezy_1.name, server=srvr, clients=temp_clients)
    resources_added.append(WzResourceWrapper(project=prj))

    if file_system.walkFiles(protos_dir) is None:
        raise errors.WebezyProtoError(
            "File", "Error on parsing proto files. make sure you have a protos dir under current location.")
    # for f in file_system.walkFiles(protos_dir):
    #     temp_file = file_system.rFile(f'{protos_dir}/{f}')
    #     index = 0
    #     file = temp_file
    #     for l in file:
    #         if 'import "' in l and 'google/protobuf' not in l:
    #             file[index] = l.replace('import "', 'import "protos/')
    #         index += 1
    #     # print(f, file)
    #     file_system.wFile(f'{protos_dir}/{f}', ''.join(file), True)

    for f in file_system.walkFiles(protos_dir):

        print_info(f"Parsing -> {f}")
        try:
            protos = resources.parse_proto(f)
            # pool = resources.parse_pool(protos.pool)
            print_info(protos,True)
            print_info(dir(protos[0]),True,'Proto Module')
            print_info(dir(protos[1]),True,'Service Module')
            proto_module = protos[0].DESCRIPTOR
            # print_info(
                # f'[{proto_module.name}] {proto_module.package} | Has Opt: {proto_module.has_options} | {proto_module.extensions_by_name}')

            if proto_module.services_by_name != {} and proto_module.message_types_by_name != {}:
                raise errors.WebezyProtoError(
                    'Service', 'Service canot hold messages ! Please de-attach the messages to stand-alone package')

            if proto_module.package is not None and proto_module.package != '':
                pkg_name = proto_module.package.split('.')[1]
                print_info(pkg_name)
        #         pkg_v = protos.package.split('.')[-1]
        #         pkg_domain = protos.package.split('.')[0]
        #         pkg_path = 'protos/{0}/{1}.proto'.format(pkg_v, pkg_name)
        #         pkgs[pkg_path] = {'uri': resources.get_uri_package(
        #             path, protos.package), 'name': pkg_name, 'package': protos.package, 'messages': [], 'enums': []}
        #         for msg in protos.message_types_by_name:
        #             desc = resources.DescriptorProto()
        #             protos.message_types_by_name[msg].CopyToProto(desc)
        #             msg_full_name = f'{protos.package}.{desc.name}'
        #             fields = []
        #             try:
        #                 logging.info(desc.Extensions)
        #             except Exception:
        #                 logging.debug("Not extension")
        #             for f in desc.field:
        #                 field_full_name = f'{msg_full_name}.{f.name}'
        #                 field = {'uri': resources.get_uri_field(path, field_full_name), 'name': f.name, 'fullName': field_full_name, 'index': f.number, 'fieldType': resources.FieldDescriptorProto.Type.Name(
        #                     f.type), 'label': resources.FieldDescriptorProto.Label.Name(f.label), 'type': resources.ResourceTypes.descriptor.value, 'kind': resources.ResourceKinds.field.value}

        #                 if resources.FieldDescriptorProto.Type.Name(f.type) == 'TYPE_MESSAGE':
        #                     field['messageType'] = f.type_name[1:]

        #                 fields.append(field)

        #             # resources.Descriptor(name=desc.name,full_name=desc.full_name,filename=desc.filename,containing_type=desc.containing_type,fields=desc.fields,nested_types=desc.nested_types,enum_types=desc.enum_types,extensions=desc.extensions)
        #             msg_dict = {'uri': resources.get_uri_message(
        #                 path, msg_full_name), 'name': desc.name, 'fullName': msg_full_name, 'fields': fields}

        #             pkgs[pkg_path]['messages'].append(msg_dict)
        #             resources_added.append(WzResourceWrapper(
        #                 message=resources.ParseDict(msg_dict, Descriptor())))

        #         for enum in protos.enum_types_by_name:
        #             pass

        #     for svc in protos.services_by_name:
        #         rpcs = []
        #         for rpc in protos.services_by_name[svc].methods_by_name:
        #             rpc = protos.services_by_name[svc].methods_by_name[rpc]
        #             client_stream = rpc.client_streaming
        #             server_stream = rpc.server_streaming
        #             full_name = rpc.full_name
        #             input_type = rpc.input_type.full_name
        #             output_type = rpc.output_type.full_name
        #             rpcs.append({'uri': resources.get_uri_rpc(path, full_name), 'name': rpc.name, 'fullName': full_name,
        #                         'outputType': output_type, 'inputType': input_type, 'clientStreaming': client_stream, 'serverStreaming': server_stream})
        #         service = {'uri': resources.get_uri_service(
        #             path, svc, server_language), 'name': svc, 'methods': rpcs}
        #         services[svc] = service
        #         logging.info(f"Adding {svc}")
        #         resources_added.append(WzResourceWrapper(
        #             service=resources.ParseDict(service, ServiceDescriptor())))

        except Exception as e:
            logging.exception(
                f'Exception occured during handling of [{f}] : {e}')

    # for f in file_system.walkFiles(protos_dir):
    #     index = 0
    #     temp_file = file_system.rFile(f'{protos_dir}/{f}')
    #     for l in temp_file:
    #         if 'import "protos/' in l and 'google/protobuf' not in l:
    #             temp_file[index] = l.replace('import "protos/', 'import "')
    #         index += 1
    #     file_system.wFile(f'{protos_dir}/{f}', ''.join(temp_file), True)
    print_success(resources_added)

    return resources_added
