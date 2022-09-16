from pprint import pprint
from webezyio import WebezyArchitect,_helpers,_resources

"""
Webezy Builder - Programaticlly build Webezy.io projects

Builder correct workflow:
-------------------------
* Init
   ||
   |- Architect
   |- Project
   ||
   \/
* Configs
   ||
   |- Domain
   |- Config
   |- Plugins
   ||
   \/
* Packages
   ||
   |- Messages
   |- Enums
   |- Extensions
   ||
   \/
* Services
   ||
   |- RPC's
   ||
   \/
* Save
""" 

"""Builder pre config"""

# Config values
_DOMAIN = "domain"
_PATH = "/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/architect/webezy.json"
_PROJECT_NAME = "TEST-PROJECT"
_SERVER_LANGUAGE = 'python'
_HOST = 'localhost'
_PORT = 50051

# Messages
_FIELDS_OTHER = [
   _helpers.WZField("testother","TYPE_STRING","LABEL_REPEATED").to_dict()
]
_FIELDS_SAMPLE = [
   _helpers.WZField("test","TYPE_BOOL",'LABEL_OPTIONAL').to_dict(),
   _helpers.WZField("testother","TYPE_STRING",'LABEL_OPTIONAL').to_dict(),
   _helpers.WZField("testotherfield","TYPE_INT32",'LABEL_OPTIONAL').to_dict(),
   _helpers.WZField("testparent","TYPE_MESSAGE",'LABEL_OPTIONAL',
                    _resources.construct_full_name(_resources.ResourceTypes.descriptor,
                                                   _resources.ResourceKinds.message,_DOMAIN,parent_name='OtherPackage',name='OtherMsg')).to_dict(),]
_ENUMS_VALUES = [_helpers.WZEnumValue("UNKNWON",0).to_dict(),_helpers.WZEnumValue("OTHER",1).to_dict()]
_ENUMS = [('SampleEnum',_ENUMS_VALUES)]
_MESSAGES_SAMPLE = [('SampleMsg',_FIELDS_SAMPLE,),('OtherMsg',_FIELDS_OTHER)]
_MESSAGES_OTHER = [('OtherMsg',_FIELDS_OTHER,)]

# Declaring packages, RPC's and services
_PACKAGES = [
   ("SamplePackage", _MESSAGES_SAMPLE, _ENUMS),("OtherPackage", _MESSAGES_OTHER, [])]
_RPC = [
   ("SampleRPC",[
      (False,f'{_DOMAIN}.SamplePackage.v1.{_MESSAGES_SAMPLE[0][0]}'), # Input (stream, full_name)
      (False,f'{_DOMAIN}.OtherPackage.v1.{_MESSAGES_OTHER[0][0]}')] # Output (stream, full_name)
   )
]
_SERVICES = [("SampleService", _RPC, [f"{_DOMAIN}.SamplePackage.v1"])]

"""Architect flow start"""

# Init Builder
ARCHITECT = WebezyArchitect(path=_PATH, domain=_DOMAIN, project_name=_PROJECT_NAME)
# Init Project
ARCHITECT.AddProject(server_language=_SERVER_LANGUAGE, clients=[])

# Configs
ARCHITECT.SetConfig({'host': _HOST, 'port': _PORT})
# TODO add plugins
packages_map = {}
messages_map = {}
# Adding packages
for p in _PACKAGES:
   packages_map[p[0]] = ARCHITECT.AddPackage(p[0],[])
   messages_map[p[0]] = {} 
   # Adding messages
   for m in p[1]:
      messages_map[p[0]][m[0]] = ARCHITECT.AddMessage(packages_map[p[0]], m[0], m[1])
   # Adding enums
   for e in p[2]:
      messages_map[p[0]][e[0]] = ARCHITECT.AddEnum(packages_map[p[0]], e[0], e[1])
services_map = {}
rpc_map = {}
# Adding services
for s in _SERVICES:
   services_map[s[0]] = ARCHITECT.AddService(s[0],[])
   rpc_map[s[0]] = {} 
   # Adding RPC's
   for r in s[1]:
      rpc_map[s[0]][r[0]] = ARCHITECT.AddRPC(services_map[s[0]], r[0], r[1])
      # ARCHITECT.undo()
# Saving webezy json
ARCHITECT.Save()

