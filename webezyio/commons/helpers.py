import logging
from typing import Literal
from webezyio.commons.protos.webezy_pb2 import FieldDescriptor
from itertools import groupby

_WELL_KNOWN_PY_IMPORTS = ["from google.protobuf.timestamp_pb2 import Timestamp","from typing import Iterator"]

_FIELD_TYPES = Literal["TYPE_INT32", "TYPE_INT64", "TYPE_STRING", "TYPE_BOOL", "TYPE_MESSAGE", "TYPE_ENUM", "TYPE_DOUBLE", "TYPE_FLOAT", "TYPE_BYTE"]
_FIELD_LABELS = Literal["LABEL_OPTIONAL", "LABEL_REPEATED"]

_OPEN_BRCK = '{'
_CLOSING_BRCK = '}'

class WZField():

    def __init__(self,name,type:_FIELD_TYPES,label:_FIELD_LABELS,message_type=None,extensions=None) -> None:
        self._name = name 
        self._field_type = type
        self._label = label
        self._message_type = message_type
        self._extensions = extensions

    def setName(self,name):
        self._name = name

    def setType(self,type):
        self._field_type = type
    
    def setLabel(self,label):
        self._label = label
        
    def setMessageType(self,message_type):
        self._message_type = message_type

    def to_dict(self):
        temp = {}
        for k in dict(self.__dict__):
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

class WZEnumValue():

    def __init__(self,name,number:int) -> None:
        self._name = name 
        self._number = number

    def setName(self,name):
        self._name = name

    def setNumber(self,type):
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

class WZContext():

    def __init__(self, webezy_context):
        self._webezy_context = webezy_context
        self._parse_context()

    def _parse_context(self):
        self._files = self._webezy_context.get('files')

    def get_rpc(self,service,name):
        svc = next((svc for svc in self._files if svc['file'].split('/')[-1].split('.')[0] == service),None)
        if svc is not None:
            for rpc in svc['methods']:
                if rpc['name'] == name:
                    return rpc
        else:
            return svc

    def edit_rpc(self,service,name,new_context):
        rpc = self.get_rpc(service,name)
        rpc['code'] = new_context['code']
        rpc['type'] = new_context['type']
        rpc['name'] = new_context['name']

    def set_rpc_code(self,service,name,code):
        rpc = self.get_rpc(service,name)
        rpc['code'] = code
        rpc['type'] = 'rpc'
    
    def get_functions(self,service):
        svc = next((svc for svc in self._files if svc['file'].split('/')[-1].split('.')[0] == service),None)
        funcs = []
        if svc is not None:
            for func in svc['methods']:
                if func['type'] != 'rpc':
                    funcs.append(func) 
            return funcs
        else:
            return svc

    def set_method_code(self,service,name,code):
        file = next((f for f in self._files if service in f['file']), None)
        if file is not None:
            method = next((m for m in file['methods'] if m['name'] == name),None)
            if method is None:
                file['methods'].insert(0, {'name':name,'code':code,'type':'func'})
            else:
                method['code'] = code

    def dump(self):
        return self._webezy_context

    @property
    def files(self):
        return self._files

class WZJson():

    def __init__(self,webezy_json):
        self._webezy_json = webezy_json
        self._parse_json()

    def _parse_json(self):
        self._domain = self._webezy_json.get('domain')
        self._config = self._webezy_json.get('config')
        self._project = self._webezy_json.get('project')
        self._services = self._webezy_json.get('services')
        self._packages = self._webezy_json.get('packages')
        self._path = self._webezy_json.get('project').get('uri')

    def get_service(self,name):
        return self._services[name]

    def get_package(self,name):
        return self._packages[f'protos/v1/{name}.proto']

    def get_message(self,full_name):
        pkg_name = full_name.split('.')[1]
        msgs = self._packages[f'protos/v1/{pkg_name}.proto']['messages']
        return next((m for m in msgs if m['name'] == full_name.split('.')[-1]), None)

    def get_rpc(self,full_name):
        svc_name = full_name.split('.')[1]
        rpcs = self._services[svc_name]['methods']
        return next((r for r in rpcs if r['name'] == full_name.split('.')[-1]), None)
    
    def get_server_language(self):
        return self.project.get('server').get('language').lower()

    @property
    def domain(self):
        return self._domain

    @property
    def project(self):
        return self._project

    @property
    def services(self):
        return self._services
    
    @property
    def packages(self):
        return self._packages

    @property
    def path(self):
        return self._path

