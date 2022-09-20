import logging
import os
from typing import List, Literal
from webezyio.commons.resources import generate_package, generate_service
from webezyio.commons.errors import WebezyCoderError, WebezyValidationError
from webezyio.commons.file_system import check_if_file_exists, join_path
from webezyio.commons.protos.webezy_pb2 import FieldDescriptor, WebezyJson
from itertools import groupby
from google.protobuf.struct_pb2 import Value
from google.protobuf.json_format import ParseDict, MessageToDict
from google.protobuf import text_format

_WELL_KNOWN_PY_IMPORTS = [
    "from google.protobuf.timestamp_pb2 import Timestamp", "from typing import Iterator"]

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


def wzJsonToMessage(wz_json) -> WebezyJson:
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

    def __init__(self, name, type: _FIELD_TYPES, label: _FIELD_LABELS, message_type=None, enum_type=None, extensions=None, description=None) -> None:
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
        for k in dict(self.__dict__):
            if k == '_extensions':
                if dict(self.__dict__)[k] is not None:
                    temp[k[1:]] = {}
                    for j in dict(self.__dict__)[k]:
                        if isinstance(dict(self.__dict__)[k][j], str):
                            temp[k[1:]][j] = Value(
                                string_value=dict(self.__dict__)[k][j])
                        elif isinstance(dict(self.__dict__)[k][j], int):
                            temp[k[1:]][j] = Value(
                                number_value=dict(self.__dict__)[k][j])
                        elif isinstance(dict(self.__dict__)[k][j], bool):
                            temp[k[1:]][j] = Value(
                                bool_value=dict(self.__dict__)[k][j])
            else:
                temp[k[1:]] = dict(self.__dict__)[k]

        return temp

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

    def __init__(self, name, in_type, out_type, client_stream=False, server_stream=False, description=None) -> None:
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

    def __init__(self, name: str, number: int) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.EnumValue` representation.

        Parameters
        ----------
            name (str): A enum key.
            number (int): A enum value.
        """
        self._name = name
        self._number = number

    def setName(self, name):
        self._name = name

    def setNumber(self, type):
        self._field_type = type

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

    def __init__(self, name, enum_values: List[WZEnumValue] = []) -> None:
        """Parses a fields into a :module:`webezyio.commons.protos.webezy_pb2.Enum` representation.

        Parameters
        ----------
            name (str): A enum name.
            enum_values (:module:`List[webezyio.commons.helpers.WZEnumValue]`): A list of enum values.
        """
        self._name = name
        self._enum_values = enum_values

    def to_tuple(self):
        enums_values = []
        for ev in self._enum_values:
            enums_values.append(ev.to_dict())
        return self._name, enums_values

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
            return self._services[name]
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
            if options is not None:
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
                    fLabel = '' if f.get('label') == 'LABEL_OPTIONAL' else '{0} '.format(
                        f.get('label').split('_')[-1].lower())
                    fType = f.get('fieldType').split('_')[-1].lower()
                    if fType == 'message':
                        fType = f.get('messageType')
                    elif fType == 'enum':
                        fType = f.get('enumType')
                    fName = f.get('name')
                    fIndex = f.get('index')
                    fOptions = []
                    if f.get('extensions') is not None:
                        for ext in f.get('extensions'):
                            list_names = ext.split('.')
                            if len(list_names) > 2:
                                ext_pkg = next((pkg for pkg in self._package if pkg == 'protos/{0}/{1}.proto'.format(
                                    ext.split('.')[2], ext.split('.')[1])))
                                if ext_pkg is not None:
                                    ext_msg = next((m for m in self._messages[ext_pkg] if m.get(
                                        'name') == ext.split('.')[3]), None)
                                    logging.debug(f'{list_names} | {ext_msg}')
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
                                fOptions.append(f'({ext}) = {ext_v}')
                        fOptions = ','.join(fOptions)
                    fOptions = f' [{fOptions}]' if len(fOptions) > 0 else ''
                    fDesc = f.get('description')
                    if ext_type == 'FieldOptions':
                        fDesc = f'// [webezyio] - {fDesc}\n\t\t' if fDesc is not None else ''
                    else:
                        fDesc = f'// [webezyio] - {fDesc}\n\t' if fDesc is not None else ''
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
                    values.append(f'{value_name} = {value_number};')
                values = '\n\t'.join(values)
                enums.append(
                    f'enum {enum_name} {_OPEN_BRCK}\n\t{values}\n{_CLOSING_BRCK}\n')
            return '\n'.join(enums)

        else:
            return ''

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'// Webezy.io Generated proto DO NOT EDIT\nsyntax = "proto3";\n\n{self.write_imports()}\n{self.write_package()}\n\n{self.write_service()}\n\n{self.write_messages()}\n{self.write_enums()}'


class WZClientPy():

    def __init__(self, project_package, services=None, packages=None, context: WZContext = None):

        self._services = services
        self._project_package = project_package
        self._context = context
        self._packages = packages

    def __str__(self):

        return f'{self.write_imports()}\n{self.write_client_wrapper()}\n\n\t{self.write_services_classes()}'

    def write_client_wrapper(self):
        return f'\nclass {self._project_package}:\n\n\t{self.init_wrapper()}'

    def init_stubs(self):
        stubs = []
        for svc in self._services:
            stubs.append(f'self.{svc}Stub = {svc}Service.{svc}Stub(channel)')

        return '\n\t\t'.join(stubs)

    def init_wrapper(self):
        init_func = f'def __init__(self, host, port, timeout=10):\n\t\tchannel = grpc.insecure_channel(\'{_OPEN_BRCK}0{_CLOSING_BRCK}:{_OPEN_BRCK}1{_CLOSING_BRCK}\'.format(host, port))\n\t\ttry:\n\t\t\tgrpc.channel_ready_future(channel).result(timeout=10)\n\t\texcept grpc.FutureTimeoutError:\n\t\t\tsys.exit(\'Error connecting to server\')\n\t\t{self.init_stubs()}'
        return init_func

    def write_imports(self):
        imports = ['from typing import Tuple,Iterator', 'import grpc',
                   'import sys', 'from functools import partial']
        for svc in self._services:
            imports.append(f'import {svc}_pb2_grpc as {svc}Service')
        for pkg in self._packages:
            pkg = pkg.split('/')[-1].split('.')[0]
            imports.append(f'import {pkg}_pb2 as {pkg}')

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
                    rpc_out_type_pkg = rpc['inputType'].split('.')[1]
                    rpc_out_type = rpc['inputType'].split('.')[-1]
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
                        f'def {rpc_name}(self, request: {in_open_type}{rpc_in_type}{in_close_type}, metadata: Tuple[Tuple[str,str]]) -> {out_open_type}{rpc_out_type}{out_close_type}:\n\t\t"""webezyio"""\n\n\t\treturn self.{svc}Stub.{rpc_name}(request,metadata=metadata)')

            rpcs = '\n\n\t'.join(rpcs)
        return ''.join(rpcs)


class WZServicePy():

    def __init__(self, project_package, name, imports=[], service=None, package=None, messages=[], enums=[], context: WZContext = None):
        self._name = name
        self._imports = imports
        self._service = service
        self._project_package = project_package
        self._context = context

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
                    code = '\t\tpass\n\n'
            rpcs.append(
                f'\t# @rpc @@webezyio - DO NOT REMOVE\n\tdef {rpc_name}(self, request: {open_in_type}{rpc_in_pkg}_pb2.{rpc_in_name}{closing_in_type}, context) -> {open_out_type}{rpc_out_pkg}_pb2.{rpc_out_name}{close_out_type}:\n{code}')
        rpcs = ''.join(rpcs)
        return f'class {self._name}({self._name}_pb2_grpc.{self._name}Servicer):\n\n{rpcs}'

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'{self.write_imports()}\n\n{self.write_class()}'


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
