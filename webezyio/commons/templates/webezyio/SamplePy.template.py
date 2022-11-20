
"""Init script for webezy.io template SamplePy
Generated thanks to -

                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| | _ | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |(_)|_| \___/ 
                                   |___/              

A basic sample project for webezyio.
It is included with examples for all RPC's types and using Enums + Nested Messages, including 'Well Known' messages from google.

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
                    prog = 'SamplePy',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--domain',default='webezy')           # optional argument
parser.add_argument('--project-name',default='SamplePy')           # optional argument

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
    
_architect.Save()
    