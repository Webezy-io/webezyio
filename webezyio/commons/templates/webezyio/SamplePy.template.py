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
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_WellKnowns_struct]
_field_webezy_SamplePackage_v1_WellKnowns_struct = helpers.WZField(name='struct',
                              description='A well known type by google that mimcs a structure with different impl. in languages - Python Struct Object, Typescript Json like object',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type='google.protobuf.Struct',
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleString]
_field_webezy_SamplePackage_v1_SampleMessage_SampleString = helpers.WZField(name='SampleString',
                              description='A sample field using string value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleBool]
_field_webezy_SamplePackage_v1_SampleMessage_SampleBool = helpers.WZField(name='SampleBool',
                              description='A sample field using boolean value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_BOOL',
                              message_type=None,
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleInt]
_field_webezy_SamplePackage_v1_SampleMessage_SampleInt = helpers.WZField(name='SampleInt',
                              description='A sample field using int32 value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_INT32',
                              message_type=None,
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleFloat]
_field_webezy_SamplePackage_v1_SampleMessage_SampleFloat = helpers.WZField(name='SampleFloat',
                              description='A sample field using float value',
                              label='LABEL_OPTIONAL',
                              type='TYPE_FLOAT',
                              message_type=None,
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleStringList]
_field_webezy_SamplePackage_v1_SampleMessage_SampleStringList = helpers.WZField(name='SampleStringList',
                              description='A sample field using repeated keyword means it accept list / array of strings',
                              label='LABEL_REPEATED',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleNested]
_field_webezy_SamplePackage_v1_SampleMessage_SampleNested = helpers.WZField(name='SampleNested',
                              description='',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.SamplePackage.v1.WellKnowns',
                              enum_type=None)

# Constructing a field for [webezy_SamplePackage_v1_SampleMessage_SampleEnum]
_field_webezy_SamplePackage_v1_SampleMessage_SampleEnum = helpers.WZField(name='SampleEnum',
                              description='',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.SamplePackage.v1.SampleEnum')

# Packing all fields for [webezy_SamplePackage_v1_WellKnowns]
_msg_fields_webezy_SamplePackage_v1_WellKnowns = [_field_webezy_SamplePackage_v1_WellKnowns_timestamp,_field_webezy_SamplePackage_v1_WellKnowns_struct]
# Packing all fields for [webezy_SamplePackage_v1_SampleMessage]
_msg_fields_webezy_SamplePackage_v1_SampleMessage = [_field_webezy_SamplePackage_v1_SampleMessage_SampleString,_field_webezy_SamplePackage_v1_SampleMessage_SampleBool,_field_webezy_SamplePackage_v1_SampleMessage_SampleInt,_field_webezy_SamplePackage_v1_SampleMessage_SampleFloat,_field_webezy_SamplePackage_v1_SampleMessage_SampleStringList,_field_webezy_SamplePackage_v1_SampleMessage_SampleNested,_field_webezy_SamplePackage_v1_SampleMessage_SampleEnum]
    
# Construct messages

# Constructing message [webezy_SamplePackage_v1_WellKnowns]
_msg_webezy_SamplePackage_v1_WellKnowns = helpers.WZMessage(name='WellKnowns',
                                 description='None',
                                 fields=_msg_fields_webezy_SamplePackage_v1_WellKnowns)

# Constructing message [webezy_SamplePackage_v1_SampleMessage]
_msg_webezy_SamplePackage_v1_SampleMessage = helpers.WZMessage(name='SampleMessage',
                                 description='A sample message including most used types',
                                 fields=_msg_fields_webezy_SamplePackage_v1_SampleMessage)

    
# Construct packages

_pkg_webezy_SamplePackage_v1 = helpers.WZPackage(name='SamplePackage',
                                                messages=[_msg_webezy_SamplePackage_v1_WellKnowns,_msg_webezy_SamplePackage_v1_SampleMessage],
                                                enums=[_enum_webezy_SamplePackage_v1_SampleEnum])

# Unpacking package [webezy_SamplePackage_v1]
_pkg_webezy_SamplePackage_v1_name, _pkg_webezy_SamplePackage_v1_messages, _pkg_webezy_SamplePackage_v1_enums = _pkg_webezy_SamplePackage_v1.to_tuple()
    
# Add packages

# Adding package [webezy_SamplePackage_v1]
_pkg_webezy_SamplePackage_v1 = _architect.AddPackage(_pkg_webezy_SamplePackage_v1_name,
                                                    dependencies=[],
                                                    description='None')
    
msgs_map = {}

# Add packages messages

for m in _pkg_webezy_SamplePackage_v1_messages:
	msg_name, msg_fields, msg_desc, msg_opt = m
	temp_msg = _architect.AddMessage(_pkg_webezy_SamplePackage_v1, msg_name, msg_fields, msg_desc, msg_opt)
	msgs_map[temp_msg.full_name] = temp_msg
    
# Add packages enums

for e in _pkg_webezy_SamplePackage_v1_enums:
	enum_name, enum_values, enum_desc = e
	_architect.AddEnum(_pkg_webezy_SamplePackage_v1, enum_name, enum_values, enum_desc)
    
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
                                              description='A sample service with all RPC\'s types available')

_svc_SampleService_name, _svc_SampleService_methods, _svc_SampleService_dependencies, _svc_SampleService_desc = _svc_SampleService.to_tuple()
    
# Add services

_svc_SampleService = _architect.AddService(_svc_SampleService_name,_svc_SampleService_dependencies,_svc_SampleService_desc,[])
    

for rpc in _svc_SampleService_methods:
	rpc_name, rpc_in_out, rpc_desc = rpc
	_architect.AddRPC(_svc_SampleService, rpc_name, rpc_in_out, rpc_desc)
    
# Initalize all code files 
_context = WebezyContext(files=[WebezyFileContext(file='typescript.ts',code=b"x\x9c\x95U]O\xdb0\x14}\xcf\xaf\xb8\xcaK\x12\xa9\xa4\xdbk\x10\xd3\x06\xeb$$\xd8\x10\x81\xeda\x9a\x90\x9b^\x8a\xb7\xc4\xcel\x17\x86\xaa\xfcw\xae\x9d\xa4q\xbaB\xa1\x0f\xad\xed\xfbu\xee\xb9\xc7\xeet\n\xa7U-\x95\xe1b\tE\xc9Q\x18\xfaaZ\x03\x13\x0b\xa8Y\xf1\x87-1\xd6I\xc0\x9d\x17\xac\xe1\x1c\r[0\xc3&\x90\xa3\xba\xe7\x05\xce\x94\x92\n\x1a\xb8U\xb2\x82\xe8\xe3R\xd5\xc5\xd4~\x1d\xfc\xd6\xd1\xe1\x10\xa7YU\x97X?R\x9c[]\xb4\xb9\xfb\xb8t\xdaV\xd7S\xf3X\xa3.\x14\xaf\r\x85O\t\x9f\xe0\x06\xcc\x1d\xf6\xf0\xb4Y\xcd\x83\x12\xdb\x05\x1c\x81\xc0\x87M\xf28\x19B\x18(\xfc\xbbBm\x9cs\xb7\xce\xc6\xd5\xd3vw\x8eZ\xd3\x8e\x92\xad\xdb\x83c)\xcb\x0c\x8cZa\x0f\xf7K)\x19E\xbfO\xdf\xf5'\xa7\xc2\xee\xfb]n\x14Q\x98A\x94\xcb\n\xc1\xe0?\xd36\xe6u3v=\xe3\x16\xcd\xcf\xe8\x8aPAI\x1b\xb2G\xdf\xa8O\x15\xfd\xea=gbUe\xbb\x00[Cz5\xcb\xafn\xbe\x7f:\xbb\x9e\xf5\xfe_)\x17.\xb2\xb5\xe1\x15\xad\xe8(\xb3\xe4|f\x06\xe3d\xa2\xa9\x9d\xc2d\xeb\xd0V\x0c\xb30w\xfb\xb0i\x9a\xc0rv\xc2\xca\x12\xae\x05S\x8fpyq\x12\x14RhYbZ\xcae\x1cZ\x9b\x15\x08\x19\xa8AW\xcayFa\x12\xd8)\xa4\xdeY\xdc1\x9d\xa4\xd4\x8b\xa0\x9d\x86\xa3\x0f\xb0\x0e\xa0\xfb\xf8\x89\xc9\x988C\x93\xa4\x053\xc5]\x8cJ=\xefN\xc6\xde}\x80|\xe2Tq@\xdd \xab\x1c\xf4A\x00\x059\xcc\x8980\x124\xa9\x15\x15\xe9@\xd7\x94\x12\x9d(6\xf6#\xb0\xc93_\xd1\x13\xf2\xdc\xc9}'\x96d\xc0\xc9o]xB*U\xf2\x01hy\x18lc\x0f/\xb1\xe0x\x8f\x0bG\xe2e\x87\xa2\x13\x7f\x9b\xb8\xed\xa4m\xc42\xbb\x8b\xad\xc3\xa0\xf1\xfb\xebo\x84\r\xd9;\xb2\xed\xfc\x8e\x01wv\xd3f \x1a\xbci\xfa\xee\xb1\xd5Q\x7f\xf3IK=q\x89\x05\xf3Cq\x83\x84\xa6\xean\xd1@\xb6\x14/A\xccQ,,\xc4>\xee\x19\x98#\x88\xe9\x83-\xb6\xd1\x98-?k\xb3l\x15\x1a\x05Q\xa1\xd8\x93L\xee\xd0\xf9\x92\xd9G]\x1b1`\xf2h\xf2M\x03.;\xbbT\xaf\xe6\xf6\xea\xcf\xf1\xe5[\xf0\nil\xd7\xdfs\x99\x86V\x8f\xf9\x82\xbf\xa5Q\xeb?V\xc8.i\x0c^[\xc2p\x03\xb1s\xdd\x0c\xd5u\xd1\xcd\x86\xe40\xa7\xc8\xb7\x88a\x8cg\x9f\x06\xfc\xec\xa3\xd1;:\xe8}\x01\xa2\x99\xfec:TwL\x08,{O)\xe2\xc8vA\xefpl\x7f_y\xf9\xdf8\xc9qC\xdb\tl\xdd$h\x12\x1f\x13\xda\xd7(\x9a\xfc\xf7@=\x83\xc1=\x92\x94\xe1\t\xc7\x1c\xa6W"),WebezyFileContext(file='python.py',code=b"x\x9c\xb5S[\x8f\x940\x14~\xe7W4\xe3\x03\x90 \x19\xf7\xd1\x04\x13g\x8c\xc9\xc4K62f\x1f\\C\xcap`\xab\xa5\xc5\xb6h&\xc6\xff\xee)-\xb7\xdd\x9d}R\x1e\xa0\xe7\xf6\x9d\xef|\xa7\xd4J\xb6\xe4\xc4\x19\x08\xa3\xd3\xeel\xee\xa4 \xac\xed\xa42\xde\x9b\x90\x9c\xb6\x1d\x87kz\xfaN\x1b(\xba\xf2\x8aP\xbdv\x06\xb5Ei\xa4l8\xa4\x9d\x92F\x96}=\xc2\x18\xd6\x826\x98nK\x13mT\x7f2\xf6\x18\x04\xc13r\x10\x0c3\xee\xc07#\xda\xf4e`_$\xf3\xaeT\x0f\x9d\xbas\x14\x07\x81\xab\xc6\xd8\x0c\x93\xe6\xc3\x11\xa3Fc`\xd5-=\x8e\x96-\xf6\xdd(Q\xf0\xa3G7\x91\xe578\x99`4\xb3\xf5P\xa9\xb3>\x80\xd6hE\xce\xc2fL4Yx\xb4\x05\xc3\xd4^3G6L\\\xdaNJ\x9e\x1dU\x0f\xde>\x08\x93\xbd\xf0\xe7\xb7\\R\xb4\xd2m\xb2\x84|\xcf\xb4\xc9\xbe\x84\xb9l\xc1\x0e\x87\x1e\x07?\xe2\x86\xaf\x85D\x9d\x14\x91\x02V\x91\xaf\x1e\xe6#2\x82*[\x8fp\x03\x9c\xbf\x13\xf2\x97\xd0\x91S,s\x9fd\x92)3:\x1e\xb4\xd9S\xcem\xd7^Pu&\x9f\xae\xf7A\x87,L\xb4\xb9\x15c(t\xe0\x9fmFH\x9e\xbf\xba\x15\x9b\x18\xd5\xd3\xc3>\xfa2]\x84#/j\xe6\xbf\xb1G\xc3l\xecVAM\x1a\x10\xa0\xa8\x81\x82\x19\xfb\x95*\x8a_\x06\x04\x9fZ*R\x10&\x88\xa2\x02u\xdf&W>`\x1f\x84\xfb\xdf{*V{\xaa\xed;*\xe2\x7f\xb4\xacx\x9adR7\x07QY\x84\xe9\x0fP@[T\x97\xfc\xde\xfe\xd9\xa4\xa8F;\x10\x98+\xcf\x0cxe\x95X\xae\xcdW\xe7\xae\xfa\xa9\xf5\xed\x87L\x97xy\x8b\xcb\xaci\x99\x8f\xecl\xbd\xd8\x99O\x0e\xea'\n0\xf3!\x17\t\xb9\xd4{\x84\xf4\xe0,\xbc\x1a+j\xcb\xfc\x87\xf7\xcc^\x1f;\r^\xa0\x15\x86\xbbC\x8f\x93\xdd\x1d\xde\x1c\xbc\xf0\x17Y\xeeX\xc5\xeeq,\xd1\xb5\xa66'=\xad\xd9\x82\xa4\x05y\xc0\xed/\xee\xce\xf1!"),WebezyFileContext(file='services/__init__.py',code=b'x\x9c\x03\x00\x00\x00\x00\x01'),WebezyFileContext(file='services/index.ts',code=b'x\x9c\xd5X\xddo\xdb6\x10\x7f\x96\xff\x8aC0\xc0R\xa0:i\x81\xbe\xc8s?\x96v@\x81v\t\x9a\x16{te\xe9\x12s\x91(\x8d\xa4\x12\x07\x99\xff\xf7\x1dI}\xba\x8a\xad\xa0n\xb2\xe5\xc1\x11y\xdfw\xbc\x1fObi\x9e\t\x05w\x10\t\x8c\x91+\x16&\xd2\x87O\xa8\xc28T\xa1\x0f\xe7(\xaeY\x84\xef\x85\xc8\x04\x84\x12\xe6\xd2n\xccQ\xef\xf8p\x920\x92\xfa\xcaCq{\x12&I\xb5\xf1\xae\xc8\x13\\\x9d+\x81aZ\xed}F\xd2\xb9H\xb0\xbb\xfb\xa7`\xaa\xd9\x855\\\x88,\x85\xf1\x9bK\x91GG\xfa\xe7\xd9_r<\x1d\xb1\xca\xcf\x9c\xc8L\xb2\x8b\xdb\x9a\xb5P,is\x9c.\xb4\x8fZg\xcd"V]%\xe7aJ\xfe\x95\xb1Y?j\xde\xc9\x11\x99P\x99<\xea0\x8d+\xe1C\x9d\x05K:\x0b\xa3\xab\xf0\x12\xfb\xe5J\xe2x\x14e\\*\x98\xbf{\xff\xfb\xdb\xaf\x1f\xbf\xccO\xcf\xbe|8\xfd\x03fp7r\x0et|\x93+\xc4<L\xd85\xce\x15Kq\x9e\xca\x83\x00\x9e\xbf8\xa6?\xbfbY*\x95\xbf\x98\xa4\x8c[\x96\x05\xaa\x1bD>\xcf\x19\xbf\x94\xbd\x02]\x9dY\xa1,W\xaf\xd6pU*\xbaaj\xa9Yu\xe5\x89\xb9O[\x8e"e\xaa\xe6\x8c\xa8\xe4\xc6\xba?Z\x8fF\xb82\x19\x8a\x92PJ\x90&\x0b\xf9-\xc59rL\x0eD\x11\xa9L\xb8\xcbL\xaa\x00hI6)\r\x07IFZ\xf4\xe6\x81\x0fZ>\x00^\xa4\x0b\x14D{y|\xfc\xf2\xb9\x0fiy\x1a\x83\xfa\\\x12\x8d\xe3M\xbdt=O\xa7\xd3QK&\'Z\x15\xd1\xf5\xbfi\xb5g\xfc\x9a\x19\xf5\xf5^\xda\xe8\xaa\x1ekZ\xa7\xf4\xf3\xc8\x1e\x10k\xb3\xe7\xe8\xb8\xdf~\xb9\xabM\xaf\x83r\xa1\x8d\xad\xbf\xf9\xed\xc6\x9a\xd0s\xa8\xf0\x03\x97\x18\x15\x02]\xcf\xdf8\x16\x1ey@\x89tr\xc1\xae\x89\x11\x88=\xcexr\xdb\x93\x82i\x0fW;\xb5}\xf4vz\xfb\xe8}a\x07}\x11O\xc9\xc7\x91stx8r\x0e\xe1\r9\xb7\xcc\xe2._\x99B\x03\x0c\x86)F\x19\t\x96+\x96qx\x0bf\x1f>\x9f\x9d\x18\xda\x15\xe314\xacy(\x08\t\x04\xfe] \x95\xb2\xd3N\xa5\xdaO(%\xadZ\xdcu5\xab\xfc\x18\x9a@U\x08.\xe1\xcc\x80\x06\xfe\xbaE\xd7+\x128\xa2\x9c\x14\x8b\x84E\xd0\xf2\xde-\x1d\t\xb6y\xd2\x1c\xd2\xd7M\x89\xbc`\x90\xe1\xe9\xff!\x93\x96\xa6\xfb}A\xf2d\xb7~\xbc(xd|Q\x19,\x10p\x15\x15\nc\xc8x\x84\xa0\x96\x08\x1a\x8c\xa9\x9b\x05\xca<\xe3\xb1\x04\x8d\x1d;]\xa9\n\xb7q\xbd\xec\xa9FA\xeb\x82\xab\xe2\x08\xc05WZ\xb0q\xc5\xc1?\xd40\xfab\xb3\x01H\xdcj\xc3\x83\xd9+\xb8\xceXL\xb5\xdf\xf0}\xbaW\xc7\t\x8d:(\xd6\x04\xf2\xfa\xa7GB\x8a\x86\x9ck\x03\xc9\xec\x02\xdc\xfa\xa8\xccf3(x\x8c\x17\x8ccl!\xdb\xb1\x95n\xae\xf5m*;\x83\xc9\x16\xcb\xee\xbd >\x91M\xee\'\x0bj\x96\xfbY=\xaf*N\x93\x7f\x8d\xcf\xce\x1a0\x91h\xbc\x87\xd2\xfbA\xf6\xbeW\xd7\x14\xcd*\xb6\xe0?\x08\x0elI\xec\xd0\xd4\x83\n\x96\xfc\xac\x1c\xaa:\xe8P\x8e;-\xd1\xfb\xfb~\xb3\xd9\xdaV\xdd\x1fB\xbc\xddj\x1f\xb3I\xbbC\xe8>}\x7f\x82>}@0{\xed\xe4\x86\x08\xae\x8d$\xe8\r\x0c|\x98\xd7\xa1\xed\x8a\xecN\x9b\xb5\xe2\x1eeRd7`W\xd3\xaa\xf7j]k\xdbB\xce\xc0\x9e\xec-\\\xb7#\x07w\xe3\xb9\xb9\xe3\xee\xedFK\xee\xedFK\xfa\xbe\x1b\xf79\xfd4/D\x0f\x1d\x80\xdaq\xfd\xd0\x1c4\xd0\x85a\xa3\xd0\x7f3\xdbO:!u\xdf\xad\x1f\xb1\xcc\x8f\x89\xd2\x0f\x08r\x13\xa5\xf7\x12\xe1\x13`\xf9\x03B&S\x03\xbb\xcc\xc0u\x89\x92\xfa\x95\xb6\x11se\xb1\xd0\xadd^\xbf-\x9f\xfd|!m3\xcdv\xa2j_\xa27\xe6\'\xc7*\x9bd\xdc\x1d\xeb\xcd\xb1\x0f\xc4)wg\xc6\xdc2N\xe3\xe2\x84\xe3JiQO\x13\xd6\x9e\xd1\x88<\xd6\n\xfb\x05\xa2L\xebT\xf4\xe6\xdd\x96\xd0\x85\xd22\xf4\x10@\xc8o\xb7\x18#\x16o\x97R3\xcay\x0f\xb8=~c1\xbb\x17\xcd4\xb1\x17\xcb4\xe1g \xd9&84\xde\r\x18o\xea\x83\xdb\xfe\x00\xb8}\xa4\x1fzRw\x9d\xbc\x1e?\xed\x1d\xbe\xae>L\x91\xb2\x8e1\xbfZw\xbem\x8c\xd6\xff\x020JUD'),WebezyFileContext(file='services/SampleService.py',code=b'x\x9c\xd5W[k\xdb0\x14~\xf7\xaf\x10\x19%\x0euM\xdb\xc7@Fon)4\x17\x92t0B\x08\x8a-\x07o\xb2\xe5\xc9\xca\xb6l\xec\xbf\xef\xc8\x97D\x96\xbd\xe6\xd2\xb40?\xc4\xe4\xdc/\xdf9\x92\x830f\\ N\x0c\x9f\xb3\x10-\x18[Pb\xc7\x9c\t6_\xfa\xb6\x08B\x92\x08\x1c\xc6\xb3x~\x89\x82Lx\\\x103\x1d\xb1\x8a\x83hQ0\x1f\x05\xe1X0n\xe4\xffG G\xc9\x88\xf0\xef\x81K\xa4\x95\xd9\x82\xc7n\x99;\xc0\xeeW\xbcH\xb9\x86a\xb8\x14\'IY\xcf\xac\xb7b\x97\xc8\xf9\x8b\xb7\xda\x86\x81\xe0\xf9\x80\xae@\x06]]\xfd s\xf2k\x150t\x86\xee\xfa\xa8\xd7\x1f\xa3\xa1\xd3\xed\x7frR)\x8f\xf8\xb9\xaf\xe7\x08\xf3\x95\x99\x10\xea[P\x8foK\xc8\xb1]\r0\xf7\xd9%I\x02\x14\x0b\xb9,\x12\xe4\xa7h\xa1\xb3\x8f\xdb\x84\xdb\xa9C\xf9\xc4<\x88\xc4,wb6\x15\xff\xcd\xb5\xef\xd6Z:\'\x14\xd9\nP^<\x05@\xc0qL"\xcflNd\xea\x84O\x9b\xaaN\x12\xb3(!\xa8\xb3-*S5\xdb\xa9\xf3\x85NQ\x13\xad}X\xb9\xc1\x1b\xc6h\xe7\x1eS\xf0\x11\xf8Z\x8c\x92\x87\x88dU\xe9\xd6:\xc6=\x9eL\xfd1\x12Z\x80@9\xbd("\xba\xa7\x0c\xeb\x02)\xed\xf4\xdc^\x0bm\xcaW\x9b\xabd\x14\xa2=`\x12O\x13\xcb\x88\x85\x88\x13-CM@\x92\xd4>\x88%\x8f\xd6\xed8\x0c\x99\xb74 \x91\x80\x00\t\x0eu\x80\x16\xf36\xd9\xd2\xe6\xe9\x81P\x15\x04\x86\x1f\xbc\x01\x90z,\xca\x13\x90\x8f\xcf\xb8\x8c\x02\x05\xd1:\x98Rgk1\xaef\x92A\xbdURR\xbc\xc1\xafQ\x89\xe2]f\xa0\xd6\xd9.C\xa0)n\xa6\xa0\x86\xf1\xca1\xd0,\xd6\xcc\x81&\xf1\xd2 \xfc\xb3\xba\xda$hr5\xa3\xa0I\xbc\xc1,d\x1d\xa8\x9f\x85\xbd\x96\xf5\xce\x83\xb3em\xab\x01\xd5mo\nu\x9c\x159\'\x80\xc5\x89Qm\xe9\x91\xb63\xbax\xef\xfd|\xbc\xc5\xfc\x8amk\xbdaE/\xff\xbb\x8a^\x1e\xf3\xfc\x9aj\xfb>\x91\xfb\xbe\x0c\xe9\xf2\xda_\x05\x84zR\xf0\xb0\xf1\xbe\t\xbc\xe0\xa8\x07\xdd\x1ec\xfe\xb6G\xdb\xbe\xa7W\xa6s\xf0-\xee\x90\x1b\\\x1d\x96_{dU \xfd"\x9cw\xbb\xb5\xedpc{\x11\xed\xb5H/\x817?\xa0\x0c\t\xccr\xb7\x01\xcdYs3H\xa4L\xb3\xf1\xc0\xe0\x1b\np>\xf9}\xfegZ\x80\x06\xa5\x9fGn\x8a\x8b\x86\r\xa0\nq\xaa\xdf\xca\x9czK8+\xd9\xfc\x0bq\x81*\xd1\x92\xb9S\xc9\xf0\xca\xfdHHz$qy\x10\x03\x98%2\x81g\xdf9\xa3\xdb\xe1\xe3`\xdc\x1f\xda\xbe\x0c]\x99\xc5\xef\x98.%n\x16D`!\xb84e)\x16\xec\x08\x87d\x93<\xf4_\xe1\xc1\x17\x1d\xa8vT\xd2\xf8\xf3\xc0\x99u\x9d\xd1\xe8\xfa\xc1)\x0fCY\x95\xe29\xa1\x9a\xee\xd3\xf5\x8d\xf34\x1b:\x03\xe7z\xec\xdc\xb5+(\nql*Y[Y\xec\xe5\xceH8V5\xd5ZiJ\x84\xee\x96\x93\xd3{\xee\x96\r\x13\x80\xc5L\x96\x07\x95\xa4S\xb2\xb4b\xa7\x9e\x92I\xfa\x9a\xa6\x85\xacn\x07\xb3q\x92\xb4\xd1I\xd2@\'\xc8T\xac\xf8KJS\xe3\xd6\xc6OK\x8dZOsWkY\xfa-\xe3/\xc2\x8e\x19\xd7')]) 

# Creating all code files on target project
for f in _context.files:
	file_system.wFile(file_system.get_current_location()+'/'+f.file,zlib.decompress(f.code).decode(),force=True)

    
_architect.Save()
    