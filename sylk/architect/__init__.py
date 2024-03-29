# Copyright (c) 2023 sylk.build

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

from enum import Enum
import logging
from sylk.commons.errors import SylkProtoError
from sylk.commons.file_system import join_path
from sylk.commons.pretty import print_error, print_info, print_note

from sylk.commons.protos import SylkClient_pb2,SylkServer_pb2,SylkProject_pb2
from google.protobuf.json_format import MessageToDict
from sylk.commons.resources import generate_enum, generate_message, generate_package, generate_project,\
                                     generate_rpc, generate_service

from sylk.architect.recievers import Builder
from sylk.architect.commands import AddResource, EditResource, InitProject,\
                                    Logger,RemoveResource, SetDomain
from sylk.architect.invoker import Sylk

logging.basicConfig(
    level='INFO',
    format='%(asctime)s - [%(filename)10s] - %(funcName)10s() - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

class CommandMap(Enum):
    _REMOVE_RESOURCE = "RemoveResource"
    _EDIT_RESOURCE = "EditResource"
    _ADD_RESOURCE = "AddResource"
    _SET_DOMAIN = "SetDomain"
    _SET_CONFIG = "SetConfig"


class SylkArchitect():

    def __init__(self,path,domain='domain',project_name='project',save=None) -> None:
        logging.info("Starting sylk.build architect process")
        if 'sylk.json' not in path:
            raise SylkProtoError('sylk.json file path is not valid','Make sure you pass in your architect class the right path to your sylk.json file')
        self._path = path
        self._project = None
        self._domain = domain
        self._project_name = project_name
        self._builder = Builder()
        self._remove_resource = RemoveResource(self._builder)
        self._edit_resource = EditResource(self._builder)
        self._add_resource = AddResource(self._builder)
        self._logger = Logger(self._builder)
        self._set_domain = SetDomain(self._builder)
        self._sylk = Sylk(self._path,save)
        self._sylk.registerCommand(CommandMap._REMOVE_RESOURCE,self._remove_resource)
        self._sylk.registerCommand(CommandMap._EDIT_RESOURCE,self._edit_resource)
        self._sylk.registerCommand(CommandMap._ADD_RESOURCE,self._add_resource)
        self._sylk.registerHook(CommandMap._ADD_RESOURCE,'log',self._logger)

    def SetDomain(self,domain):
        self._domain = domain
        self._sylk.execute(CommandMap._ADD_RESOURCE, {'organization': { 'domain' : domain }})
    
    def SetConfig(self,config):
        self._sylk.execute(CommandMap._ADD_RESOURCE, { 'config' : config })

    def AddProject(self,name=None,server_language=SylkServer_pb2.ServerLanguages.Name(SylkServer_pb2.python),clients=[]) -> SylkProject_pb2.SylkProject:
        name = name if name is not None else self._project_name
        dict = generate_project(self._path,name,server_language,clients,json=True)
        project = generate_project(self._path,name,server_language,clients)
        self._sylk.execute(CommandMap._ADD_RESOURCE,{'project':dict})
        self._project = project
        return project
    
    def AddClient(self):
        pass

    def AddService(self,name,dependencies,description,methods,extensions=None):
        dict = generate_service(self._path,self._domain,name,self._sylk.sylkJson.get('project')['server']['language'],dependencies=dependencies,description=description,extensions=extensions,json=True,methods=methods,sylk_json=self._sylk.sylkJson) 
        service = generate_service(self._path,self._domain,name,self._sylk.sylkJson.get('project')['server']['language'],dependencies=dependencies,description=description,extensions=extensions,methods=methods,sylk_json=self._sylk.sylkJson)
        services = self._sylk.sylkJson.get('services') if self._sylk.sylkJson.get('services') is not None else {} 
        services[name] = dict
        self._sylk.execute(CommandMap._ADD_RESOURCE,{'services': services })
        return service

    def AddRPC(self,service,name,*args):
        service_name = service.name
        _IN = args[0][0]
        _OUT = args[0][1]
        RPC = generate_rpc(self._path,name,_IN[0],_OUT[0],_IN[1],_OUT[1],args[1])
        service.methods.append(RPC)
        
        in_package = '.'.join(_IN[1].split('.')[:-1])
        out_package = '.'.join(_OUT[1].split('.')[:-1])

        if in_package not in service.dependencies:
            service.dependencies.append(in_package)
        if out_package not in service.dependencies:
            service.dependencies.append(out_package)
        self._sylk.execute(CommandMap._ADD_RESOURCE,{'services': { service_name : MessageToDict(service) } })

    def AddPackage(self,name,dependencies=[],messages=[],description=None,domain=None,extensions=None):
        dict = generate_package(self._path,self._domain if domain is None else domain,name,dependencies=dependencies,messages=messages,description=description,extensions=extensions,json=True,sylk_json=self._sylk.sylkJson)
        package = generate_package(self._path,self._domain if domain is None else domain,name,dependencies=dependencies,messages=messages,description=description,extensions=extensions,sylk_json=self._sylk.sylkJson)
        self._sylk.execute(CommandMap._ADD_RESOURCE,{'packages': { f'protos/v1/{name}.proto' : dict } })
        return package

    def AddMessage(self,package,name,fields,description=None,options=None,extensions=None,domain=None):
        message = generate_message(self._path,self._domain if domain is None else domain,package,name,fields,option=options,description=description,extensions=extensions,sylk_json=self._sylk.sylkJson)
        print(package)
        if next((m for m in package.messages if m.name == message.name), None) is None:
            package.messages.append(message)
            self._sylk.execute(CommandMap._ADD_RESOURCE,{'packages':{f'protos/v1/{package.name}.proto': MessageToDict(package)}})
            return message
        else:
            logging.error(f"Cannot create message '{message.name}' already exists under '{package.name}' package")
        return message
        
    def AddEnum(self,package,name,enum_values,description=None,domain=None):
        enum = generate_enum(self._path,self._domain if domain is None else domain,package.name,name,enum_values,description=description)
        package.enums.append(enum)
        self._sylk.execute(CommandMap._ADD_RESOURCE,{'packages':{f'protos/v1/{package.name}.proto': MessageToDict(package)}})
        return enum

    def EditService(self,name,dependencies,description,methods,extensions=None):
        service = generate_service(self._path,self._domain,name,self._sylk.sylkJson.get('project')['server']['language'],dependencies=dependencies,description=description,methods=methods,extensions=extensions,sylk_json=self._sylk.sylkJson)
        self._sylk.execute(CommandMap._EDIT_RESOURCE,MessageToDict(service))
        return service

    def EditPackage(self,name,dependencies=[],messages=[],enums=[],description=None,extensions=None):
        package = generate_package(self._path,self._domain,name,dependencies=dependencies,messages=messages,description=description,enums=enums,extensions=extensions,sylk_json=self._sylk.sylkJson)
        self._sylk.execute(CommandMap._EDIT_RESOURCE,MessageToDict(package))
        return package

    def EditMessage(self,package,name,fields,description=None,options=None,old_name=None,extensions=None):
        message = generate_message(self._path,self._domain,package,name,fields,option=options,description=description,extensions=extensions,sylk_json=self._sylk.sylkJson)
        self._sylk.execute(CommandMap._EDIT_RESOURCE,MessageToDict(message),old_name=old_name)
        return message

    def EditEnum(self,package,name,enum_values):
        enum = generate_enum(self._path,self._domain,package.name,name,enum_values)
        self._sylk.execute(CommandMap._EDIT_RESOURCE,MessageToDict(enum))
    
    def EditRPC(self,service,name,input_type,output_type,client_stream,server_stream,description,extensions=None):
        RPC = generate_rpc(self._path,name,client_stream,server_stream,input_type,output_type,description)
        self._sylk.execute(CommandMap._EDIT_RESOURCE,MessageToDict(RPC))

    def RemoveEnum(self,full_name):
        self._sylk.execute(CommandMap._REMOVE_RESOURCE,full_name)
    
    def RemoveMessage(self,full_name):
        self._sylk.execute(CommandMap._REMOVE_RESOURCE,full_name)

    def RemoveRpc(self, full_name):
        self._sylk.execute(CommandMap._REMOVE_RESOURCE,full_name)

    def RemoveField(self, full_name):
        self._sylk.execute(CommandMap._REMOVE_RESOURCE,full_name)

    def RemoveOneofField(self, full_name):
        self._sylk.execute(CommandMap._REMOVE_RESOURCE,full_name)
        
    def RemoveEnumValue(self, full_name):
        self._sylk.execute(CommandMap._REMOVE_RESOURCE,full_name)


    def Save(self):
        logging.info("Saving sylk.build architect process")

        self._sylk.save()

    def undo(self):
        self._sylk.undo()

    def redo(self):
        self._sylk.redo()