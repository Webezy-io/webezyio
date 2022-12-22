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
import re
import socket
import subprocess
from typing import List, Literal
from webezyio import __version__,config
from webezyio.commons import file_system

from webezyio.commons import errors, pretty
from webezyio.commons.resources import generate_package, generate_service
from webezyio.commons.errors import WebezyCoderError, WebezyValidationError
from webezyio.commons.file_system import check_if_file_exists, join_path
from webezyio.commons.protos import WebezyJson,WebezyAnalytics_pb2,webezycore
from itertools import groupby
from google.protobuf.struct_pb2 import Value
from google.protobuf.json_format import ParseDict, MessageToDict
from google.protobuf import text_format
from google.protobuf.timestamp_pb2 import Timestamp
from platform import platform
from inquirer import errors as inquirerErrors

_WELL_KNOWN_PY_IMPORTS = [
    "from google.protobuf.timestamp_pb2 import Timestamp", "from typing import Iterator"]

_WELL_KNOWN_TS_IMPORTS = ["import { \n\thandleUnaryCall,\n\thandleClientStreamingCall,\n\thandleServerStreamingCall,\n\thandleBidiStreamingCall,\n\tsendUnaryData,\n\tServerDuplexStream,\n\tServerReadableStream,\n\tServerUnaryCall,\n\tServerWritableStream,\n\tstatus,\n\tUntypedHandleCall,\n\tMetadata\n } from '@grpc/grpc-js';","import { ServiceError } from './utils/error';","import { ApiType } from './utils/interfaces';"]

_WELL_KNOWN_GO_IMPORTS = ['"context"','"io"','"google.golang.org/grpc/metadata"']

_FIELD_TYPES = Literal["TYPE_INT32", "TYPE_INT64", "TYPE_STRING", "TYPE_BOOL",
                       "TYPE_MESSAGE", "TYPE_ENUM", "TYPE_DOUBLE", "TYPE_FLOAT", "TYPE_BYTE"]
_FIELD_LABELS = Literal["LABEL_OPTIONAL", "LABEL_REPEATED"]
_EXTENSIONS_TYPE = Literal["FileOptions", "MessageOptions", "FieldOptions","ServiceOptions","MethodOptions"]

_OPEN_BRCK = '{'
_CLOSING_BRCK = '}'


def check_if_under_project():
    return check_if_file_exists(join_path(os.getcwd(),'webezy.json'))


def wzJsonCacheToMessage(path) -> WebezyJson:
    # return text_format.Parse(f.read(),WebezyJson())
    # return WebezyJson().ParseFromString(bytes(f.read(),'utf-8'))
    data = open(path, "rb").read()  # read file as string
    msg = WebezyJson()
    msg.ParseFromString(data)


def wzJsonToMessage(wz_json,validate:bool=False) -> WebezyJson:
    if validate:
        pretty.print_info("Validating webezy.json",True)
        # assert(wz_json.get('project') is not None)
        # assert(wz_json.get('config') is not None)
        # assert(wz_json.get('packages') is not None)
        # assert(wz_json.get('services') is not None)
        # for p in wz_json.get('packages'):
        #     pkg = wz_json.get('packages')[p]
        #     reorder = []
        #     index = 0
        #     for m in pkg.get('messages'):
        #         dependency_in_pkg = next((f for f in m.get('fields') if f.get('messageType') is not None),None)
                
        #         reorder.append(index)
        #         if dependency_in_pkg is not None:
        #             if pkg.get('package') in dependency_in_pkg.get('messageType'):
        #                 pretty.print_error(dependency_in_pkg)
        #                 pretty.print_info(reorder,True,"{0} / {1}".format(index,max(reorder)))
        #                 if index > max(reorder):
        #                     reorder = [x+1 for x in reorder]
        #                     reorder[index] = max(reorder) -1
        #                 else: 
        #                     reorder[index] = index +1
        #             else:
        #                 if index >= reorder[index]:
        #                     reorder = [x+1 for x in reorder]

        #                 reorder[index] = index
        #         else:
        #             reorder[index] = max(reorder) +1
        #         pretty.print_info(dependency_in_pkg,True)
        #         pretty.print_info(reorder,True,"After changes")
            
        #         index += 1
        #     reorder = [x-1 for x in reorder]
        #     mylist = [pkg.get('messages')[i] for i in reorder]
        #     pkg['messages'] = mylist

        #     pretty.print_info(mylist,True,"Last step")
        #     wz_json['packages'][p] = pkg
        #     pretty.print_info(wz_json['packages'][p],True,"Package After Change step")
    
    # DEPRECATED webezy.project.serverLanguage field -> webezy.project.server.langugae
    # Removing the deprecated field to not have any errors
    if wz_json.get('project').get('serverLanguage') :
        pretty.print_warning('Deprecated field \'webezy.project.serverLanguage\' -> Moved to \'webezy.project.server.langugae\' Since 0.1.2')
        del wz_json['project']['serverLanguage']

    return ParseDict(wz_json, WebezyJson())


class WZProject():
    """webezyio top level object that defines the required meta data properties."""

    def __init__(self, webezy_json_path: str, project_name: str, domain: str,) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.Project` representation.

        Parameters
        ----------
            webezy_json_path (str): Absoulute path of Webezy JSON file.
            project_name (str): A project name, can include hyphens or
                 underscores but not blank spaces.
            domain (Str): A company domain name,
                it is not the full domain your company holds 
                for e.x all `webezy.io` projects are inputed on gRPC
                as `webezy` without any suffix or prefix.
        """


class WZField():
    """webezyio field level object that defines the required meta data properties."""

    def __init__(self, name, type: _FIELD_TYPES, label: _FIELD_LABELS, message_type=None, enum_type=None, extensions=None, description=None, key_type=None, value_type=None, oneof_fields=[]) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.FieldDescriptor` representation.

        Parameters
        ----------
            name (str): A field name, `MUST` not include blank space and hyphens.
            type (:module:`webezyio.commons.helpers._FIELD_TYPES`): One of the available field types.
            label (:module:`webezyio.commons.helpers._FIELD_LABELS`): One of the available labels,
                `LABEL_REPEATED` - will compile generated class field as array / list type
            message_type (str): `MUST` be included when field type is `TYPE_MESSAGE` and should be 
                passed as full name for the message the field represent.
            enum_type (str): Same as `message_type` field just with enums binding.
            extensions (dict): A dict value for extensions of field.
            description (str):  A field description.
        """

        self._name = name
        self._field_type = type
        self._label = label
        self._message_type = message_type
        self._enum_type = enum_type
        self._extensions = extensions
        self._description = description
        self._key_type = key_type
        self._value_type = value_type
        self._oneof_fields = oneof_fields


    def setName(self, name):
        self._name = name

    def setType(self, type):
        self._field_type = type

    def setLabel(self, label):
        self._label = label

    def setMessageType(self, message_type):
        self._message_type = message_type

    def to_dict(self):
        temp = {}
        self._validate()
        for k in dict(self.__dict__):
            if k == '_extensions':
                if dict(self.__dict__)[k] is not None:
                    temp[k[1:]] = {}
                    for j in dict(self.__dict__)[k]:
                        if isinstance(dict(self.__dict__)[k][j], str):
                            temp[k[1:]][j] = Value(
                                string_value=dict(self.__dict__)[k][j])
                        elif isinstance(dict(self.__dict__)[k][j], int) or isinstance(dict(self.__dict__)[k][j], float):
                            temp[k[1:]][j] = Value(
                                number_value=dict(self.__dict__)[k][j])
                        elif isinstance(dict(self.__dict__)[k][j], bool):
                            temp[k[1:]][j] = Value(
                                bool_value=dict(self.__dict__)[k][j])
                        else:
                            if isinstance(dict(self.__dict__)[k][j], Value):
                                temp[k[1:]][j] = dict(self.__dict__)[k][j]
                            else:
                                pretty.print_warning("Not supported extension type !")
            else:
                temp[k[1:]] = dict(self.__dict__)[k]


        return temp

    def _validate(self):
        if self._field_type == 'TYPE_ENUM':
            if self._enum_type is None:
                pretty.print_error(f"Field {self._name} missing enum type and is configured as 'TYPE_ENUM'")
                exit(1)
        elif self._field_type == 'TYPE_MESSAGE':
            if self._message_type is None:    
                pretty.print_error(f"Field {self._name} missing enum type and is configured as 'TYPE_MESSAGE'")
                exit(1)

    @property
    def name(self):
        return self._name

    @property
    def field_type(self):
        return self._field_type

    @property
    def label(self):
        return self._label

    @property
    def message_type(self):
        return self._message_type


class WZRPC():
    """webezyio RPC level object that defines the required meta data properties."""

    def __init__(self, name, in_type, out_type, client_stream=False, server_stream=False, description=None) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.MethodDescriptor` representation.

        Parameters
        ----------
            name (str): A RPC name, `MUST` not include blank space and hyphens.
            in_type (str): Full name for message to be used as input type for the new RPC.
            out_type (str):  Full name for message to be used as output type for the new RPC.
            client_stream (bool): If client stream is available to this RPC, Defaulted to False.
            server_stream (bool): If sever stream is available to this RPC, Defaulted to False.
            description (str): Description for the RPC mainly used for client generated docs.
        """
        self._name = name
        self._input_type = in_type
        self._output_type = out_type
        self._client_stream = client_stream
        self._server_stream = server_stream
        self._description = description

    def to_tuple(self):
        return self._name, [(self._client_stream, self._input_type), (self._server_stream, self._output_type)], self._description


