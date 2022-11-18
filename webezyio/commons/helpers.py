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

from webezyio.core import webezycore,WebezyAnalytics_pb2
from webezyio.commons import errors, pretty
from webezyio.commons.resources import generate_package, generate_service
from webezyio.commons.errors import WebezyCoderError, WebezyValidationError
from webezyio.commons.file_system import check_if_file_exists, join_path
from webezyio.commons.protos.webezy_pb2 import FieldDescriptor, WebezyJson
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

_FIELD_TYPES = Literal["TYPE_INT32", "TYPE_INT64", "TYPE_STRING", "TYPE_BOOL",
                       "TYPE_MESSAGE", "TYPE_ENUM", "TYPE_DOUBLE", "TYPE_FLOAT", "TYPE_BYTE"]
_FIELD_LABELS = Literal["LABEL_OPTIONAL", "LABEL_REPEATED"]
_EXTENSIONS_TYPE = Literal["FileOptions", "MessageOptions", "FieldOptions"]

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

    def __init__(self, name, methods: List[WZRPC] = [], dependencies: List[str] = [], description=None) -> None:
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

    def to_tuple(self):
        rpcs = []
        for rpc in self._methods:
            rpcs.append(rpc.to_tuple())
        return self._name, rpcs, self._dependencies, self._description

    @property
    def name(self):
        return self._name


