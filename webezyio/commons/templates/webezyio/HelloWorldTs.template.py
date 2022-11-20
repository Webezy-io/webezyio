
"""Init script for webezy.io template HelloWorldTs
Generated thanks to -

                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| | _ | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |(_)|_| \___/ 
                                   |___/              



Author: Amit Shmulevitch
"""
# Main webezyio class to create gRPC services programmatically
# (Same inteface that webezyio cli is built as wrapper for
# WebezyArchitect whenever you generate new resource / create new project)
from webezyio.architect import WebezyArchitect

# Some common utils modules to help us build the services faster
# and adds an validations to object before they created
from webezyio.commons import helpers, file_system

# Webezy proto modules also helps us here to construct our services
# gRPC used to create another gRPC ! :)
from webezyio.commons.protos.webezy_pb2 import Language, WebezyContext, WebezyFileContext

# Default system imports
import os
import sys
import argparse
import zlib

    
"""Initialize constants and WebezyArchitect class"""
parser = argparse.ArgumentParser(
                    prog = 'HelloWorldTs',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--domain',default='webezy')           # optional argument
parser.add_argument('--project-name',default='HelloWorldTs')           # optional argument

args = parser.parse_args()

# Constants
_PATH = file_system.join_path(os.getcwd(), 'webezy.json') 
_DOMAIN = args.domain
_PROJECT_NAME = args.project_name
_SERVER_LANGUAGE = Language.Name(Language.typescript)
_HOST = 'localhost'
_PORT = 50051

# Initializing WebezyArchitect class which we going to interact with
# It is used to create all of our 'webezyio' resources
_architect = WebezyArchitect(path=_PATH,
                             domain=_DOMAIN,
                             project_name=_PROJECT_NAME)
_architect.SetConfig({'host': _HOST, 'port': _PORT})
_architect.SetDomain(_DOMAIN)
    
"""Project specific configurations"""
    
# Init all the client to be used with your services
# Here we configured a python + typescript clients to be created with our services    
_clients = [{'language': 'python', 'out_dir': file_system.join_path(_PATH, 'clients', Language.Name(Language.python))}, {'language': 'typescript', 'out_dir': file_system.join_path(_PATH, 'clients', Language.Name(Language.typescript))}]
    
# Adding the base project data
_project = _architect.AddProject(server_language=_SERVER_LANGUAGE,
                                 clients=_clients)

# NOTE - that every call to WebezyArchitect executions
# it will return the proto generated class of that object
# which can be used to enrich the webezy base structure
# or debug easly whats going on beneath the surface
# print(type(_project))
# <class 'webezy_pb2.Project'>

    
# Creating enums values

        
# Creating enums   
 
        
"""Packages and thier resources"""
# Construct fields    

# Constructing a field for [webezy_HelloWorldPkg_v1_HelloWorldMsg_Hello]
_field_webezy_HelloWorldPkg_v1_HelloWorldMsg_Hello = helpers.WZField(name='Hello',
                              description='This is simple message to say hello back to the world',
                              label='LABEL_OPTIONAL',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Packing all fields for [webezy_HelloWorldPkg_v1_HelloWorldMsg]
_msg_fields_webezy_HelloWorldPkg_v1_HelloWorldMsg = [_field_webezy_HelloWorldPkg_v1_HelloWorldMsg_Hello]
    
# Construct messages

# Constructing message [webezy_HelloWorldPkg_v1_HelloWorldMsg]
_msg_webezy_HelloWorldPkg_v1_HelloWorldMsg = helpers.WZMessage(name='HelloWorldMsg',
                                 description='This is a hello world message',
                                 fields=_msg_fields_webezy_HelloWorldPkg_v1_HelloWorldMsg,
                                 extension_type=None,
                                 extensions=None)

    
# Construct packages

_pkg_webezy_HelloWorldPkg_v1 = helpers.WZPackage(name='HelloWorldPkg',
                                                messages=[_msg_webezy_HelloWorldPkg_v1_HelloWorldMsg],
                                                enums=[],
                                                extensions=None)

# Unpacking package [webezy_HelloWorldPkg_v1]
_pkg_webezy_HelloWorldPkg_v1_name, _pkg_webezy_HelloWorldPkg_v1_messages, _pkg_webezy_HelloWorldPkg_v1_enums, _pkg_webezy_HelloWorldPkg_v1_ext, _pkg_webezy_HelloWorldPkg_v1_domain = _pkg_webezy_HelloWorldPkg_v1.to_tuple()
    
# Add packages

# Adding package [webezy_HelloWorldPkg_v1]
_pkg_webezy_HelloWorldPkg_v1 = _architect.AddPackage(_pkg_webezy_HelloWorldPkg_v1_name,
                                                    dependencies=[],
                                                    description='None',
                                                    domain=_pkg_webezy_HelloWorldPkg_v1_domain,
                                                    extensions=_pkg_webezy_HelloWorldPkg_v1_ext)
    
msgs_map = {}

# Add packages messages

for m in _pkg_webezy_HelloWorldPkg_v1_messages:
	msg_name, msg_fields, msg_desc, msg_opt, msg_domain = m
	temp_msg = _architect.AddMessage(_pkg_webezy_HelloWorldPkg_v1, msg_name, msg_fields, msg_desc, msg_opt, msg_domain)
	msgs_map[temp_msg.full_name] = temp_msg
    
# Add packages enums

for e in _pkg_webezy_HelloWorldPkg_v1_enums:
	enum_name, enum_values, enum_desc, enum_domain = e
	_architect.AddEnum(_pkg_webezy_HelloWorldPkg_v1, enum_name, enum_values, enum_desc, enum_domain)
    
"""Services and thier resources"""
# Construct rpc's

_rpc_webezy_HelloWorldSvc_v1_GetHelloWorld = helpers.WZRPC(name='GetHelloWorld',client_stream=None,server_stream=None,in_type=msgs_map[_DOMAIN+'.HelloWorldPkg.v1.HelloWorldMsg'].full_name, out_type=msgs_map[_DOMAIN+'.HelloWorldPkg.v1.HelloWorldMsg'].full_name, description='This is a simple unary call that uses HelloWorldPkg->HelloWorldMsg for input and output types')
        
# Construct services

_svc_HelloWorldSvc = helpers.WZService('HelloWorldSvc',
                                                methods=[_rpc_webezy_HelloWorldSvc_v1_GetHelloWorld],
                                                dependencies=[_pkg_webezy_HelloWorldPkg_v1.package],
                                                description='None',
                                                extensions=None)

_svc_HelloWorldSvc_name, _svc_HelloWorldSvc_methods, _svc_HelloWorldSvc_dependencies, _svc_HelloWorldSvc_desc, _svc_HelloWorldSvc_ext = _svc_HelloWorldSvc.to_tuple()
        
# Add services

_svc_HelloWorldSvc = _architect.AddService(_svc_HelloWorldSvc_name,_svc_HelloWorldSvc_dependencies,_svc_HelloWorldSvc_desc,[],extensions=_svc_HelloWorldSvc_ext)
        

for rpc in _svc_HelloWorldSvc_methods:
	rpc_name, rpc_in_out, rpc_desc = rpc
	_architect.AddRPC(_svc_HelloWorldSvc, rpc_name, rpc_in_out, rpc_desc)
    
# Initalize all code files 
_context = WebezyContext(files=[WebezyFileContext(file='tests/typescript/typescript.ts',code=b'x\x9c}\x90Mk\xc30\x0c\x86\xef\xfe\x15\xba\xc5\x81\xcd\xb9\xa7t\x14F\xb7^\x06\x83\rvn=5q\xeb\xc6A\xd6VF\xc9\x7f\xaf\xe5~\xac\xb9T\x18\x0b\xc9\xd2\xf3\xcar\xbb>\x10\xc3\x01>\x90~\x9d\xc59Q \x18`Ma\x07\xc5\xac\xa1\xdeVr=nb1Q\xeeR\xdd\xa2\xf7a\x1f\xc8\x7fs|\x80\x85D_\x12\xbdo\x9bk\xb31U:\xd6;\xec8V\xfc\xd7c\xb4\xe4zN\x1ceC\x17\x19"\xff\xac`\n\x1d\xeeG@]\xa6\n\x8f|Jf\xee[l\xea\xb1\x8cY\xdc>&\xcaAA\xb2\x9c\xad\x8b\xec\xe0E\xe6\xf8\xbc\n\xc3s\x9e\xa5P\xc3\x04\x94\x12q\xf3\x8a\xfc\xcf\xd1#\xbd2\xf3\x0c\xb7\xd8iM\x18\xef\xea\x970}:O &\xdf\x0b\x1e\x8d\x0f\x8d\xb4\x9ePCi\xec\x92m\xab5\xca\x92\xeb\xdb\x8d\xdf\xe9\xcf\xc5\x17\xc2\x11\x9f_\x8f\x8c'),
WebezyFileContext(file='tests/typescript/typescript.js',code=b"x\x9cm\x8dAK\x031\x10\x85\xef\xf9\x15C.\xcd^R\xbc\x1a<\t\xdaKo\x82\x07\x91\xa5\xa6cw!f\xd6\x99\x89U\xa4\xff\xddlZ\xaa\x05\x87\x81\x817\xef{\xcf\x16A\x10\xe51\xaa\r\x06?'b\x15\xdf\xf7(k\xda\x96\x84p\x03\xca\x05\x83\xf9\xd80\xe8\xd7\x84\x12y\x9c\xb4\xbf\xaa\x0f\xc6\xf722:\xeb\xfd\xb2nL#f\x95\xe5\xaf\xcbvGN\xb4\xbcT\x7f\xc6\xfdE\x84\x1f0%\xda\x13\xa7\xad\x8a;y\x9b\xf68kk\xd9U\xe8\xdb@\x9d\xd5\xac^\xc3\xa2]\xb8cz\x83\x87s\x12\xdc\xb6\xe6\x859\x043W\xf9{\xd4\xd59\xc6]$v-\xce\xeb\x80\xd9\xbd\x96\x1cu\xa4\x0c\x8eQ\xbaSS\xa4,\x94\xd0'\xda59\x98C\xf7d\xe3F\xe3`\x9f\xff \xc8L\xfc\x1ft|\xccX0?\xb8\x15v("),
WebezyFileContext(file='tests/python/python.py',code=b'x\x9cUP;\x0e\xc20\x0c\xdd}\no\xa4\x12\xca\x01\x90:!>\x0bR\xc5\xc2\\R\xd3F\x94$r\x8c\xa0\xb7\'i\xa9\n^\x92\xe7\xbc\x9fb\x1f\xc1\xb3\xa0\x8f`\xa7[\x1c"\xdc\xd8?\xb0\xe5`\xf0\xbb<\x07\xb3c\xf6\x0c`o\x89\xab[\x12\xf3jT\x81\xce\x0bZ\x97E:\xd4\xd2m\x00\xd3\xccH\xd7!\x90k\xd4\x8f\xa0\x80\xc9\xdc\xf4\x96\x9c$\xda \x9dwsLG}\xef_\x9e\xfbF\xe2\x1a\x8f\x19]2\xaa\xee-@\x94\xe7\x15\xcb?\x8eJv\xc2\xc3\x94\xca\x14\xd3sf\xe9\x03\xc9"V\x7f>zA\xa7\xd8\xaaQ\x99g\\\x97\xab\xf1\xc0}\xaeXM\xd5\xb6c\xd3Uj\x9ei\x81\xad\x13\x95\xa2\n\xa0\xb7\xa1\xb0|\r\xd6\x11i\xf3C\xa2\x02>\xaa\xa3uj'),
WebezyFileContext(file='services/HelloWorldSvc.ts',code=b'x\x9c\x9d\x94Mo\xda@\x10\x86\xcf\xde_1\x87H\x81\xca\xd8w\x13\x10m@\x8d*\x11*H\x9aC\x14\x89\xc5\x1e\x9cm\x16\xaf\xbb\xbbN\xe3"\xff\xf7\x8ec\x036\xa4\x1cz\xb0\xe5\x9d\x8f\xe7\x9d\x99\x1d\x10\x9bTi\x0b[\xe6<\xf3$\x92x\x9fp\x9d_s)\xdd\x9d\xe5Z\nL\xec\xc2j\xe4\x1b\x91\xc4-\xdf\x02\xf5+\xea\x8f}_D$\x8e=\x06\x93\xe8]a\xcc-\xa7s\x95?\xceR\x89oU\xec\xde8G\x1e\xf1\x15I\xb4\xcd\xcd\xfa*\xcb\x83\x16\xb6\x15h,\xb7\x99\xa1\x8f\xfb\xc4\xe6)F7U\x1bU\xce\x14-q-g\x05\xac\xb5\xda\xc0\xe5(\xd6i\xe8\x97\xaf\xdeOs\xd9g\xa2\x1e\x08\x94t\x11\xe2Dk\xa5a\x17\xed\xf9\x99\x15\xd2\xf8XZ\x9b\xd1\x9fSqGb\'\x81"\xb1\xa8\xd7<\xc4\x16\xfb\x06\xa5T\x0fJ\xcbh\xf1\x1aVm\xb8\xa7FRo\xf0R\xad\xac2~+\xea\xc0\xfc\x04\xdc4\x08\xdf_\xe2\x7f\'\x92\x93\x12Y(\xb91mU \x9a\xc4\r\xdd\xb7\xf9\xb8\xc6\xba\xcd\xab\x93\xd1\x0e\xcb\x15z\xdc\xa0}VQ\x00\xc6j\xba\xf4\xa7\x00x\x92\x93\x92\xe3\xfb0\xa2\t\xc3h\xf4\x1bW\xf8\'\x17\nz0\x9e\xc1\xed\xec\x0e\xe6\x93\xe9\xec\xc7\x849i\xb6\x92"\x84\x18\xedA9\x80\xa3\xad\xbcju\xe1\x1dNS\x13\xbbp\xc69\x84\x01t\x98\xe3\x84\x04\t\xe0h\x97\xfe\x9f\xea\xd6\xc8\x15\x0f_\xa8\xed\xe6z\x9f\x83\x0e\x99\xd3\x85A9\xb32_%f\xbf\x14t\xe1\x03(\x89\x9e\xc6_\x19\x1a\xdb\xdf\x85(\x89\x9eTqg\xf9UYh\xd1\xa07\x84\x8b\xed\xb7\xc5\xec\xd6\xab\x06/\xd6y\xa7\xc9\xe8\x16\xcbn\x89\x91hA\xa3I\x89\x86\xc1\xb9\xbe\xa8\x86\xba\x9e\x00\x96\x17\xdb\xf7\xaf\x02\x1e\xab\xb1\xc1\xbcF<-\xa1\xa8\xca\xab\'\xd0I2\xfa\x91\xed%\xba\xa5\xb3`\x8c\xd1\x83o\xbb\xff\x99\xd6^\xb9G\xe7z\xedY\xd1\xff\x0b\x9f\xd3\x99&'),
WebezyFileContext(file='services/index.ts',code=b'x\x9c\xe5VKO\xdb@\x10>\xc7\xbfb\x84*\x91 \xe3\x00\x12\x17\xa7\xe1!\xa0-R)\xa8\x808\x86\x8d=![\xec]ww\x1d\x82h\xfe{g\xed\xf8\x95\x9a\x94\x03=5\x8a\x12\xef\xcc\xb7\xdf<w\xc7<N\xa42\xf0\x02\x81\xc2\x10\x85\xe1,\xd2.\\\xa0a!3\xcc\x85kT3\x1e\xe0\x99RR\x01\xd30\xd2\xb9`\x84V\xe2\xc2I\xc4i\xd7\xad`\xea\xf9\x84EQ!8M\x93\x08\xe7\xd7F!\x8b\x0b\xd9w$\xceq\x84M\xe9\x9d\xe2\xa6\x92\xc2\x02&J\xc6\xb0y\xf4\xa0\x92\xa0o\x7f\xb6\x7f\xe8\xcd\x81\xc3\x0b?\x13Rs\xcd\'\xcf%45<\xaa#.\xc7\xd6G\xcbYB\xd4\xbcI\xf2\x05\xa3H\xdeI\x15\x85\xd7\xb3 \xf7\xa3\xc4z}2a\xa4\xee7@\x9b\xc5\xe6-\x9b\x85Ju\xf5\xf8\xf0\xfa>Rn:\x81\x14\xda\xc0\xe8\xf4\xec\xd3\xf1\xed\xd7\x9b\xd1\xe5\xd5\xcd\xf9\xe57\x18\xc2\x8b\xd3\xd9\xb0\xf1y\x8f\x88\t\x8b\xf8\x0cG\x86\xc78\x8a\xf5\x86\x0f\xbb{;\xf4q\x0b\xc8\xd4\x98d\xcf\x8b\xb9\xc8!c4O\x88b\x94p\xf1\xa0[749ejrT++\x9b/\x89\x9e\xb8\x99Z\xa8\xad<\x81\xdb\xd8\x12T17%2\xa0\x92g\xd6]g\xe188\xcf2\x14DLk\x98\xda,<\xd9,\x18M\xb1:\x9d,\x0f*\r\x8cT\xdd\xa9\xd4\xc6\x07Z\x92]J\xc5F$\x89\xc9\n7\\\xb0\x1c>\x884\x1e\xa3"\xdd\xfe\xce\xce\xfe\xae\x0b\xf1\xb2#\xfd\xb27I\'\xf0\xa9\\v{=\x9b\xd2\x8e\x99r\xedY*\xd2\xdb\xbfA!\xcb|\x1bf\xf4\xa5,\xae\xb8\x8a\xc7R\xd7(\xff(\xc8\x9b$\xb7\xd9\xd2>\xdd\xfb\x0f/\xa5\xe9\x85\xbf\\Xc\x8b{\xb7~\xb8<zf\x06\xcf\x85\xc6 U\xd8\xed\xb9+\xad\xd1#\x0f(\x99\x9dD\xf1\x19\x01\x81\xe0\xa1\x14\xd1sK\n\x06-\xa8zj\xdb\xf4\xf5\xf4\xb6\xe9\xdb\xc2\xf6\xdb"\x1e\x90\x8fN\xa7\xbf\xb5\xe5t\xb6\xe0\x88\x9c\x9b\xca\xb0\x89\xf3>\xa3\xa9\x04\x19,D\x1d(\x9e\x18.\x05\xdcP\x86\x80\xbe\x0c4\x9d-:\xad\xa9\xbdE\xc0\xf6\x14\x98)3\x90j\\9j\xdb\x07\xd5\xf2B\xd3\xc9\xa3K\x89\x8b$5\xc0D\x08\xd4\x91\xf6\xd1<\'\xa83k\x8f\x9c\xa4\xd9\xdd\x94-\x13\xa6\xe8\x86Q\xf83Ej\x8f\x06\xb1\xd7\xe0\xad\xa1\xcb\x0e)r\x9e\xe9\x14\x9aT\t\rW\xd9e\x84\x1f\xd7p\x1d\xd0\x86>\xe59\x1dG<\x80FF\xbaKW\xfcu\xbeT\xad\x7fX\x15\xbe\xe7\xbf\xc9\xf4\xe0\x7f\xadO\xae\xb3\x9e\x8eY\xf0\x08\xc7\xd5\xe3$\x15A\x16\x9d\x910F\xc0y\x90\x1a$\xd7D\x80\x14\x14\x82\x1d\x1dt\xef(\xd4\x89\x14\xa1\x06{\xd3\xfd\xd5\x95\xa2\x1dV\x86\xe1\xbbU\xde\xaf\r\xe4"\x12\x1f\xba\xd9\x08\xf6WF2\xfc\xa2\xc3m\x07q\x1e\x82\xc6\xb56z0<\x80\x99\xe4!u\xd4\x8a\xf7\x83wv\x9d\xee\xce\xc6\x9d[\x85r\xf8\xcfc!\xa2\xb7\x9c\x97l\x80\xf0\tt\xcbv\x19\x0e\x87\xd4\xf6!N\xb8\xc00\x1f0\x9d\xbc\xda\xd5\x8b\xc8:\xca\xfa\xab\xd4:\xcb\xddWG\x8e\xf7P\xcf\xbe7\xa6#\xf3:\xb8\xd7+\xcaSU\xc0\xce\x93\xce\x020\xd2\x98\xf9\x0fK\xff\xdfh\xf1O\xc2\xaap9\xb5\x1dW\x8bb\xf8\x93\x85F\x9cn}]\xce\x0eg\xf1\x1b\xa6H\xac\xd5')]) 

# Creating all code files on target project
for f in _context.files:
	file_system.wFile(file_system.get_current_location()+'/'+f.file,zlib.decompress(f.code).decode(),force=True)

    
_architect.Save()
    