
"""Init script for webezy.io template HelloWorldPy
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
                    prog = 'HelloWorldPy',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--domain',default='webezy')           # optional argument
parser.add_argument('--project-name',default='HelloWorldPy')           # optional argument

args = parser.parse_args()

# Constants
_PATH = file_system.join_path(os.getcwd(), 'webezy.json') 
_DOMAIN = args.domain
_PROJECT_NAME = args.project_name
_SERVER_LANGUAGE = Language.Name(Language.python)
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
_context = WebezyContext(files=[WebezyFileContext(file='tests/typescript/typescript.ts',code=b'x\x9c}\x90QK\x031\x0c\xc7\xdf\xfb)\xf2v=\xd8z\xef76\x84\xa1\xeeE\x10\x14|\xd6\x1a\xef\xaa\xdd\xb5\xa4\xd11\xc6}w\x9b\xce\xcd\xdd\xcbBiH\x9a\xfc\xfei\xdc6\x06b8\xc0\x13\xd2\x8f\xb3xK\x14\x08F\xf8\xa0\xb0\x85\xea\xa6\xa3h\x1b\xb9\xe6\x9f\xa9Z(w\xaa\xee\xd1\xfb\xb0\x0b\xe4\xdf\xe3~\x06\x1b\x89^$z\xfc\xea\xce\xcd\xc64\xf9X\xefp\xe0\xd4\xf0>b\xb2\xe4"g\x8e\xb2aH\x0c\x89\xbf\xdf`\t\x03\xee&@]\xe7\n\x8f|L\x16\xeeC\xea\xda\xa9\x8c\xd9\\>f\xcaAA\xb6\x92m\xab\xe2\xe0N\xe6x>\x0b\xc3\xba\xccR\xa9q\x01J\x89\xb8\xb9G\xfe\xe7\xe8\x89^]x\x86{\x1c\xb4&LW\xf5kX\xae\xfe&\x10\x93\xef\x05\x8f\xc6\x87NZ\x8f\xa8\xb16\xf6\x95m\xaf5\xca\x92\xdb\xcb\x8d_\xe9/\xc5\'\xc2/\xa4i\x8f\x90'),
WebezyFileContext(file='tests/typescript/typescript.js',code=b'x\x9cm\x8dAK\x031\x10\x85\xef\xf9\x15C.\xcd^Rz5x\x12\xb4\x97\xde\x84\x1eD\x96\x9a\x8e\xdd@\x9a\xac3\x13k\x91\xfew\xb3i\xa9\x16\x1c\x06\x06\xde\xbc\xef=]\x18\x81\x85\x82\x17\xed\x14~\x8d\x99\x84m\xdf#\xaf\xf2\xb6D\x84{\x10*\xe8\xd4\xe7\x86@\x8e#\xb2\xa70J\xbf\xa8\x0f\xc2\x8f\x12\x08\x8d\xb6v^\xd7\xc7\x80Ix\xfe\xeb\xd2\xdd\x99c)o\xd5\x9f\xf0p\x13a\x07\x8c1\x1f2\xc5\xedx4\x17o\xd3\xd6\x93\xb6\xe2]\x85\xbe\x15\xd4YN\xea\x1d\xcc\xda\x85G\xca{x\xbe&\xc1Ck\x9e\xa9\x93SS\x95}BY^c\xccMb\xd7\xe2\xac\x0c\x98\xcc{I^BN`\x08\xb9\xbb4\xf9\x9c8G\xb41\xef\x9a\xec\xd4\xa9{\xd1~#~\xd0\xaf\x7f\x10$\xca\xf4\x1ft~L\x98S?\xb9\xbdv*'),
WebezyFileContext(file='tests/python/python.py',code=b'x\x9cM\x90;\x8e\xc30\x0cD{\x9e\x82]\xe4F\x07\x08\x90*\xd8O\xb3@\x90fkG\xa6ma\x1d\x89\xa0\xb8H|\xfbH\x96\x03\x9b\x8d4\x83\xc7!A\x7f\xe7(\x8a1\x81\xaf\xbf4\'\xe8%\xdeq\x10v\xb8\x9aWv\x1f"Q\x00|\x9fY;\x90\xbaGg\x1a\x0cQ\xd1\x87\xd2d\xb9\xd5\xf1\x08\x98\xeb\xadl\xcbL\xa13\xbb\x86\x06j\xb8\x9b<\x05\xcd\xd8\xacc\x0c\xef1\xd5\x05H\xfa\x7f\xc3\xd3*\xedH\xd3\x14\x1fQ\xa6\x8eg\x93\x03T\xe6:G(e\xaa\xc0\xf6\x8b\xf4\xbb`\xbf\x053k\xe3\xe6\\\xfe\x86\x9d\xfaI\x83Y\x02J-\xf6\xe9\xb0<\xf8Yv\xbb\xd4\x9d\xceK\xc8!\xaf\\0\x16\x1f\xd4\xe4\x89\r\xd0\xd3\x11o7\xc16!\x1dw\x105\xf0\x02\x06\xf2r\xb8'),
WebezyFileContext(file='services/HelloWorldSvc.py',code=b"x\x9c\x85\x90MO\xc2@\x10\x86\xef\xfb+&\xf1\xd06\x81\xc6xl\x82\xe9A\x82\x1e\xb0\x06\x88\x1e\x8c!m\x99m\x1a\xdb\xce:;\xa0H\xf8\xefv\xb1 \x04\x13\xe6\xb6\xf3~<\xbb\xab\x99j(\x88\x8a\nC\xc3$\x94-u(e\x8dV\xd2\xda\xccMv\x03em\x88\x05f\xfb\xa5\xd2.#kS6\xc5^|\x10\xe4T\x88Uw\xbe\xc7\xaa\xa2\x17\xe2j1]\xe5\xaee^\xb0\xc9\xcf\xd5\xa7\xf7\xc2\xa9J\xa9\xbcJ\xad=\xcd\xf9\xff\xb7\x84'\xeb)\xf2\xaa\xcc\x91\x83H)h\xe7\n\xe2\xd6\x03q\xfc\x89\x19~\xafK\x82>\xdc%\xf0\x98\xcc`2\x1c'\xcf\xc3\x9dk\x81\x1aF(\x7fM\xbe\xc5J\xf7\x80\xf1c\xd9\xbe2:\xbf\xe2\x11ul\x8b\x1e\xe4\xd4\x08~I\x00\xfd\xdbK\xe6h\x87tc\xb8l\xc4\xd7\xde\x88\x8e?\xa1\xb5\xb8\x96M\x07\x87\x01l\xbd\xe0\x90a\xb4\x86\x1a\x8b\xed\xfa\x02\xc7?d\xdc\xec\xa4\x81\xb7\xb9\xde\xc2\xab\xfb$d\x98tUo^\xa8\x89\xebT\xfc\x0e\xf9\xdb\x13\x1cCe\xc9\xcd\x81\xad~\x00\xd0\xc4\xbb\x8c"),
WebezyFileContext(file='services/index.ts',code=b'x\x9c\xe5VKo\xda@\x10>\xe3_1B\x95\x02\xc85i\xa4^LI\x13\xf5\x19\xa9m\xa2&Q\x8ed\xb1\x87\xb0\x8d\xbd\xeb\xee\xaey(\xe5\xbfw\xd6\xc6/\xea\xd0\x1c\xd2S\x11\x02\xef\xcc\xb7\xdf<w\xc7<N\xa42\xf0\x00\x81\xc2\x10\x85\xe1,\xd2.|E\xc3Bf\x98\x0b\x97\xa8\x16<\xc0\x0fJI\x05L\xc3D\xe7\x82\tZ\x89\x0b\xef"N\xbb\xae\x05S\xebw,\x8a\n\xc1\xfb4\x89pui\x14\xb2\xb8\x90}G\xe2\x9cF\xd8\x94\xde(n*)l`\xa6d\x0c\x07\'w*\t\x86\xf6\xe7\xe5\x0f}0rx\xe1gBj\xae\xf9l]BS\xc3\xa3:\xe2|j}\xb4\x9c%D\xad\x9a$\x9f1\x8a\xe4\x8dTQx\xb9\x08r?J\xac7$\x13F\xeaa\x03tPl\x1e\xd8,T\xaa\x8b\xfb\xbb\xc7\xf7\x91\xf2\xc0\t\xa4\xd0\x06&\xef?|<\xbd\xfer59\xbf\xb8:;\xff\x06cxp:]\x1b\x9fw\x8f\x98\xb0\x88/pbx\x8c\x93Xw}xutH\x1f\xb7\x80\xcc\x8dI\x8e\xbc\x98\x8b\x1c2E\xb3D\x14\x93\x84\x8b;\xdd\xba\xa1\xc9)S\x93\xa3ZY\xd9jK\xb4\xe4fn\xa1\xb6\xf2\x04ncKP\xc5\xdc\x94\xc8\x80J\x9eYw\x9d\x8d\xe3\xe0*\xcbP\x101\xadan\xb3\xb0\xb4YH\xd6\x14\xab\xd3\xc9\xf2\xa0\xd2\xc0H\xd5\x9bKm|\xa0%\xd9\xa5Tt#ILV\xd8u\xc1r\xf8 \xd2x\x8a\x8at\xaf\x0f\x0f_\xbfr!\xdev\xa4_\xf6&\xe9\x04.\xcbe\xaf\xdf\xb7)\xed\x989\xd7\x9e\xa5"\xbd\xfd\x1b\x15\xb2\xcc\xb7qF_\xca\xe2\x8a\xabx,u\x8d\xf2O\x82\xbcIr\x9b-\xed\xd3\xbb}\xf1P\x9a\xde\xf8\xdb\x855\xb6\xb9u\xeb\x87\xcb\xa3gf\xf0Lh\x0cR\x85\xbd\xbe\xbb\xd3\x1a}\xf2\x80\x92\xd9I\x14_\x10\x10\x08\x1eJ\x11\xad[R0jA\xd5S\xdb\xa6\xaf\xa7\xb7M\xdf\x16\xb6\xdf\x16\xf1\x88|t:\xc3\xc1\xc0\xe9\x0c\xe0\x84\x9c\x9b\xcb\xb0\x89\xf3>\xa1\xa9\x04\x19,D\x1d(\x9e\x18.\x05\\Q\x86\x80\xbe\x0c4\x9d-:\xad\xa9\xbdE\xc0\xf6\x14\x9893\x90j\xdc9j/\x8f\xab\xe5WM\'\x8f.%.\x92\xd4\x00\x13!PG\xdaG\xb3NPg\xd6\xee9I\xb3\xbb)[&L\xd1\r\xa3\xf0g\x8a\xd4\x1e\rb\xaf\xc1[C\x97\x1dR\xe4<\xd3)4\xa9\x12\x1a.\xb2\xcb\x08\xdf\xec\xe1:\xa6\rC\xcas:\x8dx\x00\x8d\x8c\xf4\xb6\xae\xf8\xfb|\xa9Z\xffmU\xf8\xbe\xff$\xd3\xa3\xff\xb5>\xb9\xcez:e\xc1=\x9cV\x8f\xb3T\x04YtF\xc2\x14\x01WAj\x90\\\x13\x01RP\x08vt\xd0\xbd\xa3P\'R\x84\x1a\xecM\xf7WW\x8av\xd8\x19\x86\xcfVy\xbf6\x90\x8bH|\xe8e#\xd8\xdf\x19\xc9\xf0\x8b\x0e\xb7\x1d\xc4y\x08\x1a\xf7\xda\xe8\xc3\xf8\x18\x16\x92\x87\xd4Q;\xde\x8f\x9e\xd9u\xba;\x1bwn\x15\xca\xdb\x7f\x1e\x0b\x11=\xe5\xbcd\x03\x84\xcf\xa0W\xb6\xcbx<\xa6\xb6\x0fq\xc6\x05\x86\xf9\x80\xe9\xe4\xd5\xae^D\xf6Q\xd6_\xa5\xf6Y\xee=:r\xbc\xbbz\xf6\xbd)\x1d\x99\xc7\xc1\xfd~Q\x9e\xaa\x02v\x9et6\x80\x91\xc6\xcc\x7f\xd8\xfa\xffD\x8b\x7f\x12V\x85\xcb\xa9\xed\xb8\xda\x14\xc3\x9f,4\xe2t\xeb\xebrv8\x9b\xdf\xb6l\xac\xd7')]) 

# Creating all code files on target project
for f in _context.files:
	file_system.wFile(file_system.get_current_location()+'/'+f.file,zlib.decompress(f.code).decode(),force=True)

    
_architect.Save()
    