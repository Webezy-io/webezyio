from enum import Enum
import logging

from webezyio.commons.protos.webezy_pb2 import PackageDescriptor
from google.protobuf.json_format import MessageToDict
from webezyio.commons.resources import generate_enum, generate_message, generate_package, generate_project,\
                                     generate_rpc, generate_service

from webezyio.architect.recievers import Builder
from webezyio.architect.commands import AddResource, InitProject,\
                                    Logger,RemoveResource, SetDomain
from webezyio.architect.invoker import Webezy

logging.basicConfig(
    level='INFO',
    format='%(asctime)s - [%(filename)10s] - %(funcName)10s() - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

class CommandMap(Enum):
    _ADD_RESOURCE = "AddResource"
    _SET_DOMAIN = "SetDomain"
    _SET_CONFIG = "SetConfig"


class WebezyArchitect():

    def __init__(self,path,domain='domain',project_name='project') -> None:
        logging.info("Starting webezyio architect process")
        self._path = path
        self._domain = domain
        self._project_name = project_name

        self._builder = Builder()
        self._add_resource = AddResource(self._builder)
        self._logger = Logger(self._builder)
        self._set_domain = SetDomain(self._builder)
        self._webezy = Webezy(self._path)
        self._webezy.registerCommand(CommandMap._ADD_RESOURCE,self._add_resource)
        self._webezy.registerHook(CommandMap._ADD_RESOURCE,'log',self._logger)

    def SetDomain(self,domain):
        self._domain = domain
        self._webezy.execute(CommandMap._ADD_RESOURCE, {'domain':domain})
    
    def SetConfig(self,config):
        self._webezy.execute(CommandMap._ADD_RESOURCE, {'config':config})

    def AddProject(self,name=None,server_language='python',clients=[]):
        name = name if name is not None else self._project_name
        dict = generate_project(self._path,name,server_language,clients,json=True)
        project = generate_project(self._path,name,server_language,clients)
        self._webezy.execute(CommandMap._ADD_RESOURCE,{'project':dict})
        return project
    
    def AddClient(self):
        pass

    def AddService(self,name,dependencies):
        dict = generate_service(self._path,self._domain,name,self._webezy.webezyJson.get('project')['server']['language'],dependencies=dependencies,json=True) 
        service = generate_service(self._path,self._domain,name,self._webezy.webezyJson.get('project')['server']['language'],dependencies=dependencies)
        self._webezy.execute(CommandMap._ADD_RESOURCE,{'services': { name : dict } })
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
        self._webezy.execute(CommandMap._ADD_RESOURCE,{'services': { service_name : MessageToDict(service) } })

    def AddPackage(self,name,dependencies):
        dict = generate_package(self._path,self._domain,name,dependencies,True)
        package = generate_package(self._path,self._domain,name,dependencies)
        self._webezy.execute(CommandMap._ADD_RESOURCE,{'packages': { f'protos/v1/{name}.proto' : dict } })
        return package

    def AddMessage(self,package,name,fields,*args):
        message = generate_message(self._path,self._domain,package,name,fields,option=args[1],description=args[0])
        if next((m for m in package.messages if m.name == message.name), None) is None:
            package.messages.append(message)
            self._webezy.execute(CommandMap._ADD_RESOURCE,{'packages':{f'protos/v1/{package.name}.proto': MessageToDict(package)}})
            return message
        else:
            logging.error(f"Cannot create message {message.name} already exists under {package.name} package")

    def AddEnum(self,package,name,enum_values):
        enum = generate_enum(self._path,self._domain,package.name,name,enum_values)
        package.enums.append(enum)
        self._webezy.execute(CommandMap._ADD_RESOURCE,{'packages':{f'protos/v1/{package.name}.proto': MessageToDict(package)}})
        return enum

    def EditService(self):
        pass

    def EditPackage(self):
        pass

    def EditMessage(self):
        pass

    def EditEnum(self):
        pass

    def Save(self):
        logging.info("Saving webezyio architect process")
        self._webezy.save()

    def undo(self):
        self._webezy.undo()

    def redo(self):
        self._webezy.redo()