class WZMessage():
    """webezyio message level object that defines the required meta data properties."""

    def __init__(self, name, fields: List[WZField] = None, description: str = None, extension_type: _EXTENSIONS_TYPE = None) -> None:
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

    def setFields(self, fields: List[WZField]):
        self._fields = fields

    def to_tuple(self):
        if self._fields is None:
            raise WebezyValidationError(
                "Message", "Message must hold atleast 1 field !")

        f_array = []
        for f in self._fields:
            f_array.append(f.to_dict())

        return self._name, f_array, self._description, self._extension_type

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

    def __init__(self, name, enum_values: List[WZEnumValue] = [],description:str = '') -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.Enum` representation.

        Parameters
        ----------
            name (str): A enum name.
            enum_values (:module:`List[webezyio.commons.helpers.WZEnumValue]`): A list of enum values.
        """
        self._name = name
        self._enum_values = enum_values
        self._description = description

    def to_tuple(self):
        enums_values = []
        for ev in self._enum_values:
            enums_values.append(ev.to_dict())
        return self._name, enums_values, self._description

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

    def __init__(self, name, messages: List[WZMessage] = [], enums: List[WZEnum] = []):
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

    def to_tuple(self):
        messages = []
        enums = []
        for e in self._enums:
            enums.append(e.to_tuple())
        for m in self._messages:
            messages.append(m.to_tuple())
        return self._name, messages, enums

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
            return generate_package(self.path,self.domain,name,depend if depend is not None else [],msgs if msgs is not None else [],enums if enums is not None else [])


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
            list_fields = next((f for f in temp_msg.get('fields') if f.get('extensions') is not None),None)
            
        return list_fields

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

    def __init__(self, name, imports=[], service=None, package=None, messages=[], enums=[], description=None):
        self._name = name
        self._imports = imports
        self._service = service
        self._package = package
        self._messages = messages
        self._enums = enums
        self._description = description

    def write_imports(self):
        if self._imports is not None:
            temp_imports = []
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
            return ''

    def write_package(self):
        if self._package is not None:
            return f'package {self._package};'
        else:
            return ''

    def write_service(self):
        if self._service is not None:
            rpcs = []
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
                fields = []
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

                                # ext_pkg = next((pkg for pkg in self._package if pkg == 'protos/{0}/{1}.proto'.format(
                                #     ext.split('.')[2], ext.split('.')[1])),None)
                                # if ext_pkg is not None:
                                #     ext_msg = next((m for m in self._messages[ext_pkg] if m.get(
                                #         'name') == ext.split('.')[3]), None)
                                #     logging.debug(f'{list_names} | {ext_msg}')
                            else:
                                ext_msg = next((m for m in self._messages if m.get(
                                    'name') == ext.split('.')[0]), None)
                                logging.debug(f'{list_names} | {ext_msg}')
                            if ext_msg is None:
                                raise WebezyValidationError(
                                    'FieldOptions', f'Field Option [{ext}] specified for : "{fName}", is invalid !')
                            field = next((f for f in ext_msg.get(
                                'fields') if f.get('name') == list_names[-1]), None)
                            if field is None:
                                logging.error(
                                    f"Cant parse extension field [{f.get('fullName')}] {ext}")
                            else:
                                ext_v = f.get('extensions')[ext]
                                type_ext = field.get(
                                    'fieldType').split('_')[-1].lower()
                                label_ext = field.get(
                                    'label').split('_')[-1].lower()
                                if label_ext != 'repeated':
                                    if 'int' in type_ext:
                                        ext_v = int(ext_v)
                                    elif type_ext == 'float' or type_ext == 'double':
                                        ext_v = float(ext_v)
                                    elif type_ext == 'string':
                                        ext_v = f'"{ext_v}"'
                                    elif type_ext == 'bool':
                                        if ext_v == 0:
                                            ext_v = "false"
                                        elif ext_v == 1:
                                            ext_v = "true"
                                    elif type_ext == 'message':
                                        ext_msg = next((m for m in self._messages if m.get(
                                            'name') == field.get('messageType').split('.')[-1]), None)
                                        temp_v_list = []
                                        for k in ext_v:
                                            field_in_ext = next((f for f in ext_msg.get('fields') if f.get('name') == k),None)
                                            if field_in_ext is not None:
                                                field_ext_in_type = field_in_ext.get('fieldType').split('_')[-1].lower()
                                                if 'int' in field_ext_in_type:
                                                    temp_v = int(ext_v[k])
                                                elif field_ext_in_type == 'float' or field_ext_in_type == 'double':
                                                    temp_v = float(ext_v[k])
                                                elif field_ext_in_type == 'string':
                                                    temp_v = f'"{ext_v[k]}"'
                                                elif field_ext_in_type == 'bool':
                                                    if ext_v[k] == 0:
                                                        temp_v = "false"
                                                    elif ext_v[k] == 1:
                                                        temp_v = "true"
                                                temp_v_list.append('{0} : {1}'.format(k,temp_v))
                                                
                                        joined_fields = ','.join(temp_v_list)
                                        ext_v = f'{_OPEN_BRCK}{joined_fields}{_CLOSING_BRCK}'
                                        pretty.print_note(ext_v)
                                        # joined_fields = ','.join(temp_v_list)
                                        # ext_v = f'{_OPEN_BRCK}{}{_CL/OSING_BRCK}
                                
                                if label_ext == 'repeated':
                                    for v in ext_v:
                                        if 'int' in type_ext:
                                            temp_v = int(v)
                                        elif type_ext == 'float' or type_ext == 'double':
                                            temp_v = float(v)
                                        elif type_ext == 'string':
                                            temp_v = f'"{v}"'
                                        elif type_ext == 'bool':
                                            if v == 0:
                                                temp_v = "false"
                                            elif v == 1:
                                                temp_v = "true"
                                        elif type_ext == 'message':
                                            # if self._package not in field.get('messageType'):
                                            ext_msg = next((m for m in self._messages if m.get(
                                                'name') == field.get('messageType').split('.')[-1]), None)
                                            temp_v_list = []
                                            if ext_msg is not None:
                                                for value_nested in v:

                                                    field_in_ext = next((f for f in ext_msg.get('fields') if f.get('name') == value_nested),None)
                                                    if field_in_ext is not None:
                                                        field_ext_in_type = field_in_ext.get('fieldType').split('_')[-1].lower()
                                                        if 'int' in field_ext_in_type:
                                                            temp_v = int(v[value_nested])
                                                        elif field_ext_in_type == 'float' or field_ext_in_type == 'double':
                                                            temp_v = float(v[value_nested])
                                                        elif field_ext_in_type == 'string':
                                                            temp_v = f'"{v[value_nested]}"'
                                                        elif field_ext_in_type == 'bool':
                                                            if v[value_nested] == 0:
                                                                temp_v = "false"
                                                            elif v[value_nested] == 1:
                                                                temp_v = "true"
                                                        temp_v_list.append('{0} : {1}'.format(value_nested,temp_v))
                                                joined_fields = ','.join(temp_v_list)
                                                temp_v = f'{_OPEN_BRCK}{joined_fields}{_CLOSING_BRCK}'
                                            else:
                                                pretty.print_error("Canot parse extension values for {} because it is nested message from another package please move {} to current package {}".format(value_nested,field.get('messageType'),self._package))
                                        elif type_ext == 'enum':
                                            temp_v = v
                                            # pretty.print_info(self._enums)
                                        else:
                                            pretty.print_warning("Not supported parsing of: {} for extension values".format(type_ext))
                                        fOptions.append(f'\n\t\t({ext}) = {temp_v}')

                                else:
                                    fOptions.append(f'({ext}) = {ext_v}')
                        fOptions = ','.join(fOptions)
                    fOptions = f' [{fOptions}]' if len(fOptions) > 0 else ''
                    fDesc = f.get('description')
                    if ext_type == 'FieldOptions':
                        fDesc = f'// [webezyio] - {fDesc}\n\t\t' if fDesc is not None else ''
                    else:
                        fDesc = f'// [webezyio] - {fDesc}\n\t' if fDesc is not None else ''
                    if f.get('fieldType') == 'TYPE_ONEOF':
                        fields.append(
                            f'{fDesc}{fType}')
                    else:
                        fields.append(
                            f'{fDesc}{fLabel}{fType} {fName} = {fIndex}{fOptions};')

                if ext_type == 'FieldOptions':
                    fields = '\n\t\t'.join(fields)
                    msgs.append(
                        f'// [webezyio] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\textend google.protobuf.FieldOptions {_OPEN_BRCK}\n\t\t{fields}\n\t{_CLOSING_BRCK}\n{_CLOSING_BRCK}\n')
                elif ext_type == 'MessageOptions':
                    logging.error(f"{ext_type} Not supported at the moment!")
                else:
                    fields = '\n\t'.join(fields)
                    msgs.append(
                        f'// [webezyio] - {m_desc}\nmessage {msg_name} {_OPEN_BRCK}\n\t{fields}\n{_CLOSING_BRCK}\n')

            msgs = '\n'.join(msgs)
            return msgs
        else:
            return ''

    def write_enums(self):
        if self._enums is not None:
            enums = []
            for e in self._enums:
                enum_name = e.get('name')
                enum_full_name = e.get('full_name')
                values = []
                for v in e.get('values'):
                    value_name = v.get('name')
                    value_number = 0 if v.get(
                        'number') is None else v.get('number')
                    v_desc = v.get('description')
                    values.append(f'// [webezyio] - {v_desc}\n\t{value_name} = {value_number};')
                values = '\n\t'.join(values)
                e_desc = e.get('description')
                enums.append(
                    f'// [webezyio] - {e_desc}\nenum {enum_name} {_OPEN_BRCK}\n\t{values}\n{_CLOSING_BRCK}\n')
            return '\n'.join(enums)

        else:
            return ''

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'// Webezy.io Generated proto DO NOT EDIT\nsyntax = "proto3";\n\n{self.write_imports()}\n{self.write_package()}\n\n{self.write_service()}\n\n{self.write_messages()}\n{self.write_enums()}'


class WZClientPy():

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