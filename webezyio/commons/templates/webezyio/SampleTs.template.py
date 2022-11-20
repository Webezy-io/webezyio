
"""Init script for webezy.io template SampleTs
Generated thanks to -

                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| | _ | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |(_)|_| \___/ 
                                   |___/              

A sample project template for typescript server

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
                    prog = 'SampleTs',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--domain',default='webezy')           # optional argument
parser.add_argument('--project-name',default='SampleTs')           # optional argument

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

# Instantiating all enum values for [webezy_SamplePackage_v1_SampleEnum]
_enum_values_webezy_SamplePackage_v1_SampleEnum = [helpers.WZEnumValue('UNKNOWN_SAMPLEENUM',0),helpers.WZEnumValue('TEST_VALUE',1)]
        
# Creating enums   

# Constructing enum [webezy_SamplePackage_v1_SampleEnum]
_enum_webezy_SamplePackage_v1_SampleEnum = helpers.WZEnum('SampleEnum',enum_values=_enum_values_webezy_SamplePackage_v1_SampleEnum) 
        
"""Packages and thier resources"""
# Construct fields    

# Constructing a field for [webezy_SamplePackage_v1_WellKnowns_timestamp]
_field_webezy_SamplePackage_v1_WellKnowns_timestamp = helpers.WZField(name='timestamp',
                              description='A well known type by goole for timestamps - Typescript Date object',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type='google.protobuf.Timestamp',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_WellKnowns_struct]
_field_webezy_SamplePackage_v1_WellKnowns_struct = helpers.WZField(name='struct',
                              description='A well known type by google that mimcs a structure with different impl. in languages - Python Struct Object, Typescript Json like object',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type='google.protobuf.Struct',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleString]
_field_webezy_SamplePackage_v1_SampleMessage_SampleString = helpers.WZField(name='SampleString',
                              description='A sample field using string value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleBool]
_field_webezy_SamplePackage_v1_SampleMessage_SampleBool = helpers.WZField(name='SampleBool',
                              description='A sample field using boolean value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_BOOL',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleInt]
_field_webezy_SamplePackage_v1_SampleMessage_SampleInt = helpers.WZField(name='SampleInt',
                              description='A sample field using int32 value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_INT32',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleFloat]
_field_webezy_SamplePackage_v1_SampleMessage_SampleFloat = helpers.WZField(name='SampleFloat',
                              description='A sample field using float value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_FLOAT',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleStringList]
_field_webezy_SamplePackage_v1_SampleMessage_SampleStringList = helpers.WZField(name='SampleStringList',
                              description='A sample field using repeated keyword means it accept list / array of strings',
                              label='LABEL_REPEATED',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleNested]
_field_webezy_SamplePackage_v1_SampleMessage_SampleNested = helpers.WZField(name='SampleNested',
                              description='',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.SamplePackage.v1.WellKnowns',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleEnum]
_field_webezy_SamplePackage_v1_SampleMessage_SampleEnum = helpers.WZField(name='SampleEnum',
                              description='',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.SamplePackage.v1.SampleEnum',
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Packing all fields for [webezy_SamplePackage_v1_WellKnowns]
_msg_fields_webezy_SamplePackage_v1_WellKnowns = [_field_webezy_SamplePackage_v1_WellKnowns_timestamp,_field_webezy_SamplePackage_v1_WellKnowns_struct]
# Packing all fields for [webezy_SamplePackage_v1_SampleMessage]
_msg_fields_webezy_SamplePackage_v1_SampleMessage = [_field_webezy_SamplePackage_v1_SampleMessage_SampleString,_field_webezy_SamplePackage_v1_SampleMessage_SampleBool,_field_webezy_SamplePackage_v1_SampleMessage_SampleInt,_field_webezy_SamplePackage_v1_SampleMessage_SampleFloat,_field_webezy_SamplePackage_v1_SampleMessage_SampleStringList,_field_webezy_SamplePackage_v1_SampleMessage_SampleNested,_field_webezy_SamplePackage_v1_SampleMessage_SampleEnum]
    
# Construct messages

# Constructing message [webezy_SamplePackage_v1_WellKnowns]
_msg_webezy_SamplePackage_v1_WellKnowns = helpers.WZMessage(name='WellKnowns',
                                 description='None',
                                 fields=_msg_fields_webezy_SamplePackage_v1_WellKnowns,
                                 extension_type=None,
                                 extensions=None)

# Constructing message [webezy_SamplePackage_v1_SampleMessage]
_msg_webezy_SamplePackage_v1_SampleMessage = helpers.WZMessage(name='SampleMessage',
                                 description='A sample message including most used types',
                                 fields=_msg_fields_webezy_SamplePackage_v1_SampleMessage,
                                 extension_type=None,
                                 extensions=None)

    
# Construct packages

_pkg_webezy_SamplePackage_v1 = helpers.WZPackage(name='SamplePackage',
                                                messages=[_msg_webezy_SamplePackage_v1_WellKnowns,_msg_webezy_SamplePackage_v1_SampleMessage],
                                                enums=[_enum_webezy_SamplePackage_v1_SampleEnum],
                                                extensions=None)

# Unpacking package [webezy_SamplePackage_v1]
_pkg_webezy_SamplePackage_v1_name, _pkg_webezy_SamplePackage_v1_messages, _pkg_webezy_SamplePackage_v1_enums, _pkg_webezy_SamplePackage_v1_ext, _pkg_webezy_SamplePackage_v1_domain = _pkg_webezy_SamplePackage_v1.to_tuple()
    
# Add packages

# Adding package [webezy_SamplePackage_v1]
_pkg_webezy_SamplePackage_v1 = _architect.AddPackage(_pkg_webezy_SamplePackage_v1_name,
                                                    dependencies=[],
                                                    description='None',
                                                    domain=_pkg_webezy_SamplePackage_v1_domain,
                                                    extensions=_pkg_webezy_SamplePackage_v1_ext)
    
msgs_map = {}

# Add packages messages

for m in _pkg_webezy_SamplePackage_v1_messages:
	msg_name, msg_fields, msg_desc, msg_opt, msg_domain = m
	temp_msg = _architect.AddMessage(_pkg_webezy_SamplePackage_v1, msg_name, msg_fields, msg_desc, msg_opt, msg_domain)
	msgs_map[temp_msg.full_name] = temp_msg
    
# Add packages enums

for e in _pkg_webezy_SamplePackage_v1_enums:
	enum_name, enum_values, enum_desc, enum_domain = e
	_architect.AddEnum(_pkg_webezy_SamplePackage_v1, enum_name, enum_values, enum_desc, enum_domain)
    
"""Services and thier resources"""
# Construct rpc's

_rpc_webezy_SampleService_v1_SampleUnary = helpers.WZRPC(name='SampleUnary',client_stream=None,server_stream=None,in_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, out_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, description='A Unary RPC')
_rpc_webezy_SampleService_v1_SampleClientStream = helpers.WZRPC(name='SampleClientStream',client_stream=True,server_stream=None,in_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, out_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, description='A Client-Stream RPC')
_rpc_webezy_SampleService_v1_SampleServerStream = helpers.WZRPC(name='SampleServerStream',client_stream=None,server_stream=True,in_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, out_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, description='A Server-Stream RPC')
_rpc_webezy_SampleService_v1_SampleBidiStream = helpers.WZRPC(name='SampleBidiStream',client_stream=True,server_stream=True,in_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, out_type=msgs_map[_DOMAIN+'.SamplePackage.v1.SampleMessage'].full_name, description='A Bidi-Stream RPC')
        
# Construct services

_svc_SampleService = helpers.WZService('SampleService',
                                                methods=[_rpc_webezy_SampleService_v1_SampleUnary,_rpc_webezy_SampleService_v1_SampleClientStream,_rpc_webezy_SampleService_v1_SampleServerStream,_rpc_webezy_SampleService_v1_SampleBidiStream],
                                                dependencies=[_pkg_webezy_SamplePackage_v1.package],
                                                description='A sample service with all RPC"s types available',
                                                extensions=None)

_svc_SampleService_name, _svc_SampleService_methods, _svc_SampleService_dependencies, _svc_SampleService_desc, _svc_SampleService_ext = _svc_SampleService.to_tuple()
        
# Add services

_svc_SampleService = _architect.AddService(_svc_SampleService_name,_svc_SampleService_dependencies,_svc_SampleService_desc,[],extensions=_svc_SampleService_ext)
        

for rpc in _svc_SampleService_methods:
	rpc_name, rpc_in_out, rpc_desc = rpc
	_architect.AddRPC(_svc_SampleService, rpc_name, rpc_in_out, rpc_desc)
    
# Initalize all code files 
_context = WebezyContext(files=[WebezyFileContext(file='tests/typescript.js',code=b'x\x9c\x9dU[O\xdb0\x14~\xef\xaf\xb0\xf2\x92T\x82t\xbc\xb6B\xda`\x9d\x84\x04\x1b"\xb0= T\xb9\xc9\xa15K\xec\xccv\xb8\x08\xf1\xdf9\xc7\xb99\x85\xaec\xa9\xd4\xc6\xc7\xe7\xf2\x9d\xef|v\x83\xca\x003V\x8b\xd4\x06\xb3\x11<\x96J[\x13/\x16`\xceTV\xe5\xc0\x0e\x99\xd5\x15\xccF\x93\t;)hW\xc8\x15Ks\x01\xd2\xe2\x0f7\x86q\x99\xb1\x92\xa7\xbf\xf9\n"3\x1e\xdds\xcdV\xbaL\x17wfq\x80\xe1\x1a\xfeTBC\x14|&\xeb\x84\xbe\xf6\xefL0\x9e9O\xfbT\x82I\xb5(\xed\xd09\x8e\'u\x113\xe9](\x88pHa\x99]C\x0b\xc3\xd8j\xe9\x92\xd1\x0b&\x91\xf00\xc8\x1b\x1b^\x949X\x13y\xf1\xdc\xd5\x02c]d\xf3\x8e\xc1\xcf,q\xdeGJ\xe5S\xd7\xfb^c\xf9\x96+n\xa7\xec \xfe\xd4ZN$\xad\xdbU\x82,\xca\xd5\x94\x85\x89*\x80Yx\xb4\xecV\xab\xc2\x83\x12\x0e]O\x85\xc1\xf8\xeb\xf0\x92*\xe7\xb8\xc0\xfd\xf0\x076\xa6\xc3\x9b\xd6s.\xabb:\xec\xa6\xde8\xaf\x19\x8f{\xb7\xf8r\x9e\\.~~9\xbd\x9a\xb7\xd1\xdf13dSl\xca\x8a\x02\xdf\xd18u\xf4|\xe5\x16\xa2\xf1\x1eM\xbeJ-9\x04\x84"\x98\xb2 q\xa6\x80\xbd\xd0\xc7\xf1u\xcc\xf3\x9c]I\xae\x9f\xd8\xc5\xf9\xf1(U\xd2\xa8\x1c\xe2\\\xad\xa2\x80\xf6H\x11\xb8\x81\x8d\xbb\xa2\xce3\xa4Y\xd1<b\xcf\x1854\x8fclRF\xb7\x95L\xadP\x92\xa1\xdd\x8c\xd9\xf3\x88\xe1\xe3g\x0f/ \x15p\x0f\x19\xce\xc7\x94\xb8\x015\xa3\x06\xf4=\xa0vT\x83*E\x10!\xd6\xdb\x8c\xa7\xb4\xb3\xd1\xcb\xf8:H\xb9M\xd7\xc1\x8dW\x12\xb4~\xaf$\x99)\xa4o\xfc\xd8\x89l\x1fi\x01^8\x02z\tQ\xe1%\x0e\x82\xa04\xa0Z\xa4NV\xdd\xfe!\x1bT\xdec^\xc7\xe2\xb6F\xe3\x16\xf4\xd8\xb5V\x0f\x0cMo;\n:F\x88\xf0\x8b\x01+\r\xfd5\xde\x1a\xae\x9b\xc2\x16V\xfc\xa3\xd0\x1d$\n\xda9\xe07\x15\\\xab\xce\xb8\xa8S`\xbf\xde\xec}\xff\x88\xd4\xd7]\x0f\xf1\x19X\x9eq\xcbI\x8b-Y5\xf7\xbf\xb4\xb0\x80\xd0P\xb6\x06u\xee1\x8c\x1c\xfe\x05o\x022#\xbcm\xdc6\xcc\x03\xbc\xf1\x03U\xeb\xe4\xe9\x00\xcc\xeb<\x1b\xa5\x06QX*\xf2\x94\x928|\xbeRv1YGx\xa8<\xd6\xfc\xbd\x0e\x99\x1bfl\xaa%\xdd\x06K\xd8}\x84\xfeA0o@l;F}\xa7G"\x13\x1f\xe9\x93\xfc7\xf4\xf2\x9ePz\xb7\xad2\xa9A\xd0\x90\xbb\t\xbb^\x9a1!\x13KL\xf2\x11el`\xdb)\x08?\xff;:\xc0{\x86!\xdf\xf8\xc7\xd5\x00[s)!o]\x95\x8cB\xea\x04\xaf\xfa~vd\xf8\xcf\xe1m\xa0\xdf\xcc\xe02\xd7\xb3\xf3\x00\xe0\xd5\xa2\xf4\x00\xc1\xce\xdb\xf0\x15I\xb3\xc0\x8d'),
WebezyFileContext(file='tests/python.py',code=b'x\x9c\xb5S\xdfo\xd30\x10~\xcf_q\xda\x1e\x92H!\x1d{DdR7\x84V\x01\xa3\xa2E\x081\x149\xcd\xa55$v\xb0\x9dM\x11\xe2\x7f\xe7\x1c\xa7i\xb2\xad{\x02K\x89}\xbe_\xdf}w>\x85y\x9es\xb1\x05%\xa5\x81\x9c+\x90\x05\xd4J\xfe\xc0\x8d\x89\xbdS\x98\x97\x06\x95`\x86\xdfa\xd9B+\x1b\xd80\x01\xaa\x11`v\x08z\xa3xm\xa0P\xb2\x02&Z\xb8\xdf\xa1B:\xe5\xc0\xf2\xbc\xb3\x18\xc22\r\xcb\xaf\xeb\xeb\x8f7\xcb\xf9\xfa:y]3\xb3\x9b\x199\xebS]@\xdd\x9a\x9d\x14\xf0H13\xa8\x8d\x9e9u\\\xb7\x1e\xafj\xa9\x0cH\xbd?\xe9V{\xf4\xc5\xd63fu\x8d"\x0fd/Rf\xc1*<*\xb3L\xdb=H\xd3\x82\x97\x98\xa6!-\x8f\xca^t\xa1-/\x9b\x92\x0bC\x7f\xa6uWX\xcd6?\xd9\x16\xdd\x8d\xd7UN&(\x0cEt%\xeca\xb1\xaa.\xd1\xe8\x08V\xddi\xe9\x1c\x9d\xcbV\xcam\x891\x15id\xd6\x14{\x1f\xc3+\xaa\x96\xcc\xd3:;\x8f\xb4Q\xcd\xc6\xd8c\x07Ip\xd3Q\xea\xd2\x816M\xe6\xd9\x1f$C\xae\x80\xc0;/{9\xb8\xc7\xab\xeeHZ\xa3I1\xc9\x12\xaf\xf7R\x10\x0ei\x18(\xfc\xd5\xd05\xc8\xccv\xc1\xdb\x8b\xc9\xb4\x98\xd8I\x1fPk\x92\x02\'Q2".\xf1\xd7\xd6\xa1\xab\xb6\'\xc6\x01\xf7#gv)e\x99\xacU\x83\xbd\xbc\x10&y\xd9\x9f\xdf\x96\x92\x91\x14\x9fE\xe3\x90\xef\xb96\xc97\x7f%+\xb4\xc5\xd9\xee\x8c\xf8\xf7#\x7f.$\x11D#,p\xa2\xf9\xde\x87\xb9!D\x98\'\xd3\x12\xbe`Y\xbe\x13\xf2^\xe8\xc01\x96\xb8-\x1ahJ\x8cvSq\xc5\xca\xd2fm\x04S-|Z^y5\xa10\xc1\xc9\xad\xd8\xab|\x17\xfc\xb3\xb5\xf0\xe1\xc5\xc5\xad8\t\x89=\xdd\xf5\xa3\xc9\xe2\x91:\xe8IM\xfa=\xec\xa3\x915e\xcb\xb1\x80-\nT\xcc`\xca\x8d\xdd\xa5\n\xc2W\x1e\xd0*\xa4\x82\x148=D&\x88\xf7\xb3\xe8\xbcW\xd8E\xe1\xfew\x9f\xd2I\x9f\n\xfb\x0f\xd2\xf0\x1f5+\x1c*\x19\xd8]\xd1\x9b\xee\x1f\xa3\x1b}\x85\xac"v\xe1\xf7\xd9\x9f\x93\x98\xd8\xa8:\x00\x07\xcf\x96c\x99[&\xc6m\xeb\xbdW\xce\xfb\xb9\xf6]u\x96\xce\xf0x\x17\xc7VC3\x9f\xe8\xd9\xb4\xb1\x07<+TwD\xc0\x01\x0f\x1c\x05\xe4L\x1f\x00\xd2\xdde\xda\xb31\x816\xb6\x7f<gv|l54@\x93\x18n\x86\x9e\x06{\xb9x\xb3\xe8\x89?\x8a\xf2\x92\xe7\xfc\x01\xc6\x8c\xae\xa6\xd0\x0eF\xcfs6\x02i\x83<\xc2\xf6\x17dJYg'),
WebezyFileContext(file='tests/typescript.ts',code=b'x\x9c\x95U]O\xdb0\x14}\xcf\xaf\xb0\xf2\x92D*\xe9\xf6\x1a\xc4\xb4\xc1:\t\t6D`{\x98&\xe4\xa6\x97\xe2-\xb13\xdb\x85\xa1*\xff\x9d{\x9d\xb8I\xbaB\xa1\x0f\xad\xed\xfbu\xee\xb9\xc7\xeet\xcaN\xabZi+\xe4\x92\x15\xa5\x00i\xf1\x87\x1b\xc3\xb8\\\xb0\x9a\x17\x7f\xf8\x12b\x93\x04\xc2y\xb15;\x07\xcb\x17\xdc\xf2\t\xcbA\xdf\x8b\x02fZ+\xcd\x1av\xabU\xc5\xa2\x8fK]\x17S\xfa:\xf8m\xa2\xc3>\xce\xf0\xaa.\xc1\x1a\x8cs\xab\x8b6\xb7\x8fK\xd3i[\xdeL\xedc\r\xa6\xd0\xa2\xb6\x18?E\x80RXf\xef\xc0\xe33v5\x0f0\x95[\xb0#&\xe1a\x93=N\xfa\x10\xce4\xfc]\x81\xb1\xce\xb9[g\xe3\xf2i\xbb;\x07cp\x87\xc9\xd6\xed\xc1\xb1Re\xc6\xac^\x81\xc7\xfb\xa5T\x1c\xa3\xdf\xa7\xef\xfc\xc9\xa9\xa4\xbd\xdf\xe5V#\x87\x19\x8brU\x01\xb3\xf0\xcf\xb6\x9d\r\xba\x19\xbb\x9e\tB\xf33\xbaBT\xac\xc4\r\xda\xa3o\xd8\xa7\x8e~y\xcf\x99\\U\xd9.\xc0dH\xaff\xf9\xd5\xcd\xf7Og\xd73\xef\xff\x15s\xc1"[[Q\xe1\n\x8f2"\xe73\xb7\x10\'\x13\x83\xed\x146[\x87T1\xcc\xc2\xdc\xed\xc3\xa6i\x02\xe2\xec\x84\x97%\xbb\x96\\?\xb2\xcb\x8b\x93\xa0P\xd2\xa8\x12\xd2R-\xe3\x90l\xa4\x104`\x83\xae\x94\xf3\x8c\xc2$\xa0)\xa4\x83\xb3\xb8c:I\xb1\x17\x19\xe3\xd6d\\>&\xec\xe8\x03[\x07\xac\xfb\x0c\xd3G\x97P\x08\xb8\x87\x05\x0e\xc9\xd4h\x80\x96:\x83\x02\x03\xcd\xac\xea`\x15\x88"Jv\xa6\xc0\xc0\xd6\xd0$i\xc1mq\x17\xc7\xa0\xf5\x9e\xba\xe8\xe1\x836\x04\x9c8\x8d\x1d 7\xc0+GD/\'\xaa?\xc71\x10\xa2\x0e\x9b\x07\xec$\xb6\xb1\x1f1W}xA&D\xc3\x0b\xd2\x1b\xc0\x14\xb7.<A\xcdk\xf5\xc0py\x18lC\x0f7\x94\xd1H.G\xb4u\x03j;i\x1b\xa19\xed\xa2\xec0h\x86\xfd\xf9\xfbE!{\x05\xb0\x9d\xdf1\xe0\xcen\xda\x0cH\xc3@\x1bC\xf7\x98T\xe9\x1f\x12T\xa6\'\xce\x8d\xe1\x87\x16\x16\x10M\xd5\xdd\xc9\x9el%_\x82\x98\x83\\\x10D\x1f\xf7\x0c\xcc\x11\xc4\xf4\x81\x8am\x14K\xe5gm\x96\xadB\xa3 ,\x14\'\xfd\x9d\xc9\x1d\xba\xa1d\xf6Q\xd7F\xf4\x98\x064\rM=.\x9a]jVszH\xe6\x84\xd7<\xaf\xeaWHc\xbb\xfe\x9e\x1b\xd5\xb7z,\x16\xe2-\x8d\x92\xffX!\xbb\xa4\xd1{m\t\xc3\r\x84\xe6\xba\x19\xaa\xeb\xa2\x9b\r\xcaa\x8e\x91o\x11\xc3\x18\xcf>\r\x0c\xb3\x8fF\xef\xe8\xc0G\x86!\xcd\xf8\x8f\xd5\xa1\xba\xe3RB\xe9=\x95\x8c#\xea\x02_\xf5\x98~_y\xf9\xdf8\xc9qC\xdb\t\xa8n\x124\xc9\x10\x13\xd0k\x14M\xfe{\xa0\x9e\xc1\xe0\xdeH\xcc\xf0\x04\xd8!\xc0X'),
WebezyFileContext(file='services/SampleService.ts',code=b'x\x9c\xe5XMS\xdbH\x10=[\xbfb\x8a\xda*\xc9[FN\xae"!\x10\xf0\xd6\xb2\x85\r\x85M\xf6@\xa5\x92Aj\xecY\xe4\x19\xef\xcc\x18\xc7\xa1\xfc\xdf\xd3\xf3!K\xb2\x8d!\x14K\x0e{\x00[\xf3\xf1\xa6\xe7u\xbf\xee\x96\xd9x"\xa4&\xf7$h\x8c(\xcfr\xb8\xe4T\xce\x8fh\x9e\xb7\x8a\x91\xa3\x9c\x01\xd7}-\x81\x8e\x19\x1f\xd6\xe6\xfa \xef@n\x9e\xfb\xc82\xb6:\xa3\x80g\xf6\x84c\xaa)>\xbb\xfd\xc7\xd3I\x0e\xdf\xdc\xda\xe5\xe0\x05\xd0\x8c^\xe3\x11\xf5\xe1\xaa}n\xe4o\xc9tm\xa1\xd2TO\x15~\xb9\xe4z>\x81\xecOw\r\xb7\xa7\x0b\x1aq5\r\xc8\x82\xdcH1&\xe1\xc1PN\xd2\xb6\xf9\xb7\xfb\x8f\n\xf7\x02VPb\xe0Y\n\x1d)\x85\\\xae\x8e\xdbS\xcdr\xd5\x063Z]}8a\x03<mm!\xe3\x1a\xe4\rM\xa1\x8eM\xc7\x13G\x1f\x9e\xe0\xee\xd1Z\x1f\xc4\x8f\n\xdeD\n-T\xbb\xb6\xaa\xc4\xfc\x9dP\xe5\x11\xceizK\x87\xb0y\xa3\x9f\xc4\x8dA\x9aS\xa5\xea\xa7\x12f\x1e\xc6\xe8p\xb5\xd9F\x7f\xcdwk\xdc\xee\x93\xfb\xa0q5\x06=\x12YB\x94\x96\xe8\xf5\xcf\t\xa1|\x8e\'5R\xc1qh\x9aj!\xa3\xa6YiGD\x0eq.\x86\xd1\xce\tG\x1f\xe6\xec;d$\xac\xdfo\xa7\x89k\xf5\x88\xa9X\x82\x9a\xe0\x1e \xef\xed\xfe\x86[\xf7Q\x88<Adh\x95c\x7f\xe4\x82\xea\xe4m\xfc\xa62v\xc2q\xa4\xf2\xdc\xb7\x06&\xe1\x00\x94\xf6\xd6:\xbe\x94\xbdh\xb8\xb6\xf4\x94)\x9d\\\xd5\xd6S)\xe9<l\x85\xda\x8cU7\x7f\xae\xec\xee\xe1$d\x895\xb9\xe18\xf0\x0f\r\xb3/\t\xefh>\x05w^\xa3a\xb1voa\x1e&o\xdf\xd8\xa1\x85\x9b\xd1l\x8c3\x88\x98p\x98\x11\x94\x0fD\x86\x19?\xed\x8e\xea\xf0\xe98\xa9y9.\'\xe2A\xa7?\xf8\xf2\xe9\xf0\xf4\xb2\x83;\x16{Ac\x81~\x99Hv\x87X\xa4 w\xe3\xf6.(\x85O\xc6\x8f\xed69@\xa5\x90\x83\x83\x19\\\xc3\xf79\x13d\x97\x1c\x9f\x91\xde\xd9\x80\\t\xbag\x9f\x10|2\xbd\xceYJ\x94\xddk\xf5\x9a\x90\x95\xe4\xf2n\xcb1-\xb2er\x1f\xbd\x1f\x99\xe8A\x90\x84\xac\xa4\x84\xe7\xa3\xb6<\xe45\xceb\xf0V\xb3\xd46\xd0\xfd\xa0\xd1$\xefm\xe4\x1bf\x9c\x18\x08\xe3\xa909\x0fI\xfdwjB\xc3\xcdZ\t\x90\xfb2l\x0b\x93\x8cw\x8a\xef6t\x8b\x07\x8c\xd9eR\xb0\x11W\x7f2\x11Y\x8c\xb8([ ;&\xb9\xed\xad\xe8\xeb\xebIa\xd2\xc5\xf9\x11:\xec\xaa_\xfa\x065\xfa\xdb\xfd_\xfd\xb3^\xec\xa2\x9a\xdd\xcc#CE<\x04}\x0e\x80rm.\xbe6\x1f\x04\xf4L<\x15\xd4S\xe2!\xd9\r\x89j\xda\x8e\xab\xb7qy\xa2\xf1\xf0\x82x)\n\xbcw)\x0bs\xfbE\xc5\xa1\x11\x9fb\xea\xaf\xc14m\xf8\xff|4Wka\x11\xd4\x1b\xea\xe3\x8b\x86w\xbd\x10\xfe\xd2\x18\xdf\x1aS\xeb\x0c=9\xb4\xd0\x0fK\xb4\x14Y\xe5\x90\x13\xb8C\x1cor,x\x14\x9a\xc0\x0e[$2\x9f\xdb\xd2\xd4\xd2\xdam\x92T\xd6@\xbf\xe8\x95\x95\xf9\xb8\x92\x9eF\xa5\xc1\xf3\x04.l\xd0/\xa9Js\xa1\xb0\xa4D\x86\x8a\xfb\xd5\x13\xc3#\x9c\xb5L[|OE\xc1{\xd8\xf4\xa4\x1c\xf9P!zT\x96\x07b\xc1\xb6\xeb\n\x8d\xa9\xda\xe2\x1a\xa5V\x84\x9f\x89m\xa5J\xffT\xad\xc2\xe9\xf2"x\xfc\xa1Rl\xc8\xad\xaaK\x95k\xb1\xb4\xe4?\xce\x1e\x81\xe7\x80\x93)\xde\xda\\\x86X2fL\x8f\xea\x8d!\xda\x94!\x8c\x14sB\x0b\x12}\xc2_\xf2\x84\xe0\xd5=\x91\xebP\xe3\xcb\xdeI\xf7\xfc\xb4\xd3\xed\xf4\x06\x9d\xe3\xd6N\xd7\xf6N\x84)\xc2\x85&s\xd0e3\x06\xd9N\xb3\x19</gU{\xf4"gm\xe8\xdb_4g\xd5{\xf2\xe7Co\xaf\xaf\xd6-^\xd1\xafZc\xab\xa5\xec\xd1Z\xbb\xee\x85\x97+\xb9?\x81]\xad\xbc\x8e\xacN\xc6\xf4k\xe9\xc9\x1eh\xa2\x02|\x8f\\\xa6\x14\x14\x90\xcbDE\xd6\x98\x99euK|\x91\xe8\xf0\xcc9}6\x02N2\xc1\xc1g/\xbch\xb1\x1b\xebZ\xd4,\x05\x18{q\xfeb\x11\x96/\xc3\x85\x04\xd7^\x8f_T\x80\xd5W\xea\x17\x91\xdf\x13B\xbc\xbc\xd1\xd3\x03\xbc^\xdc\xff?\xb5};W\x95\xca\xbeI\xa8\x8f(\xf5C\xa9D/\xda\xe7\xa9\xd6\xca\xd6\x9c\xdfGM9\x82\x1d\x80*5\x8bUQ\xe1K\xbb\xe0\xa6M`\xb2\xf0\x81*\xfa\x84\x87\xc4\xbc\xf0\x12=\xe3\xc46+\xeb\xed\x9e\xefaH\xb4\xb9_Xv1\xd7\xc8\xe4\xaesy\xb8\x82\x8cf\xaf\xe3\xe2\xa0\xef\x8c6\x80\x9a\x04\xb3\nXO+Ux[\xff\xed\x01d\x06dLo1\x1dM%\xd8\x8e\xa9\x82\xb2li1\xa9\xf8l\x04\xd9\x86\x16\x89D\xf6\xcb#]\x92\x90\xa5Q\x8f\xe5\xb6\x13\xcci\x17\xbd\xc3\xd3\xd6N_\x8c\xc1\x1b,\xd2\x14\x8d\xb4\xb9\xcc]\x07\xbb\x9d\x00\xff\xe0\x9b\xfbm*(~\xf6p\x80\xad\x95g\xff\x11,\xf6~\x00\xb00\xc8\x1d'),
WebezyFileContext(file='services/__init__.py',code=b'x\x9c\x03\x00\x00\x00\x00\x01'),
WebezyFileContext(file='services/index.ts',code=b'x\x9c\xd5X\xddo\xdb6\x10\x7f\x96\xff\x8aC0\xc0R\xa0:i\x81\xbe\xc8s?\x96v@\x81v\t\x9a\x16{te\xe9\x12s\x91(\x8d\xa4\x12\x07\x99\xff\xf7\x1dI}\xba\x8a\xad\xa0n\xb2\xe5\xc1\x11y\xdfw\xbc\x1fObi\x9e\t\x05w\x10\t\x8c\x91+\x16&\xd2\x87O\xa8\xc28T\xa1\x0f\xe7(\xaeY\x84\xef\x85\xc8\x04\x84\x12\xe6\xd2n\xccQ\xef\xf8p\x920\x92\xfa\xcaCq{\x12&I\xb5\xf1\xae\xc8\x13\\\x9d+\x81aZ\xed}F\xd2\xb9H\xb0\xbb\xfb\xa7`\xaa\xd9\x855\\\x88,\x85\xf1\x9bK\x91GG\xfa\xe7\xd9_r<\x1d\xb1\xca\xcf\x9c\xc8L\xb2\x8b\xdb\x9a\xb5P,is\x9c.\xb4\x8fZg\xcd"V]%\xe7aJ\xfe\x95\xb1Y?j\xde\xc9\x11\x99P\x99<\xea0\x8d+\xe1C\x9d\x05K:\x0b\xa3\xab\xf0\x12\xfb\xe5J\xe2x\x14e\\*\x98\xbf{\xff\xfb\xdb\xaf\x1f\xbf\xccO\xcf\xbe|8\xfd\x03fp7r\x0et|\x93+\xc4<L\xd85\xce\x15Kq\x9e\xca\x83\x00\x9e\xbf8\xa6?\xbfbY*\x95\xbf\x98\xa4\x8c[\x96\x05\xaa\x1bD>\xcf\x19\xbf\x94\xbd\x02]\x9dY\xa1,W\xaf\xd6pU*\xbaaj\xa9Yu\xe5\x89\xb9O[\x8e"e\xaa\xe6\x8c\xa8\xe4\xc6\xba?Z\x8fF\xb82\x19\x8a\x92PJ\x90&\x0bJR\x9c#\xc7\xe4@\x14\x91\xca\x84\xbb\xcc\xa4\n\x80\x96d\x93\xd2p\x90d\xa4Eo\x1e\xf8\xa0\xe5\x03\xe0E\xba@A\xb4\x97\xc7\xc7/\x9f\xfb\x90\x96\xa71\xa8\xcf%\xd18\xde\xd4K\xd7\xf3t:\x1d\xb5dr\xa2U\x11]\xff\x9bV{\xc6\xaf\x99Q_\xef\xa5\x8d\xae\xea\xb1\xa6uJ?\x8f\xec\x01\xb16{\x8e\x8e\xfb\xed\x97\xbb\xda\xf4:(\x17\xda\xd8\xfa\x9b\xdfn\xac\t=\x87\n?p\x89Q!\xd0\xf5\xfc\x8dc\xe1\x91\x07\x94H\'\x17\xec\x9a\x18\x81\xd8\xe3\x8c\'\xb7=)\x98\xf6p\xb5S\xdbGo\xa7\xb7\x8f\xde\x17v\xd0\x17\xf1\x94|\x1c9G\x87\x87#\xe7\x10\xde\x90s\xcb,\xee\xf2\x95)4\xc0`\x98b\x94\x91`\xb9b\x19\x87\xb7`\xf6\xe1\xf3\xd9\x89\xa1]1\x1eC\xc3\x9a\x87\x82\x90@\xe0\xdf\x05R);\xedT\xaa\xfd\x84R\xd2\xaa\xc5]W\xb3\xca\x8f\xa1\tT\x85\xe0\x12\xce\x0ch\xe0\xaf[t\xbd"\x81#\xcaI\xb1HX\x04-\xef\xdd\xd2\x91`\x9b\'\xcd!}\xdd\x94\xc8\x0b\x06\x19\x9e\xfe\x1f2ii\xba\xdf\x17$Ov\xeb\xc7\x8b\x82G\xc6\x17\x95\xc1\x02\x01WQ\xa10\x86\x8cG\x08j\x89\xa0\xc1\x98\xbaY\xa0\xcc3\x1eK\xd0\xd8\xb1\xd3\x95\xaap\x1b\xd7\xcb\x9ej\x14\xb4.\xb8*\x8e\x00\\s\xa5\x05\x1bW\x1c\xfcC\r\xa3/6\x1b\x80\xc4\xad6<\x98\xbd\x82\xeb\x8c\xc5T\xfb\r\xdf\xa7{u\x9c\xd0\xa8\x83bM \xaf\x7fz$\xa4h\xc8\xb96\x90\xcc.\xc0\xad\x8f\xcal6\x83\x82\xc7x\xc18\xc6\x16\xb2\x1d[\xe9\xe6Z\xdf\xa6\xb23\x98l\xb1\xec\xde\x0b\xe2\x13\xd9\xe4~\xb2\xa0f\xb9\x9f\xd5\xf3\xaa\xe24\xf9\xd7\xf8\xec\xac\x01\x13\x89\xc6{(\xbd\x1fd\xef{uM\xd1\xacb\x0b\xfe\x83\xe0\xc0\x96\xc4\x0eM=\xa8`\xc9\xcf\xca\xa1\xaa\x83\x0e\xe5\xb8\xd3\x12\xbd\xbf\xef7\x9b\xadm\xd5\xfd!\xc4\xdb\xad\xf61\x9b\xb4;\x84\xee\xd3\xf7\'\xe8\xd3\x07\x04\xb3\xd7Nn\x88\xe0\xdaH\x82\xde\xc0\xc0\x87y\x1d\xda\xae\xc8\xee\xb4Y+\xeeQ&Ev\x03v5\xadz\xaf\xd6\xb5\xb6-\xe4\x0c\xec\xc9\xde\xc2u;rp7\x9e\x9b;\xee\xden\xb4\xe4\xden\xb4\xa4\xef\xbbq\x9f\xd3O\xf3B\xf4\xd0\x01\xa8\x1d\xd7\x0f\xcdA\x03]\x186\n\xfd7\xb3\xfd\xa4\x13R\xf7\xdd\xfa\x11\xcb\xfc\x98(\xfd\x80 7Qz/\x11>\x01\x96? d25\xb0\xcb\x0c\\\x97(\xa9_i\x1b1W\x16\x0b\xddJ\xe6\xf5\xdb\xf2\xd9\xcf\x17\xd26\xd3l\'\xaa\xf6%zc~r\xac\xb2I\xc6\xdd\xb1\xde\x1c\xfb@\x9crwf\xcc-\xe34.N8\xae\x94\x16\xf54a\xed\x19\x8d\xc8c\xad\xb0_ \xca\xccG\tz\xf3nK\xe8Bi\x19z\x08 \xe4\xb7[\x8c\x11\x8b\xb7K\xa9\x19\xe5\xbc\x07\xdc\x1e\xbf\xb1\x98\xdd\x8bf\x9a\xd8\x8be\x9a\xf03\x90l\x13\x1c\x1a\xef\x06\x8c7\xf5\xc1m\x7f\x00\xdc>\xd2\x0f=\xa9\xbbN^\x8f\x9f\xf6\x0e_W\x1f\xa6HY\xc7\x98_\xad;\xdf6F\xeb\x7f\x01\n\xe6UB')]) 

# Creating all code files on target project
for f in _context.files:
	file_system.wFile(file_system.get_current_location()+'/'+f.file,zlib.decompress(f.code).decode(),force=True)

    
_architect.Save()
    