class WZProto():

    def __init__(self,name,imports=[],service=None,package=None,messages=[],enums=[]):
        self._name = name
        self._imports = imports
        self._service = service
        self._package = package
        self._messages = messages
        self._enums = enums

    def write_imports(self):
        if self._imports is not None:
            return '\n'.join(list(map(lambda imp: 'import "{0}.proto";'.format(imp.split('.')[1]), self._imports)))
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
                stream_in = 'stream ' if m.get('clientStreaming') is not None and m.get('clientStreaming') == True else ''
                stream_out = 'stream ' if m.get('serverStreaming') is not None and m.get('serverStreaming') == True else ''
                rpcs.append(f'rpc {rpc_name} ({stream_in}{msg_name_in}) returns ({stream_out}{msg_name_out});')
            rpcs = '\n\t'.join(rpcs)
            return f'service {self._name} {_OPEN_BRCK}\n\t{rpcs}\n{_CLOSING_BRCK}'
        else:
            return ''

    def write_messages(self):
        if len(self._messages) > 0:
            msgs = []
            for m in self._messages:
                msg_name = m.get('name')
                fields = []
                for f in m.get('fields'):
                    fLabel='' if f.get('label') == 'LABEL_OPTIONAL' else '{0} '.format(f.get('label').split('_')[-1].lower())
                    fType=f.get('fieldType').split('_')[-1].lower()
                    if fType == 'message':
                        fType = f.get('messageType')
                    elif fType == 'enum':
                        fType = f.get('enumType')
                    fName=f.get('name')
                    fIndex=f.get('index')
                    fOptions=''
                    fields.append(f'{fLabel}{fType} {fName} = {fIndex}{fOptions};')
                fields = '\n\t'.join(fields)
                msgs.append(f'message {msg_name} {_OPEN_BRCK}\n\t{fields}\n{_CLOSING_BRCK}\n')
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
                    value_number = 0 if v.get('number') is None else v.get('number')
                    values.append(f'{value_name} = {value_number};')
                values = '\n\t'.join(values)
                enums.append(f'enum {enum_name} {_OPEN_BRCK}\n\t{values}\n{_CLOSING_BRCK}\n')
            return '\n'.join(enums)

        else:
            return ''

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'// Webezy.io Generated proto DO NOT EDIT\nsyntax = "proto3";\n\n{self.write_imports()}\n{self.write_package()}\n\n{self.write_service()}\n\n{self.write_messages()}\n{self.write_enums()}'


class WZServicePy():

    def __init__(self,project_package,name,imports=[],service=None,package=None,messages=[],enums=[],context:WZContext=None):
        self._name = name
        self._imports = imports
        self._service = service
        self._project_package = project_package
        self._context = context

    def write_imports(self):
        if self._imports is not None:
            list_d = list(map(lambda i: i,_WELL_KNOWN_PY_IMPORTS))
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

        for func in self._context.get_functions(self._name):
            func_code = func['code']
            rpcs.append(f'\t# @skip @@webezyio - DO NOT REMOVE\n{func_code}')
        
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

            code = self._context.get_rpc(self._name,rpc_name).get('code')
            rpcs.append(f'\t# @rpc @@webezyio - DO NOT REMOVE\n\tdef {rpc_name}(self, request: {open_in_type}{rpc_in_pkg}_pb2.{rpc_in_name}{closing_in_type}, context) -> {open_out_type}{rpc_out_pkg}_pb2.{rpc_out_name}{close_out_type}:\n{code}')
        rpcs = ''.join(rpcs)
        return f'class {self._name}({self._name}_pb2_grpc.{self._name}Servicer):\n\n{rpcs}'

    def to_str(self):
        return self.__str__()

    def __str__(self):
        return f'{self.write_imports()}\n\n{self.write_class()}'

def parse_code_file(file_content,seperator='@rpc'):
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
        
        
    return [list(g) for k, g in groupby(file_content, key=lambda x: seperator not in x ) if k][1:]