class WZService():
    """webezyio service level object that defines the required meta data properties."""

    def __init__(self, name, methods: List[WZRPC] = [], dependencies: List[str] = [], description=None,extensions=None) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.ServiceDescriptor` representation.

        Parameters
        ----------
            name (str): A service name, `MUST` not include blank space and hyphens.
            methods (:module:`List[webezyio.commons.helpers.WZRPC]`): A list of RPC methods.
            dependencies (List[str]): List of service dependencies (Other packages).
            description (str): A service description.
        """
        self._name = name
        self._methods = methods
        self._dependencies = dependencies
        self._description = description
        self._extensions = extensions

    def to_tuple(self):
        rpcs = []
        for rpc in self._methods:
            rpcs.append(rpc.to_tuple())
        return self._name, rpcs, self._dependencies, self._description, self._extensions

    @property
    def name(self):
        return self._name


class WZMessage():
    """webezyio message level object that defines the required meta data properties."""

    def __init__(self, name, fields: List[WZField] = None, description: str = None, extension_type: _EXTENSIONS_TYPE = None,extensions=None,domain=None) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.Descriptor` representation.

        Parameters
        ----------
            name (str): A message name, `MUST` not include blank space and hyphens.
            fields (:module:`List[webezyio.commons.helpers.WZField]`): A list of message fields.
            description (str): A message description.
            extension_type (:module:`webezyio.commons.protos.webezy_pb2.Options`): A message extension option.
        """
        self._name = name
        self._fields = fields
        self._description = description
        self._extension_type = extension_type
        self._extensions = extensions
        self._domain = domain

    def setFields(self, fields: List[WZField]):
        self._fields = fields

    def to_tuple(self):
        if self._fields is None:
            raise WebezyValidationError(
                "Message", "Message must hold atleast 1 field !")

        f_array = []
        for f in self._fields:
            f_array.append(f.to_dict())

        return self._name, f_array, self._description, self._extension_type, self._extensions,  self._domain

    @property
    def name(self):
        return self._name


class WZEnumValue():
    """webezyio enum value level object that defines the required meta data properties."""

    def __init__(self, name: str, number: int, description: str = None) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.EnumValue` representation.

        Parameters
        ----------
            name (str): A enum key.
            number (int): A enum value.
        """
        self._name = name
        self._number = number
        self._description = description

    def setName(self, name):
        self._name = name

    def setNumber(self, type):
        self._number = type

    def setDescription(self, type):
        self._description = type

    def to_dict(self):
        temp = {}
        for k in dict(self.__dict__):
            temp[k[1:]] = dict(self.__dict__)[k]
        return temp

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number


class WZEnum():
    """webezyio enum level object that defines the required meta data properties."""

    def __init__(self, name, enum_values: List[WZEnumValue] = [],description:str = '',domain=None) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.Enum` representation.

        Parameters
        ----------
            name (str): A enum name.
            enum_values (:module:`List[webezyio.commons.helpers.WZEnumValue]`): A list of enum values.
        """
        self._name = name
        self._enum_values = enum_values
        self._description = description
        self._domain = domain

    def to_tuple(self):
        enums_values = []
        for ev in self._enum_values:
            enums_values.append(ev.to_dict())
        return self._name, enums_values, self._description, self._domain

    @property
    def name(self):
        return self._name


class WZContext():

    def __init__(self, webezy_context):
        self._webezy_context = webezy_context
        self._parse_context()

    def _parse_context(self):
        self._files = self._webezy_context.get('files')

    def get_rpc(self, service, name):
        svc = next((svc for svc in self._files if svc['file'].split(
            '/')[-1].split('.')[0] == service), None)
        if svc is not None:
            for rpc in svc['methods']:
                if rpc['name'] == name:
                    return rpc
        else:
            return svc

    def new_rpc(self,service,context, suffix='py'):
        file = next((file for file in self._files if file.get('file') == f'./services/{service}.{suffix}'),None)
        if file is not None:
            file.get('methods').append(context)

    def edit_rpc(self, service, name, new_context):
        rpc = self.get_rpc(service, name)
        rpc['code'] = new_context['code']
        rpc['type'] = new_context['type']
        rpc['name'] = new_context['name']

    def set_rpc_code(self, service, name, code):
        rpc = self.get_rpc(service, name)
        rpc['code'] = code
        rpc['type'] = 'rpc'

    def get_functions(self, service):
        svc = next((svc for svc in self._files if svc['file'].split(
            '/')[-1].split('.')[0] == service), None)
        funcs = []
        if svc is not None:
            for func in svc['methods']:
                if func['type'] != 'rpc':
                    funcs.append(func)
            return funcs
        else:
            return svc

    def set_method_code(self, service, name, code):
        file = next((f for f in self._files if service in f['file']), None)
        if file is not None:
            method = next(
                (m for m in file['methods'] if m['name'] == name), None)
            if method is None:
                file['methods'].insert(
                    0, {'name': name, 'code': code, 'type': 'func'})
            else:
                method['code'] = code

    def dump(self):
        return self._webezy_context

    @property
    def files(self):
        return self._files


class WZPackage():
    """webezyio package level object that defines the required meta data properties."""

    def __init__(self, name, messages: List[WZMessage] = [], enums: List[WZEnum] = [],extensions=None,domain=None):
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.PackageDescriptor` representation.

        Parameters
        ----------
            name (str): A package name.
            messages (List[:module:`webezyio.commons.helpers.WZMessage`]): A list of package messages.
            enums (List[:module:`webezyio.commons.helpers.WZEnum`]): A list of package enums.
        """
        self._name = name
        self._messages = messages
        self._enums = enums
        self._extensions = extensions
        self._domain = domain

    def to_tuple(self):
        messages = []
        enums = []
        for e in self._enums:
            enums.append(e.to_tuple())
        for m in self._messages:
            messages.append(m.to_tuple())
        return self._name, messages, enums, self._extensions, self._domain

    @property
    def name(self):
        return self._name


class WZJson():

    def __init__(self, webezy_json):
        self._webezy_json = webezy_json
        self._parse_json()

    def _parse_json(self):
        self._domain = self._webezy_json.get('domain')
        self._config = self._webezy_json.get('config')
        self._project = self._webezy_json.get('project')
        self._services = self._webezy_json.get('services')
        self._packages = self._webezy_json.get('packages')
        self._path = self._webezy_json.get('project').get('uri')

    def get_service(self, name, json=True):
        if json:
            try:
                return self._services[name]
            except Exception:
                return None
        else:
            depend = self._services[name].get('dependencies')
            methods = self._services[name].get('methods')
            return generate_service(self.path,self.domain,name,self.get_server_language(),depend if depend is not None else [],self._services[name].get('description'),methods if methods is not None else [])


    def get_package(self, name,json=True):
        if json:
            return self._packages[f'protos/v1/{name}.proto']
        else:
            depend = self._packages[f'protos/v1/{name}.proto'].get('dependencies')
            msgs = self._packages[f'protos/v1/{name}.proto'].get('messages')
            enums = self._packages[f'protos/v1/{name}.proto'].get('enums')
            return generate_package(self.path,self.domain,name,depend if depend is not None else [],msgs if msgs is not None else [],enums if enums is not None else [],wz_json=self)


    def get_enum(self, full_name):
        pkg_name = full_name.split('.')[1]
        enums = self._packages[f'protos/v1/{pkg_name}.proto'].get('enums')
        if enums is not None:
            return next((e for e in enums if e['name'] == full_name.split('.')[-1]), None)
        else:
            return None


    def get_message(self, full_name):
        pkg_name = full_name.split('.')[1]
        msgs = self._packages[f'protos/v1/{pkg_name}.proto']['messages']
        return next((m for m in msgs if m['name'] == full_name.split('.')[-1]), None)

    def get_rpc(self, full_name):
        svc_name = full_name.split('.')[1]
        rpcs = self._services[svc_name].get('methods')
        if rpcs is None:
            return rpcs
        else:
            return next((r for r in rpcs if r['name'] == full_name.split('.')[-1]), None)

    def get_server_language(self):
        return self.project.get('server').get('language').lower()

    def get_extended_fields(self,message_full_name:str):
        """This function should be used when trying to iterate a specific message fields options
        
        Args
        ----
            message_full_name - Full valid name for the message we want to get fields that are extended

        Returns
        -------
            A list of fields under passed message that holds an extension value
        """
        list_fields = None
        temp_msg = self.get_message(message_full_name)

        if temp_msg is not None:
            list_fields = [f for f in temp_msg.get('fields') if f.get('extensions') is not None]
            
        return list_fields

    def get_extended_messages(self,package:str,extension:str=None):
        """This function should be used when trying to iterate a specific package message options
        
        Args
        ----
            package - valid name for the package we want to get fields that are extended
            extension - Optional full name that filter the message extension accordingly must be the extension message full name

        Returns
        -------
            A list of messages under passed package that holds an extension value
        """
        list_msgs = None
        temp_pkg = self.get_package(package)

        if temp_pkg is not None:
            if temp_pkg.get('messages') is not None:
                list_msgs = [
                    m for m in temp_pkg.get('messages') if m.get('extensions') is not None 
                    and (extension in m.get('extensions') if extension is not None else True)]
            
        return list_msgs

    @property
    def domain(self):
        """str: Project domain."""
        return self._domain

    @property
    def project(self):
        """:obj:`dict` Project dictionary."""
        return self._project

    @property
    def services(self):
        """:obj:`List[dict]` Project domain."""
        return self._services

    @property
    def packages(self):
        return self._packages

    @property
    def path(self):
        return self._path

def load_wz_json(path:str):
    WEBEZY_JSON = file_system.rFile(path, json=True)
    WEBEZY_JSON = WZJson(webezy_json=WEBEZY_JSON)
    return WEBEZY_JSON

class WZProto():

    def __init__(self, name, imports=[], service=None, package=None, messages=[], enums=[], description=None,extensions=None,wz_json:WZJson=None):
        self._name = name
        self._imports = imports
        self._service = service
        self._package = package
        self._messages = messages
        self._enums = enums
        self._description = description
        self._extensions = extensions
        self._wz_json = wz_json

    def write_imports(self):
        temp_imports = []
        if self._wz_json.project.get('goPackage') is not None:
                temp_imports.append('\n// Go package name\noption go_package = "{}{}";\n'.format(self._wz_json.project.get('goPackage'),'/services/protos/{}'.format(self._name)))
        if self._imports is not None:
                
            for imp in self._imports:
                if 'google.protobuf.' in imp:
                    imp = f"{imp.replace('.','/')}.proto"
                    temp_imports.append(f'import "{imp.lower()}";')
                else:
                    imp = imp.split('.')[1]
                    temp_imports.append(f'import "{imp}.proto";')

            options = next((m for m in self._messages if m.get(
                'extensionType') is not None), None)
            if options is not None and 'google.protobuf.Descriptor' not in self._imports :
                temp_imports.append(
                    'import "google/protobuf/descriptor.proto";')
            return '\n'.join(temp_imports)
        else:
            return '\n'.join(temp_imports)

    def write_package(self):
        if self._package is not None:
            if self._extensions is not None:
                temp_extensions = []
                for ext_key in self._extensions:

                    ext_value = self._extensions[ext_key]
                    extension_type = self._wz_json.get_message('.'.join(ext_key.split('.')[:4]))
                    extensions_package = parse_extension_to_proto('FileOptions',extension_type,ext_key,ext_value,self._wz_json)
                    temp_extensions.append(extensions_package)
                joined_extensions = '\n'.join(temp_extensions)
                return f'package {self._package};\n\n// Webezy.io Package Extensions\n{joined_extensions}'
            else:
                return f'package {self._package};'
        else:
            return ''

    def write_service(self):
        if self._service is not None:
            rpcs = []

            if self._service.get('extensions') is not None:
                for ext in self._service.get('extensions'):
                    ext_msg = self._wz_json.get_message('.'.join(ext.split('.')[:4]))
                    temp_svc_ext = parse_extension_to_proto('ServiceOptions',ext_msg,ext,self._service.get('extensions')[ext],self._wz_json)
                    rpcs.append(temp_svc_ext)

            for m in self._service.get('methods'):
                rpc_name = m.get('name')
                msg_name_in = m.get('inputType')
                msg_name_out = m.get('outputType')

                description = m.get('description')

                stream_in = 'stream ' if m.get('clientStreaming') is not None and m.get(
                    'clientStreaming') == True else ''
                stream_out = 'stream ' if m.get('serverStreaming') is not None and m.get(
                    'serverStreaming') == True else ''
                
                rpcs.append(
                    f'// [webezyio] - {description}\n\trpc {rpc_name} ({stream_in}{msg_name_in}) returns ({stream_out}{msg_name_out});')
            rpcs = '\n\t'.join(rpcs)
            desc = f'// [webezyio] {self._description}\n' if self._description is not None else ''
            return f'{desc}service {self._name} {_OPEN_BRCK}\n\t{rpcs}\n{_CLOSING_BRCK}'
        else:
            return ''

    def write_messages(self):
        if len(self._messages) > 0:
            msgs = []
            for m in self._messages:
                msg_name = m.get('name')
                msgFullName = m.get('fullName')
                fields = []
                # Adding MessageOptions
                if m.get('extensions') is not None:
                    for ext_key in m.get('extensions'):
                        ext_msg = self._wz_json.get_message('.'.join(ext_key.split('.')[:-1]))
                        if ext_msg is None:
                            raise WebezyValidationError(
                                'FieldOptions', f'Field Option [{ext}] specified for : "{fName}", is invalid !')
                        fields.append('{}'.format(parse_extension_to_proto('MessageOptions',ext_msg,ext_key,m.get('extensions')[ext_key],self._wz_json)))
                m_desc = m.get('description')
                ext_type = m.get('extensionType')
                for f in m.get('fields'):
                    fLabel = '' if f.get('label') == 'LABEL_OPTIONAL' or f.get('label') is None else '{0} '.format(
                        f.get('label').split('_')[-1].lower())
                    fType = f.get('fieldType').split('_')[-1].lower()
                    if fType == 'message':
                        fType = f.get('messageType')
                    elif fType == 'enum':
                        fType = f.get('enumType')
                    elif fType == 'map':
                        keyType = f.get('keyType').split('_')[-1].lower()
                        valueType = f.get('valueType').split('_')[-1].lower() if f.get('valueType') != 'TYPE_MESSAGE' and f.get('valueType') != 'TYPE_ENUM'  else f.get('messageType') if f.get('valueType') == 'TYPE_MESSAGE' else f.get('enumType') if f.get('valueType') == 'TYPE_ENUM' else None
                        if valueType is None:
                            pretty.print_error("Value type for 'map' is not valid ! {0}".format(f.get('valueType')))
                        else:
                            fType = 'map<{0}, {1}>'.format(keyType,valueType)
                    elif fType == 'oneof':
                        field_name = f.get('name')
                        oneof_fields = []
                        
                        for oneof_field in f.get('oneofFields'):
                            if oneof_field.get('fieldType') == 'TYPE_MESSAGE':
                                oneof_field_type = oneof_field.get('messageType')
                            elif oneof_field.get('fieldType') == 'TYPE_ENUM':
                                oneof_field_type = oneof_field.get('enumType')
                            else:
                                oneof_field_type = oneof_field.get('fieldType').split('_')[-1].lower()
                            
                            oneof_field_name = oneof_field.get('name')
                            oneof_field_index = oneof_field.get('index') if oneof_field.get('index') is not None else 1
                            oneof_fields.append(f'\n\t\t{oneof_field_type} {oneof_field_name} = {oneof_field_index};')
                        oneof_fields = ''.join(oneof_fields)
                        fType = f'oneof {field_name} {_OPEN_BRCK}\n{oneof_fields}\n\t{_CLOSING_BRCK}'
                    
                    fName = f.get('name')
                    fIndex = f.get('index')
                    fOptions = []
                    if f.get('extensions') is not None:
                        for ext in f.get('extensions'):
                            list_names = ext.split('.')
                            ext_msg = None

                            if len(list_names) > 2:
                                if '.'.join(list_names[:3]) == self._package:
                                    ext_msg = next((m for m in self._messages if m.get('name') == list_names[3]),None)
                            else:
                                ext_msg = next((m for m in self._messages if m.get(
                                    'name') == ext.split('.')[0]), None)
                            if ext_msg is None:
                                ext_msg = self._wz_json.get_message('.'.join(ext.split('.')[:-1]))
                                if ext_msg is None:
                                    raise WebezyValidationError(
                                        'FieldOptions', f'Field Option [{ext}] specified for : "{fName}", is invalid !')
                            
                            temp_field_extension_test = parse_extension_to_proto('FieldOptions',ext_msg,ext,f.get('extensions')[ext],self._wz_json)
                            fOptions.append(temp_field_extension_test)

                        fOptions = ',\n\t\t'.join(fOptions)
                    fOptions = f' [\n\t\t{fOptions}\n\t]' if len(fOptions) > 1 else f'[{fOptions}]' if len(fOptions) == 1 else ''
                    fDesc = f.get('description')
                    fFullName = f.get('fullName')
                    if ext_type == 'FieldOptions' or ext_type == 'FileOptions' or ext_type == 'MessageOptions' or ext_type == 'ServiceOptions' or ext_type == 'MethodOptions':
                        fDesc = f'// [{fFullName}] - {fDesc}\n\t\t' if fDesc is not None else ''
                    else:
                        fDesc = f'// [{fFullName}] - {fDesc}\n\t' if fDesc is not None else ''
                    if f.get('fieldType') == 'TYPE_ONEOF':
                        fields.append(
                            f'{fDesc}{fType}')
                    else:
                        fields.append(
                            f'{fDesc}{fLabel}{fType} {fName} = {fIndex}{fOptions};')

                if ext_type == 'FieldOptions':
                    fields = '\n\t\t'.join(fields)
                    msgs.append(
                        f'// [{msgFullName}] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\textend google.protobuf.FieldOptions {_OPEN_BRCK}\n\t\t{fields}\n\t{_CLOSING_BRCK}\n{_CLOSING_BRCK}\n')
                elif ext_type == 'MessageOptions':
                    fields = '\n\t\t'.join(fields)
                    msgs.append(
                        f'// [{msgFullName}] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\textend google.protobuf.MessageOptions {_OPEN_BRCK}\n\t\t{fields}\n\t{_CLOSING_BRCK}\n{_CLOSING_BRCK}\n')
                elif ext_type == 'FileOptions':
                    fields = '\n\t\t'.join(fields)
                    msgs.append(
                        f'// [{msgFullName}] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\textend google.protobuf.FileOptions {_OPEN_BRCK}\n\t\t{fields}\n\t{_CLOSING_BRCK}\n{_CLOSING_BRCK}\n')
                elif ext_type == 'ServiceOptions':
                    fields = '\n\t\t'.join(fields)
                    msgs.append(
                        f'// [{msgFullName}] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\textend google.protobuf.ServiceOptions {_OPEN_BRCK}\n\t\t{fields}\n\t{_CLOSING_BRCK}\n{_CLOSING_BRCK}\n')
                elif ext_type == 'MethodOptions':
                    fields = '\n\t\t'.join(fields)
                    msgs.append(
                        f'// [{msgFullName}] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\textend google.protobuf.MethodOptions {_OPEN_BRCK}\n\t\t{fields}\n\t{_CLOSING_BRCK}\n{_CLOSING_BRCK}\n')
                else:
                    fields = '\n\t'.join(fields)
                    msgs.append(
                        f'// [{msgFullName}] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\t{fields}\n{_CLOSING_BRCK}\n')

            msgs = '\n'.join(msgs)
            return msgs
        else:
            return ''

    def write_enums(self):
        if self._enums is not None:
            enums = []
            for e in self._enums:
                enum_name = e.get('name')
                enum_full_name = e.get('fullName')
                values = []
                for v in e.get('values'):
                    value_name = v.get('name')
                    value_number = 0 if v.get(
                        'number') is None else v.get('number')
                    v_desc = v.get('description')
                    values.append(f'// [{enum_full_name}] - {v_desc}\n\t{value_name} = {value_number};')
                values = '\n\t'.join(values)
                e_desc = e.get('description')
                enums.append(
                    f'// [{enum_full_name}] - {e_desc}\nenum {enum_name} {_OPEN_BRCK}\n\t{values}\n{_CLOSING_BRCK}\n')
            return '\n'.join(enums)

        else:
            return ''

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'// Webezy.io Generated proto DO NOT EDIT\nsyntax = "proto3";\n\n{self.write_imports()}\n{self.write_package()}\n\n{self.write_service()}\n\n{self.write_messages()}\n{self.write_enums()}'


class WZClientPy():
    """A helper class to write 'Python' language clients for Webezy.io project services"""

    def __init__(self, project_package, services=None, packages=None, context: WZContext = None, config = None):

        self._services = services
        self._project_package = project_package
        self._context = context
        self._packages = packages
        self._config = config

    def __str__(self):

        return f'{self.write_imports()}\n{self.write_client_wrapper()}\n\n\t{self.write_services_classes()}'

    def write_client_wrapper(self):
        return f'\n# For available channel options in python visit https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h\n_CHANNEL_OPTIONS = (("grpc.keepalive_permit_without_calls",1),\n\t("grpc.keepalive_time_ms",120000),\n\t("grpc.http2.min_time_between_pings_ms",120000),\n\t("grpc.keepalive_timeout_ms",20000),\n\t("grpc.http2.max_pings_without_data",0),)\n\nclass {self._project_package}:\n\n\t{self.init_wrapper()}'

    def init_stubs(self):
        stubs = []
        for svc in self._services:
            stubs.append(f'self.{svc}Stub = {svc}Service.{svc}Stub(channel)')

        return '\n\t\t'.join(stubs)

    def init_wrapper(self):
        if self._config is not None:
            host = self._config.get('host')
            port = self._config.get('port')

        else:
            host = 'localhost'
            port = 50051
        init_func = f'def __init__(self, host="{host}", port={port}, timeout=10):\n\t\tchannel = grpc.insecure_channel(\'{_OPEN_BRCK}0{_CLOSING_BRCK}:{_OPEN_BRCK}1{_CLOSING_BRCK}\'.format(host, port),_CHANNEL_OPTIONS)\n\t\ttry:\n\t\t\tgrpc.channel_ready_future(channel).result(timeout=timeout)\n\t\texcept grpc.FutureTimeoutError:\n\t\t\tsys.exit(\'Error connecting to server\')\n\t\t{self.init_stubs()}'
        return init_func

    def write_imports(self):
        imports = ['from typing import Tuple,Iterator', 'import grpc',
                   'import sys', 'from functools import partial']
        for svc in self._services:
            imports.append(f'from . import {svc}_pb2_grpc as {svc}Service')
        for pkg in self._packages:
            pkg = pkg.split('/')[-1].split('.')[0]
            imports.append(f'from . import {pkg}_pb2 as {pkg}')

        return '\n'.join(imports)

    def write_services_classes(self):
        if self._services is not None:
            rpcs = []
            for svc in self._services:
                for rpc in self._services[svc]['methods']:
                    rpc_name = rpc['name']
                    description = rpc.get('description') if rpc.get('description') is not None else ''
                    rpc_in_type_pkg = rpc['inputType'].split('.')[1]
                    rpc_in_type = rpc['inputType'].split('.')[-1]
                    rpc_in_type = f'{rpc_in_type_pkg}.{rpc_in_type}'
                    rpc_out_type_pkg = rpc['outputType'].split('.')[1]
                    rpc_out_type = rpc['outputType'].split('.')[-1]
                    rpc_out_type = f'{rpc_out_type_pkg}.{rpc_out_type}'
                    in_open_type = 'Iterator[' if rpc.get(
                        'clientStreaming') is not None and rpc.get('clientStreaming') == True else ''
                    in_close_type = ']' if rpc.get('clientStreaming') is not None and rpc.get(
                        'clientStreaming') == True else ''
                    out_open_type = 'Iterator[' if rpc.get(
                        'serverStreaming') is not None and rpc.get('serverStreaming') == True else ''
                    out_close_type = ']' if rpc.get('serverStreaming') is not None and rpc.get(
                        'serverStreaming') == True else ''
                    rpcs.append(
                        f'def {rpc_name}_WithCall(self, request: {in_open_type}{rpc_in_type}{in_close_type}, metadata: Tuple[Tuple[str,str]] = ()) -> Tuple[{out_open_type}{rpc_out_type}{out_close_type}, grpc.Call]:\n\t\t"""webezyio - {description} Returns: RPC output and a call object"""\n\n\t\treturn self.{svc}Stub.{rpc_name}.with_call(request,metadata=metadata)')
                    rpcs.append(
                        f'def {rpc_name}(self, request: {in_open_type}{rpc_in_type}{in_close_type}, metadata: Tuple[Tuple[str,str]] = ()) -> {out_open_type}{rpc_out_type}{out_close_type}:\n\t\t"""webezyio - {description}"""\n\n\t\treturn self.{svc}Stub.{rpc_name}(request,metadata=metadata)')

            rpcs = '\n\n\t'.join(rpcs)
        return ''.join(rpcs)


class WZServicePy():
    """A helper class to write 'Python' language services for Webezy.io project services"""

    def __init__(self, project_package, name, imports=[], service=None, package=None, messages=[], enums=[], context: WZContext = None,wz_json: WZJson= None):
        self._name = name
        self._imports = imports
        self._service = service
        self._project_package = project_package
        self._context = context
        self._wz_json = wz_json

    def write_imports(self):
        if self._imports is not None:
            list_d = list(map(lambda i: i, _WELL_KNOWN_PY_IMPORTS))
            list_d.append(f'import {self._name}_pb2_grpc')
            for d in self._imports:
                name = d.split('.')[1]
                d_name = '{0}_pb2'.format(name)
                list_d.append(f'import {d_name}')

            list_d = '\n'.join(list_d)
            return f'{list_d}'
        else:
            return ''

    def write_class(self):
        rpcs = []
        functions = self._context.get_functions(self._name)
        if functions is not None:
            for func in functions:
                func_code = func['code']
                rpcs.append(
                    f'\t# @skip @@webezyio - DO NOT REMOVE\n{func_code}')

        for rpc in self._service.get('methods'):
            rpc_name = rpc.get('name')
            rpc_in_pkg = rpc.get('inputType').split('.')[1]
            rpc_in_name = rpc.get('inputType').split('.')[-1]
            rpc_out_pkg = rpc.get('outputType').split('.')[1]
            rpc_out_name = rpc.get('outputType').split('.')[-1]
            rpc_type_in = rpc.get('clientStreaming')
            rpc_type_out = rpc.get('serverStreaming')

            open_in_type = 'Iterator[' if rpc_type_in is not None and rpc_type_in == True else ''
            closing_in_type = ']' if rpc_type_in is not None and rpc_type_in == True else ''

            open_out_type = 'Iterator[' if rpc_type_out is not None and rpc_type_out == True else ''
            close_out_type = ']' if rpc_type_out is not None and rpc_type_out == True else ''
            code = ''
            if self._context is not None:
                code = self._context.get_rpc(self._name, rpc_name)
                if code is not None:
                    code =code.get('code')
                else:
                    if self._wz_json is not None:
                        fields = []
                        msg = self._wz_json.get_message(rpc.get('outputType'))
                        for f in msg.get('fields'):
                            fields.append('{0}=None'.format(f.get('name')))
                    fields = ','.join(fields)
                    if rpc_type_out:
                        out_prototype = f'\t\t# responses = [{rpc_out_pkg}_pb2.{rpc_out_name}({fields})]\n\t\t# for res in responses:\n\t\t#    yield res\n'
                    else:
                        out_prototype = f'\t\t# response = {rpc_out_pkg}_pb2.{rpc_out_name}({fields})\n\t\t# return response\n'
                    code = f'{out_prototype}\n\t\tsuper().{rpc_name}(request, context)\n\n'
            rpcs.append(
                f'\t# @rpc @@webezyio - DO NOT REMOVE\n\tdef {rpc_name}(self, request: {open_in_type}{rpc_in_pkg}_pb2.{rpc_in_name}{closing_in_type}, context: grpc.ServicerContext) -> {open_out_type}{rpc_out_pkg}_pb2.{rpc_out_name}{close_out_type}:\n{code}')
        rpcs = ''.join(rpcs)
        return f'class {self._name}({self._name}_pb2_grpc.{self._name}Servicer):\n\n{rpcs}'

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'"""Webezy.io service implemantation for -> {self._name}"""\nimport grpc\n{self.write_imports()}\n\n{self.write_class()}'

class WZServiceTs():
    """A helper class to write 'Typescript' language services for Webezy.io project services"""
    
    def __init__(self, project_package, name, imports=[], service=None, package=None, messages=[], enums=[], context: WZContext = None,wz_json: WZJson= None):
        self._name = name
        self._imports = imports
        self._service = service
        self._project_package = project_package
        self._context = context
        self._wz_json = wz_json

    def write_imports(self):
        if self._imports is not None:
            list_d = list(map(lambda i: i, _WELL_KNOWN_TS_IMPORTS))

            list_d.append(f'import {_OPEN_BRCK} {self._name}Server, {self._name}Service {_CLOSING_BRCK} from \'./protos/{self._name}\';')
            for d in self._imports:
                name = d.split('.')[1]
                d_name = '{0}'.format(name)
                list_d.append(f'import * as {d_name} from \'./protos/{d_name}\';')

            list_d = '\n'.join(list_d)
            return f'{list_d}'
        else:
            return ''

    def write_class(self):
        rpcs = []
        functions = self._context.get_functions(self._name)
        if functions is not None:
            for func in functions:
                func_code = func['code']
                rpcs.append(
                    f'\t// @skip @@webezyio - DO NOT REMOVE\n{func_code}')

        for rpc in self._service.get('methods'):
            rpc_name = rpc.get('name')
            rpc_in_pkg = rpc.get('inputType').split('.')[1]
            rpc_in_name = rpc.get('inputType').split('.')[-1]
            rpc_out_pkg = rpc.get('outputType').split('.')[1]
            rpc_out_name = rpc.get('outputType').split('.')[-1]
            rpc_type_in = rpc.get('clientStreaming') if rpc.get('clientStreaming') is not None else False
            rpc_type_out = rpc.get('serverStreaming') if rpc.get('serverStreaming') is not None else False
            
            handleType = 'handleUnaryCall'
            args = f'call: ServerUnaryCall<{rpc_in_pkg}.{rpc_in_name}, {rpc_out_pkg}.{rpc_out_name}>,\n\t\tcallback: sendUnaryData<{rpc_out_pkg}.{rpc_out_name}>'
            
            if rpc_type_in and rpc_type_out:
                handleType = 'handleBidiStreamingCall'
                args = f'call: ServerDuplexStream<{rpc_in_pkg}.{rpc_in_name}, {rpc_out_pkg}.{rpc_out_name}>'
            elif rpc_type_in and rpc_type_out == False:
                handleType = 'handleClientStreamingCall'
                args = f'call: ServerReadableStream<{rpc_in_pkg}.{rpc_in_name}, {rpc_out_pkg}.{rpc_out_name}>,\n\t\tcallback: sendUnaryData<{rpc_out_pkg}.{rpc_out_name}>'
            elif rpc_type_in == False and rpc_type_out:
                handleType = 'handleServerStreamingCall'
                args = f'call: ServerWritableStream<{rpc_in_pkg}.{rpc_in_name}, {rpc_out_pkg}.{rpc_out_name}>'
            code = ''
            if self._context is not None:
                code = self._context.get_rpc(self._name, rpc_name)
                if code is not None:
                    code =code.get('code')
            temp_name = rpc_name[0].lower() + rpc_name[1:]
            rpcs.append(
                f'\t// @rpc @@webezyio - DO NOT REMOVE\n\tpublic {temp_name}: {handleType}<{rpc_in_pkg}.{rpc_in_name}, {rpc_out_pkg}.{rpc_out_name}> = (\n\t\t{args}\n\t) => {_OPEN_BRCK}\n{code}\n\t{_CLOSING_BRCK}\n')
        rpcs = ''.join(rpcs)
        return f'\nclass {self._name} implements {self._name}Server, ApiType<UntypedHandleCall> {_OPEN_BRCK}\n\t[method: string]: any;\n\n{rpcs}\n\n{_CLOSING_BRCK}\n\nexport {_OPEN_BRCK}\n\t{self._name},\n\t{self._name}Service\n{_CLOSING_BRCK};'

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'{self.write_imports()}\n{self.write_class()}'


class WZClientTs():
    """A helper class to write 'Typescript' language clients for Webezy.io project services"""

    def __init__(self, project_package, services=None, packages=None, context: WZContext = None, config = None):
        self._services = services
        self._project_package = project_package
        self._context = context
        self._packages = packages
        self._config = config

    def __str__(self):
        return f'{self.write_imports()}\n{self.write_client_wrapper()}\n\n\t{self.write_services_classes()}\n{_CLOSING_BRCK}\n{self.write_client_exports()}'

    def write_client_exports(self):
        pkgs_list = []
        clients_list = []
        for key in self._packages:
            pkg = self._packages[key].get('name')
            pkgs_list.append(pkg)
        pkgs_list = ',\n\t'.join(pkgs_list)
        for key in self._services:
            clients_list.append(key+'Client')
        clients_list = ',\n\t'.join(clients_list)
        return f'export {_OPEN_BRCK}\n\t{pkgs_list},\n\t{clients_list}\n{_CLOSING_BRCK}' 

    def write_client_wrapper(self):
        return f'const _DEFAULT_OPTION = {_OPEN_BRCK}\n\t"grpc.keepalive_time_ms": 120000,\n\t"grpc.http2.min_time_between_pings_ms": 120000,\n\t"grpc.keepalive_timeout_ms": 20000,\n\t"grpc.http2.max_pings_without_data": 0,\n\t"grpc.keepalive_permit_without_calls": 1,\n{_CLOSING_BRCK}\n\nexport class {self._project_package} {_OPEN_BRCK}\n\n\t{self.init_wrapper()}'

    def init_stubs(self):
        stubs = []
        for svc in self._services:
            stubs.append(f'this.{svc}_client = new {svc}Client(`${_OPEN_BRCK}this.host{_CLOSING_BRCK}:${_OPEN_BRCK}this.port{_CLOSING_BRCK}`, credentials.createInsecure(),_DEFAULT_OPTION);')

        return '\n\t\t'.join(stubs)

    def args_stubs(self):
        stubs = []
        for svc in self._services:
            stubs.append(f'private readonly {svc}_client: {svc}Client;')

        return '\n\t'.join(stubs)

    def init_wrapper(self):
        if self._config is not None:
            host = self._config.get('host')
            port = self._config.get('port')

        else:
            host = 'localhost'
            port = 50051
        init_func = f'constructor(host: string = "{host}", port: number = {port}, metadata: Metadata = new Metadata()) {_OPEN_BRCK}\n\t\tthis.host = host;\n\t\tthis.port = port;\n\t\tthis.metadata = metadata;\n\t\t{self.init_stubs()}\n\t{_CLOSING_BRCK}\n\n\tprivate readonly metadata: Metadata;\n\tprivate readonly host: string;\n\tprivate readonly port: number;\n\t{self.args_stubs()}'
        return init_func

    def write_imports(self):
        imports = ['import { credentials, Metadata, ServiceError as _service_error, ClientUnaryCall, ClientDuplexStream, ClientReadableStream, ClientWritableStream } from \'@grpc/grpc-js\';',
                   'import { promisify } from \'util\';','import { Observable } from \'rxjs\';']
        for svc in self._services:
            imports.append(f'import {_OPEN_BRCK} {svc}Client {_CLOSING_BRCK} from \'./protos/{svc}\'')
        for pkg in self._packages:
            pkg = pkg.split('/')[-1].split('.')[0]
            imports.append(f'import * as {pkg} from \'./protos/{pkg}\'')

        return '\n'.join(imports)

    def write_services_classes(self):
        if self._services is not None:
            rpcs = []
            for svc in self._services:
                for rpc in self._services[svc]['methods']:
                    rpc_name = rpc['name']
                    rpc_in_type_pkg = rpc['inputType'].split('.')[1]
                    rpc_in_type = rpc['inputType'].split('.')[-1]
                    rpc_in_type = f'{rpc_in_type_pkg}.{rpc_in_type}'
                    rpc_out_type_pkg = rpc['outputType'].split('.')[1]
                    rpc_out_type = rpc['outputType'].split('.')[-1]
                    rpc_out_type = f'{rpc_out_type_pkg}.{rpc_out_type}'
                    rpc_output_type = rpc.get('serverStreaming') if rpc.get('serverStreaming') is not None else False
                    rpc_input_type = rpc.get('clientStreaming') if rpc.get('clientStreaming') is not None else False
                    
                    rpc_type = 'Unary' if rpc_output_type == False and rpc_input_type == False else 'Client Stream' if rpc_input_type == True and rpc_output_type == False  else 'Server Stream' if rpc_input_type == False and rpc_output_type == True else 'Bidi Stream' 
                    
                    rpc_description = rpc.get('description')
                    return_type_overload = 'ClientUnaryCall' if rpc_output_type == False and rpc_input_type == False else f'ClientDuplexStream<{rpc_in_type}, {rpc_out_type}>' if rpc_output_type == True and rpc_input_type == True else f'ClientReadableStream<{rpc_out_type}>' if rpc_output_type == True and rpc_input_type == False else f'ClientWritableStream<{rpc_in_type}>' if rpc_output_type == False and rpc_input_type == True else 'any'
                    return_type = f'Promise<{rpc_out_type}>' if rpc_output_type == False else f'Observable<{rpc_out_type}>'
                    temp_rpc_name = rpc_name[0].lower() + rpc_name[1:]
                    rpc_impl = f'if (callback === undefined) {_OPEN_BRCK}\n\t\t\treturn promisify<{rpc_in_type}, Metadata, {rpc_out_type}>(this.{svc}_client.{temp_rpc_name}.bind(this.{svc}_client))(request, metadata);\n\t\t{_CLOSING_BRCK} else {_OPEN_BRCK}\n\t\t return this.{svc}_client.{temp_rpc_name}(request, metadata, callback);\n\t\t{_CLOSING_BRCK}' if rpc_output_type == False and rpc_input_type == False else f'return this.{svc}_client.{temp_rpc_name}(metadata);' if rpc_output_type == True and rpc_input_type == True  else f'if (callback === undefined) {_OPEN_BRCK}\n\t\t\tcallback = (_error:_service_error | null , _response:{rpc_out_type}) => {_OPEN_BRCK}if (_error) throw _error; return _response{_CLOSING_BRCK}\n\t\t{_CLOSING_BRCK}\n\t\treturn this.{svc}_client.{temp_rpc_name}(metadata, callback);' if rpc_output_type == False and rpc_input_type == True else f'return new Observable(subscriber => {_OPEN_BRCK}\n\t\tconst stream = this.{svc}_client.{temp_rpc_name}(request, metadata);\n\t\t\tstream.on(\'data\', (res: {rpc_out_type}) => {_OPEN_BRCK}\n\t\t\t\tsubscriber.next(res)\n\t\t\t{_CLOSING_BRCK}).on(\'end\', () => {_OPEN_BRCK}\n\t\t\t\tsubscriber.complete()\n\t\t\t{_CLOSING_BRCK}).on(\'error\', (err: any) => {_OPEN_BRCK}\n\t\t\t\tsubscriber.error(err)\n\t\t\t\tsubscriber.complete()\n\t\t\t{_CLOSING_BRCK});\n\t\t{_CLOSING_BRCK})'
                    if rpc_output_type == False and rpc_input_type == True:
                        description = f'/**\n\t* @method {svc}.{rpc_name}\n\t* @description {rpc_description}\n\t* @kind {rpc_type}\n\t* @param metadata Metadata\n\t*/'
                        rpcs.append(
                            f'\n\t{description}\n\tpublic {rpc_name}(metadata?: Metadata): {return_type};\n\tpublic {rpc_name}(metadata: Metadata, callback: (error: _service_error | null, response: {rpc_out_type}) => void): {return_type_overload};\n\tpublic {rpc_name}(metadata: Metadata = this.metadata, callback?: (error: _service_error | null, response: {rpc_out_type}) => void): {return_type_overload} | {return_type} {_OPEN_BRCK}\n\t\t{rpc_impl}\n\t{_CLOSING_BRCK}')
                    elif rpc_output_type == True and rpc_input_type == True:
                        description = f'/**\n\t* @method {svc}.{rpc_name}\n\t* @description {rpc_description}\n\t* @kind {rpc_type}\n\t* @param request {rpc_in_type}\n\t* @param metadata Metadata\n\t*/'
                        rpcs.append(
                            f'\n\t{description}\n\tpublic {rpc_name}(metadata: Metadata = this.metadata): {return_type_overload} {_OPEN_BRCK}\n\t\t{rpc_impl}\n\t{_CLOSING_BRCK}')
                    else:
                        description_0 = f'/**\n\t* @method {svc}.{rpc_name}\n\t* @description {rpc_description}\n\t* @kind {rpc_type}\n\t* @param request {rpc_in_type}\n\t* @param metadata Metadata\n\t* @returns {return_type}\n\t*/'
                        description_1 = f'/**\n\t* @method {svc}.{rpc_name}\n\t* @description {rpc_description}\n\t* @kind {rpc_type}\n\t* @param request {rpc_in_type}\n\t* @param metadata Metadata\n\t* @param callback A callback function to be excuted once the server responds with {rpc_out_type}\n\t* @returns {return_type_overload}\n\t*/'
                        
                        rpcs.append(
                            f'\n\t{description_0}\n\tpublic {rpc_name}(request: {rpc_in_type}, metadata?: Metadata): {return_type};\n\t{description_1}\n\tpublic {rpc_name}(request: {rpc_in_type}, metadata: Metadata, callback: (error: _service_error | null, response: {rpc_out_type}) => void): {return_type_overload};\n\tpublic {rpc_name}(request: {rpc_in_type}, metadata: Metadata = this.metadata, callback?: (error: _service_error | null, response: {rpc_out_type}) => void): {return_type_overload} | {return_type} {_OPEN_BRCK}\n\t\t{rpc_impl}\n\t{_CLOSING_BRCK}')

            rpcs = '\n\n\t'.join(rpcs)
        return ''.join(rpcs)

class WZClientGo:
    """A helper class to write 'Go' language clients for Webezy.io project services"""

    def __init__(self, project_package, services=None, packages=None, context: WZContext = None, config = None,wz_json:WZJson=None):
        self._services = services
        self._project_package = project_package
        self._context = context
        self._packages = packages
        self._config = config
        self._wz_json = wz_json

    def __str__(self):
        return f'{self.write_imports()}{self.write_struct()}{self.write_new()}{self.write_methods()}'

    def write_imports(self):
        list_of_services = ['// Importing services']
        list_of_packages = ['// Importing packages']
        for s in self._services:
            list_of_services.append('"{}/services/protos/{}"'.format(self._wz_json.project.get('goPackage'),self._services[s].get('name')))
        for p in self._packages:
            list_of_packages.append('"{}/services/protos/{}"'.format(self._wz_json.project.get('goPackage'),self._packages[p].get('name')))

        _default_imports = ['"fmt"','"io"','"context"','"log"','"time"','"google.golang.org/grpc"','"google.golang.org/grpc/credentials/insecure"','"google.golang.org/grpc/metadata"','\n','\n\t'.join(list_of_services),'\n\t'.join(list_of_packages)]

        return 'package {}\n\nimport (\n\t{}\n)'.format(self._project_package,'\n\t'.join(_default_imports))

    def write_struct(self):
        client_options = ['host string // Host name should be a valid ip or domain',
                          'port int // Port that been served by the host',
                          'dialOpts []grpc.DialOption // Connection dial options',
                          'callOpts []grpc.CallOption // Connection call options',
                          'conn *grpc.ClientConn // A client connection object']
        for s in self._services:
            temp_svc = s[0].upper() + s[1:]
            temp_lower_svc = s.lower()
            client_options.append(f'{temp_lower_svc} {s}.{temp_svc}Client')
        return '\n\n// \'{0}\' represents the project services facing client side\ntype {0} struct {1}\n\t{2}\n{3}\n\n'.format(self._wz_json.project.get('packageName'),_OPEN_BRCK,'\n\t'.join(client_options),_CLOSING_BRCK)
    
    def write_new(self):
        _list_of_services_clients = []
        _temp_svc_list = []
        _list_of_client_opts = ['host string','port int','dialOpts []grpc.DialOption','callOpts []grpc.CallOption']
        _list_of_client_opts_none_types = []

        for i in _list_of_client_opts:
            _list_of_client_opts_none_types.append(i.split()[0])

        for s in self._services:
            temp_service = s[0].upper() + s[1:]
            _list_of_services_clients.append('{0}Client := {1}.New{2}Client(conn)'.format(s.lower(),s,temp_service))
            _temp_svc_list.append('{0}Client'.format(s.lower()))
        
        _new_client_init = ['\n\tlog.SetFlags(log.Lshortfile + log.Ltime)',
                            '\n\tsize := 1024 * 1024 * 50 // Max Recv / Send message 50MB as default',
                            '\n\tif len(dialOpts) == 0 {}\n\t\tdialOpts = append(dialOpts,\ngrpc.WithTransportCredentials(insecure.NewCredentials()),\ngrpc.WithDefaultCallOptions(\ngrpc.MaxCallRecvMsgSize(size),\ngrpc.MaxCallSendMsgSize(size),))\n\t{}'.format(_OPEN_BRCK,_CLOSING_BRCK),
                            '\n\tif host == "" {}\n\t\thost = defaultHost\n\t{}'.format(_OPEN_BRCK,_CLOSING_BRCK),
                            '\n\tif port == 0 {}\n\t\tport = defaultPort\n\t{}'.format(_OPEN_BRCK,_CLOSING_BRCK),
                            '// Dailing to client target\n\tconn, err := grpc.Dial(fmt.Sprintf("%s:%d", host, port), dialOpts...)',
                            'if err != nil {}\n\t\tlog.Fatalf("fail to dial: %v", err)\n\t{}'.format(_OPEN_BRCK,_CLOSING_BRCK),
                            '\n\t'.join(_list_of_services_clients),
                            'c := &{0}{1}{2}, conn, {3}{4}'.format(self._project_package,_OPEN_BRCK,', '.join(_list_of_client_opts_none_types),', '.join(_temp_svc_list),_CLOSING_BRCK),
                            'return c']
        default_client = '// Default returns the standard client used by the project-level services RPC\'s.\nfunc Defualt() *{} {} return std {}'.format(self._project_package,_OPEN_BRCK,_CLOSING_BRCK)
        return '// Initalize default constants\n\nvar defaultHost = "localhost"\nvar defaultPort = 50051\nvar defaultDialOpts []grpc.DialOption\nvar defaultCallOpts []grpc.CallOption\nvar std = New(defaultHost, defaultPort, defaultDialOpts, defaultCallOpts)\n{5}\n// Create new client stub\nfunc New({0}) *{1} {2}\n{3}\n{4}'.format(', '.join(_list_of_client_opts),self._project_package,_OPEN_BRCK,'\n\t'.join(_new_client_init),_CLOSING_BRCK,default_client)
    
    def write_methods(self):
        list_of_rpcs = []
        for s in self._services:
            svc = self._services[s]
            for r in svc.get('methods'):
                rpc_msg_in_pkg = r.get('inputType').split('.')[1]
                rpc_msg_input_type = r.get('inputType').split('.')[-1][0].upper() + r.get('inputType').split('.')[-1][1:]
                rpc_msg_out_pkg = r.get('outputType').split('.')[1]
                rpc_msg_output_type = r.get('outputType').split('.')[-1][0].upper() + r.get('outputType').split('.')[-1][1:]
                rpc_client_stream = r.get('clientStreaming') if r.get('clientStreaming') is not None else False
                rpc_server_stream = r.get('serverStreaming') if r.get('serverStreaming') is not None else False
                rpc_name = r.get('name')[0].upper() + r.get('name')[1:]
                # Unary
                if rpc_server_stream == False and rpc_client_stream == False:
                    list_of_rpcs.append('\n\n// [webezy.io] - {10}.{1}\n// Description: {9}\n// Read: https://www.webezy.io/docs/go/unary-call\nfunc (c *{0}) {1}(message *{2}.{3}) (*{7}.{8}, metadata.MD, metadata.MD) {4}\n\tlog.Printf("Calling {1} %v", message)\n\n\tctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)\n\n\tdefer cancel()\n\n\tvar header, trailer metadata.MD\n\n\tresponse, err := c.{5}.{1}(ctx, message, grpc.Header(&header), grpc.Trailer(&trailer))\n\n\tif err != nil {4}\n\t\tlog.Fatalf("Client call {1} failed: %v", err)\n\t{6}\n\n\treturn response, header, trailer\n{6}'.format(self._project_package,rpc_name,rpc_msg_in_pkg,rpc_msg_input_type,_OPEN_BRCK,s.lower(),_CLOSING_BRCK,rpc_msg_out_pkg,rpc_msg_output_type,r.get('description'),s))
                # Client stream
                elif rpc_client_stream == True and rpc_server_stream == False:
                    list_of_rpcs.append('\n\n// [webezy.io] - {10}.{1}\n// Description: {9}\n// Read: https://www.webezy.io/docs/go/client-stream\nfunc (c *{0}) {1}(messages []*{2}.{3}) *{7}.{8} {4}\n\tlog.Printf("Calling {1} %v", messages)\n\n\tctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)\n\n\tdefer cancel()\n\n\tstream, err := c.{5}.{1}(ctx)\n\n\tif err != nil {4}\n\t\tlog.Fatalf("Client call {1} failed: %v", err)\n\t{6}\n\n\tfor _, message := range messages {4}\n\t\tif err := stream.Send(message); err != nil {4}\n\t\t\tlog.Fatalf("Client sending message %v stream failed: %v", message, err)\n\t\t{6}\n\t{6}\n\tresponse, err := stream.CloseAndRecv()\n\tif err != nil {4}\n\t\tlog.Fatalf("Client stream failed on getting response: %v", err)\n\t{6}\n\n\treturn response\n{6}'.format(self._project_package,rpc_name,rpc_msg_in_pkg,rpc_msg_input_type,_OPEN_BRCK,s.lower(),_CLOSING_BRCK,rpc_msg_out_pkg,rpc_msg_output_type,r.get('description'),s))
                # Server stream
                elif rpc_client_stream == False and rpc_server_stream == True:
                    list_of_rpcs.append('\n\n// webezy.io - {10}.{1}\n// Description: {9}\n// Read: https://www.webezy.io/docs/go/server-stream\nfunc (c *{0}) {1}(message *{2}.{3}) []*{7}.{8} {4}\n\tlog.Printf("Calling {1} %v", message)\n\n\tctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)\n\n\tdefer cancel()\n\n\tstream, err := c.{5}.{1}(ctx, message)\n\n\tif err != nil {4}\n\t\tlog.Fatalf("Client call {1} failed: %v", err)\n\t{6}\n\n\tvar listResponses []*{7}.{8}\n\n\twaitc := make(chan struct{4}{6})\n\n\tgo func() {4}\n\t\tfor {4}\n\t\t\t{8}, err := stream.Recv()\n\t\t\tif err == io.EOF {4}\n\t\t\t\tclose(waitc)\n\t\t\t\tbreak\n\t\t\t{6}\n\t\t\tif err != nil {4}\n\t\t\t\tlog.Fatalf("Client call {1} stream message failed: %v", err)\n\t\t\t{6}\n\t\t\tlistResponses = append(listResponses, {8})\n\t\t{6}\n\t{6}()\n\t<-waitc\n\treturn listResponses\n{6}'.format(self._project_package,rpc_name,rpc_msg_in_pkg,rpc_msg_input_type,_OPEN_BRCK,s.lower(),_CLOSING_BRCK,rpc_msg_out_pkg,rpc_msg_output_type,r.get('description'),s))
                # BidiStream
                elif rpc_client_stream and rpc_server_stream:
                    list_of_rpcs.append('\n\n// webezy.io - {10}.{1}\n// Description: {9}\n// Read: https://www.webezy.io/docs/go/bidi-stream\nfunc (c *{0}) {1}(messages []*{2}.{3}) []*{7}.{8} {4}\n\tlog.Printf("Calling {1} %v", message)\n\n\tctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)\n\n\tdefer cancel()\n\n\tstream, err := c.{5}.{1}(ctx)\n\n\tif err != nil {4}\n\t\tlog.Fatalf("Client call {1} failed: %v", err)\n\t{6}\n\n\tvar listResponses []*{7}.{8}\n\n\twaitc := make(chan struct{4}{6})\n\n\tgo func() {4}\n\t\tfor {4}\n\t\t\t{8}, err := stream.Recv()\n\t\t\tif err == io.EOF {4}\n\t\t\t\tclose(waitc)\n\t\t\t\tbreak\n\t\t\t{6}\n\t\t\tif err != nil {4}\n\t\t\t\tlog.Fatalf("Client call {1} stream message failed: %v", err)\n\t\t\t{6}\n\t\t\tlistResponses = append(listResponses, {8})\n\t\t{6}\n\t{6}()\n\tfor _, message := range messages {4}\n\t\tif err := stream.Send(message); err != nil {4}\n\t\t\tlog.Fatalf("Client.{1} stream.Send(%v) failed: %v", message, err)\n\t\t{6}\n\t{6}\n\tstream.CloseSend()\n\t<-waitc\n\treturn listResponses\n{6}'.format(self._project_package,rpc_name,rpc_msg_in_pkg,rpc_msg_input_type,_OPEN_BRCK,s.lower(),_CLOSING_BRCK,rpc_msg_out_pkg,rpc_msg_output_type,r.get('description'),s))


        return '\n\n'.join(list_of_rpcs)

class WZServiceGo():
    """A helper class to write 'Go' language services for Webezy.io project services"""
    
    def __init__(self, project_package, name, imports=[], service=None, package=None, messages=[], enums=[], context: WZContext = None,wz_json: WZJson= None):
        self._name = name
        self._imports = imports
        self._service = service
        self._project_package = project_package
        self._context = context
        self._wz_json = wz_json

    def write_imports(self):
        if self._imports is not None:
            list_d = list(map(lambda i: i, _WELL_KNOWN_GO_IMPORTS))
            go_package_name = self._wz_json.project.get('goPackage')
            # list_d.append('codes "google.golang.org/grpc/codes"')
            # list_d.append('status "google.golang.org/grpc/status"')
            list_d.append(f'{self._name}Servicer "{go_package_name}/services/protos/{self._name}"')
            list_d.append(f'"{go_package_name}/services/utils"')

            for d in self._imports:
                name = d.split('.')[1]
                d_name = '{0}'.format(name)
                list_d.append(f'{d_name} "{go_package_name}/services/protos/{d_name}"')

            list_d = '\n\t'.join(list_d)
            return f'{list_d}'
        else:
            return ''

    def write_struct(self):
        temp_name = self._name[0].capitalize() + self._name[1:]
        return 'type {0} struct {1}\n\t{3}Servicer.Unimplemented{0}Server\n{2}'.format(temp_name,_OPEN_BRCK,_CLOSING_BRCK,self._name)

    def write_methods(self):
        temp_name = self._name[0].capitalize() + self._name[1:]
        list_of_rpcs = []
        for rpc in self._service.get('methods'):
            rpc_temp_name = rpc.get('name')[0].capitalize() + rpc.get('name')[1:]
            rpc_output_type = rpc.get('serverStreaming') if rpc.get('serverStreaming') is not None else False
            rpc_input_type = rpc.get('clientStreaming') if rpc.get('clientStreaming') is not None else False
            rpc_input_name = rpc.get('inputType').split('.')[3]
            rpc_input_package_name = rpc.get('inputType').split('.')[1]
            rpc_output_name = rpc.get('outputType').split('.')[3]
            rpc_output_package_name = rpc.get('outputType').split('.')[1]
            temp_go_rpc_input_name = rpc_input_name[0].capitalize() + rpc_input_name[1:]
            temp_go_rpc_output_name = rpc_output_name[0].capitalize() + rpc_output_name[1:]
            rpc_description = rpc.get('description')
            
            # Unary
            if rpc_output_type == False and rpc_input_type == False:
                list_of_rpcs.append('\n'.join([
                    f'\n\n// [webezy.io] - {self._name}.{rpc_temp_name} - {rpc_description}',
                    f'func ({self._name}Servicer *{temp_name}) {rpc_temp_name}(ctx context.Context, {rpc_input_name} *{rpc_input_package_name}.{temp_go_rpc_input_name}) (response *{rpc_output_package_name}.{temp_go_rpc_output_name}, err error) {_OPEN_BRCK}',
                    f'\tprintLog("{rpc_temp_name}",ctx, {rpc_input_name})',
                    f'\treturn &{rpc_output_package_name}.{temp_go_rpc_output_name}{_OPEN_BRCK}{_CLOSING_BRCK}, nil',
                    f'{_CLOSING_BRCK}'
                    ]))
            # Client stream
            elif rpc_input_type == True and rpc_output_type == False:
                list_of_rpcs.append('\n'.join([
                    f'\n\n// [webezy.io] - {self._name}.{rpc_temp_name} - {rpc_description}',
                    f'func ({self._name}Servicer *{temp_name}) {rpc_temp_name}(stream {self._name}Servicer.{temp_name}_{rpc_temp_name}Server) (err error) {_OPEN_BRCK}',
                    f'\tprintLog("{rpc_temp_name}",stream.Context(), nil)',
                    f'\tfor {_OPEN_BRCK}',
                    f'\t\tclientStreamRequest, err := stream.Recv()',
                    f'\t\tif err == io.EOF {_OPEN_BRCK}',
                    f'\t\t\tutils.ErrorLogger.Printf("[{rpc_temp_name}] Client stream closed.")',
                    f'\t\t\tbreak',
                    f'\t\t{_CLOSING_BRCK}',
                    f'\t\tif err != nil {_OPEN_BRCK}',
                    f'\t\t\tutils.ErrorLogger.Printf("[{rpc_temp_name}] Client stream Request error: \'%v\'.", err)',
                    f'\t\t\treturn stream.SendAndClose(&{rpc_output_package_name}.{temp_go_rpc_output_name}{_OPEN_BRCK}{_CLOSING_BRCK})',
                    f'\t\t{_CLOSING_BRCK}',
                    f'\t\t// Do something with incoming object',
                    f'\t\tutils.InfoLogger.Printf("[{rpc_temp_name}] Request received: \'%v\'.", clientStreamRequest)',
                    f'\t{_CLOSING_BRCK}',
                    f'\treturn stream.SendAndClose(&{rpc_output_package_name}.{temp_go_rpc_output_name}{_OPEN_BRCK}{_CLOSING_BRCK})',
                    f'{_CLOSING_BRCK}',
                ]))
            # Server stream
            elif rpc_input_type == False and rpc_output_type == True:
                list_of_rpcs.append('\n'.join([
                    f'\n\n// [webezy.io] - {self._name}.{rpc_temp_name} - {rpc_description}',
                    f'func ({self._name}Servicer *{temp_name}) {rpc_temp_name}({rpc_input_name} *{rpc_input_package_name}.{temp_go_rpc_input_name}, stream {self._name}Servicer.{temp_name}_{rpc_temp_name}Server) (err error) {_OPEN_BRCK}',
                    f'\tprintLog("{rpc_temp_name}",stream.Context(), nil)',
                    f'\t// Do loop for responses',
                    f'\treturn nil',
                    f'{_CLOSING_BRCK}',
                ]))
            # BidiStream
            elif rpc_input_type and rpc_output_type:

                list_of_rpcs.append('\n'.join([
                    f'\n\n// [webezy.io] - {self._name}.{rpc_temp_name} - {rpc_description}',
                    f'func ({self._name}Servicer *{temp_name}) {rpc_temp_name}(stream {self._name}Servicer.{temp_name}_{rpc_temp_name}Server) (err error) {_OPEN_BRCK}',
                    f'\tprintLog("{rpc_temp_name}",stream.Context(), nil)',
                    f'\tfor {_OPEN_BRCK}',
                    f'\t\tbidirectionalStreamRequest, err := stream.Recv()',
                    f'\t\tif err == io.EOF {_OPEN_BRCK}',
                    f'\t\t\tutils.ErrorLogger.Printf("[{rpc_temp_name}] Client stream closed.")',
                    f'\t\t\tbreak',
                    f'\t\t{_CLOSING_BRCK}',
                    f'\t\tif err != nil {_OPEN_BRCK}',
                    f'\t\t\tutils.ErrorLogger.Printf("[{rpc_temp_name}] Client stream Request error: \'%v\'.", err)',
                    f'\t\t\treturn stream.Send(&{rpc_output_package_name}.{temp_go_rpc_output_name}{_OPEN_BRCK}{_CLOSING_BRCK})',
                    f'\t\t{_CLOSING_BRCK}',
                    f'\t\t// Do something with incoming object',
                    f'\t\tutils.InfoLogger.Printf("[{rpc_temp_name}] Request received: \'%v\'.", bidirectionalStreamRequest)',
                    f'\t\tstream.Send(&{rpc_output_package_name}.{temp_go_rpc_output_name}{_OPEN_BRCK}{_CLOSING_BRCK})',
                    f'\t{_CLOSING_BRCK}',
                    '\treturn nil',
                    f'{_CLOSING_BRCK}'
                ]))
  
        return '\n'.join(list_of_rpcs)


    def write_log_func(self):
        return f'func printLog(name string, ctx context.Context, message interface{_OPEN_BRCK}{_CLOSING_BRCK}) {_OPEN_BRCK}\n\
\tcontextMetadata, _ := metadata.FromIncomingContext(ctx)\n\
\tutils.InfoLogger.Printf("[%s] Got RPC request: %v", name, message)\n\
\tutils.DebugLogger.Printf("[%s] Metadata: %v", name, contextMetadata)\n\
{_CLOSING_BRCK}'

    def to_str(self):
        return self.__str__()

    def __str__(self):
        temp_svc_name = self._name[0].capitalize() + self._name[1:]
        return f'package {temp_svc_name}\n\nimport (\n\t{self.write_imports()}\n)\n\n{self.write_struct()}\n{self.write_methods()}\n\n{self.write_log_func()}'


def parse_code_file(file_content, seperator='@rpc'):
    logging.debug(f"Parsing code file | seperator : {seperator}")
    # temp_lines = []
    # for lines in :
    #     drop_lines = False
    #     for line in lines:
    #         print(line)
    #         if nag in line:
    #             drop_lines = True

    #     if drop_lines == False:
    #         temp_lines.append(lines)

    return [list(g) for k, g in groupby(file_content, key=lambda x: seperator not in x) if k][1:]



def validation(answers, current):

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

def field_exists_validation(new_field, fields, msg):
    if new_field in fields:
        raise errors.WebezyProtoError(
            'Message', f'Field {new_field} already exits under {msg}')
    return True

def float_value_validate(answers, current):
    try:
        float(current)
    except Exception:
        raise inquirerErrors.ValidationError(
            current, reason='Value must be valid float type')
    return True

def int_value_validate(answers, current):
    try:
        int(current)
    except Exception:
        raise inquirerErrors.ValidationError(
            current, reason='Value must be valid integer type')
    return True



def enum_value_validate(answers, current):
    try:
        int(current)
    except Exception:
        raise errors.ValidationError(
            current, reason='Enum Value MUST be an integer value')
    return True

def send_analytic_event(args):
    stub = webezycore()
    ts = Timestamp()
    ts.GetCurrentTime()
    temp_args = []
    if hasattr(args, '__dict__'):
        for k in args.__dict__:
            temp_args.append(str((k,args.__dict__[k])))
    else:
        temp_args = [str((k, v)) for k, v in args.items()]
    hostname=socket.gethostname() 
    # pretty.print_info(temp_args)
    try:
        stub.PublishCLIEvent(
        WebezyAnalytics_pb2.CLIEvent(
            version=__version__.__version__,
            ts=ts,
            args=temp_args,
            os=platform() if hasattr(config,'token') == False else config.token.split(':')[0], 
            user_id='UNKNWON:'+hostname if hasattr(config,'token') == False else config.token+':'+hostname
            ))
    except Exception as e:
        pretty.print_warning(e)

_BUILTINS_TEMPLATES = Literal[
    "@webezyio/Blank",
    "@webezyio/SamplePy",
    "@webezyio/SampleTs",
    "@webezyio/PubSubTs",
    "@webezyio/HelloWorldPy",
    "@webezyio/HelloWorldTs"]

def attach_template(ARCHITECT,template:_BUILTINS_TEMPLATES):
    if template != '@webezyio/Blank':
        file_dir = os.path.dirname(__file__)
        template_domain_name = template.split('/')[0].split('@')[-1]
        template_name = template.split('/')[-1]
        pretty.print_note(file_dir + '/templates/{0}/{1}.template.py'.format(template_domain_name,template_name))
        os.chdir(ARCHITECT._path.split('webezy.json')[0])
        subprocess.run(['python',file_dir + '/templates/{0}/{1}.template.py'.format(template_domain_name,template_name),'--domain',ARCHITECT._domain,'--project-name',ARCHITECT._project_name])

def parse_extension_to_proto(
    extension_type:Literal['FileOptions','MessageOptions','FieldOptions','ServiceOptions','MethodOptions'],
    extension_message,ext_key,ext_value,wz_json):
    extension_value = None
    # Get current key to parse
    extension_field = next((f for f in extension_message.get('fields') if f.get('name') == ext_key.split('.')[-1]))
    # Get type and label for the extension field
    type_ext = extension_field.get(
        'fieldType').split('_')[-1].lower()
    label_ext = extension_field.get(
        'label').split('_')[-1].lower()
    # Handle FileOptions extensions
    if extension_type == 'FileOptions':
        if label_ext == 'repeated':
            pass
        else:
            extension_value = parse_extension_value(type_ext,ext_value,wz_json,extension_field)
            if extension_value is not None:
                extension_value = f'option ({ext_key}) = {extension_value};'
    
    elif extension_type == 'MessageOptions':
        if label_ext == 'repeated':
            pass
        else:
            extension_value = parse_extension_value(type_ext,ext_value,wz_json,extension_field,2)
            if extension_value is not None:
                extension_value = f'option ({ext_key}) = {extension_value};'
    
    elif extension_type == 'FieldOptions':
        if label_ext == 'repeated':
            pass
        else:
            extension_value = parse_extension_value(type_ext,ext_value,wz_json,extension_field,2)
            if extension_value is not None:
                extension_value = f'({ext_key}) = {extension_value}'
    elif extension_type == 'ServiceOptions':
        if label_ext == 'repeated':
            pass
        else:
            extension_value = parse_extension_value(type_ext,ext_value,wz_json,extension_field,2)
            if extension_value is not None:
                extension_value = f'option ({ext_key}) = {extension_value};'
    elif extension_type == 'MethodOptions':
        if label_ext == 'repeated':
            pass
        else:
            extension_value = parse_extension_value(type_ext,ext_value,wz_json,extension_field,2)
            if extension_value is not None:
                extension_value = f'option ({ext_key}) = {extension_value};'

    else:
        raise errors.WebezyValidationError('Extension Type Error','Extension of type {} is not valid !'.format(extension_type))

    return extension_value

def parse_extension_value(type,value,wz_json:WZJson,field=None,num_tabs=1):
    """
    This function serve as util for returning an extension proto value
    """
    if 'int' in type:
        value = int(value)
    elif type == 'float' or type == 'double':
        value = float(value)
    elif type == 'string':
        value = f'"{value}"'
    elif type == 'bool':
        if value == 0:
            value = "false"
        elif value == 1:
            value = "true"
    elif type == 'message':
        if field is not None:
            ext_msg = wz_json.get_message(field.get('messageType'))
            temp_values = []
            for k in value:
                field_in_ext = next((f for f in ext_msg.get('fields') if f.get('name') == k),None)
                if field_in_ext is not None:
                    field_ext_in_type = field_in_ext.get('fieldType').split('_')[-1].lower()
                    parsed_value_field = parse_extension_value(field_ext_in_type,value[k],wz_json,field_in_ext)
                    if parsed_value_field is not None:
                        temp_values.append('{} : {}'.format(k,parsed_value_field))
            if num_tabs > 1:
                value = ',\n\t\t'.join(temp_values)
                value = f'{_OPEN_BRCK}\n\t\t{value}\n\t{_CLOSING_BRCK}'
            else:
                value = ',\n\t'.join(temp_values)
                value = f'{_OPEN_BRCK}\n\t{value}\n{_CLOSING_BRCK}'
    elif type == 'enum':
        if isinstance(value,float) or isinstance(value,int):
            if value != 0:
                value = int(value)
            else:
                value = None
        else:
            if 'UNKNOWN' not in value:
                value = value
            else:    
                value = None

    return value