
"""Init script for webezy.io template io
Generated thanks to -

                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| | _ | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |(_)|_| \___/ 
                                   |___/              

A basic sample project for webezyio.    It is included with examples for all RPC's types    and using Enums + Nested Messages, including 'Well Known'    messages from google

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
                    prog = 'io',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--domain',default='webezy')           # optional argument
parser.add_argument('--project-name',default='io')           # optional argument

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
# Here we configured a python clients to be created with our services    
_clients = [{'language': 'python', 'out_dir': file_system.join_path(_PATH, 'clients', Language.Name(Language.python))}]
    
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

# Instantiating all enum values for [webezy_io_v1_LoggingLevels]
_enum_values_webezy_io_v1_LoggingLevels = [helpers.WZEnumValue('UNKNWON_LOG_LEVEL',0,description='None'),
	helpers.WZEnumValue('DEBUG',1,description='The most verbose logging, will show all - DEBUG'),
	helpers.WZEnumValue('INFO',2,description='Will show all log levels after - INFO'),
	helpers.WZEnumValue('WARNING',3,description='Second most critical logging, wll show all log levels after - WARNING'),
	helpers.WZEnumValue('ERROR',4,description='Most critical logging level, will show only - ERROR')]
# Instantiating all enum values for [webezy_io_v1_ValidationTypes]
_enum_values_webezy_io_v1_ValidationTypes = [helpers.WZEnumValue('UNKNOWN_VALIDATION',0,description='None'),
	helpers.WZEnumValue('NUMERIC',1,description='Numeric validations using filters'),
	helpers.WZEnumValue('TEXT',2,description='String validations using RegEx')]
# Instantiating all enum values for [webezy_io_v1_Validations]
_enum_values_webezy_io_v1_Validations = [helpers.WZEnumValue('UNKNOWN_NUM_VALIDATION',0,description='None'),
	helpers.WZEnumValue('EQ',1,description='Equal to the value passed'),
	helpers.WZEnumValue('LT',2,description='Less than to the value passed'),
	helpers.WZEnumValue('GT',3,description='Greater than to the value passed'),
	helpers.WZEnumValue('LTE',4,description='Less than or equal to the value passed'),
	helpers.WZEnumValue('GTE',5,description='Greate than or equal to the value passed'),
	helpers.WZEnumValue('NOT',6,description='Not equal to the value passed')]
        
# Creating enums   

# Constructing enum [webezy_io_v1_LoggingLevels]
_enum_webezy_io_v1_LoggingLevels = helpers.WZEnum('LoggingLevels',enum_values=_enum_values_webezy_io_v1_LoggingLevels)
# Constructing enum [webezy_io_v1_ValidationTypes]
_enum_webezy_io_v1_ValidationTypes = helpers.WZEnum('ValidationTypes',enum_values=_enum_values_webezy_io_v1_ValidationTypes)
# Constructing enum [webezy_io_v1_Validations]
_enum_webezy_io_v1_Validations = helpers.WZEnum('Validations',enum_values=_enum_values_webezy_io_v1_Validations) 
        
"""Packages and thier resources"""
# Construct fields    

# Constructing a field for [webezy_io_v1_ConsoleLoggingOptions_level]
_field_webezy_io_v1_ConsoleLoggingOptions_level = helpers.WZField(name='level',
                              description='A logging level constant to be used at ConsoleLogger',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.io.v1.LoggingLevels',
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldValidation_field]
_field_webezy_io_v1_FieldValidation_field = helpers.WZField(name='field',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldValidation_validation]
_field_webezy_io_v1_FieldValidation_validation = helpers.WZField(name='validation',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.io.v1.ValidationTypes',
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldValidation_filter]
_field_webezy_io_v1_FieldValidation_filter = helpers.WZField(name='filter',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.io.v1.Validations',
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldValidation_regex]
_field_webezy_io_v1_FieldValidation_regex = helpers.WZField(name='regex',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldValidation_value]
_field_webezy_io_v1_FieldValidation_value = helpers.WZField(name='value',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_FLOAT',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FileExtensions_ConsoleLogger]
_field_webezy_io_v1_FileExtensions_ConsoleLogger = helpers.WZField(name='ConsoleLogger',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.io.v1.ConsoleLoggingOptions',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_ServiceExtensions_ConsoleLogger]
_field_webezy_io_v1_ServiceExtensions_ConsoleLogger = helpers.WZField(name='ConsoleLogger',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.io.v1.ConsoleLoggingOptions',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_MessageExtensions_fields]
_field_webezy_io_v1_MessageExtensions_fields = helpers.WZField(name='fields',
                              description='None',
                              label='LABEL_REPEATED',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.io.v1.FieldValidation',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldsExtensions_validation]
_field_webezy_io_v1_FieldsExtensions_validation = helpers.WZField(name='validation',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.io.v1.FieldValidation',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Packing all fields for [webezy_io_v1_ConsoleLoggingOptions]
_msg_fields_webezy_io_v1_ConsoleLoggingOptions = [_field_webezy_io_v1_ConsoleLoggingOptions_level]
# Packing all fields for [webezy_io_v1_FieldValidation]
_msg_fields_webezy_io_v1_FieldValidation = [_field_webezy_io_v1_FieldValidation_field,_field_webezy_io_v1_FieldValidation_validation,_field_webezy_io_v1_FieldValidation_filter,_field_webezy_io_v1_FieldValidation_regex,_field_webezy_io_v1_FieldValidation_value]
# Packing all fields for [webezy_io_v1_FileExtensions]
_msg_fields_webezy_io_v1_FileExtensions = [_field_webezy_io_v1_FileExtensions_ConsoleLogger]
# Packing all fields for [webezy_io_v1_ServiceExtensions]
_msg_fields_webezy_io_v1_ServiceExtensions = [_field_webezy_io_v1_ServiceExtensions_ConsoleLogger]
# Packing all fields for [webezy_io_v1_MessageExtensions]
_msg_fields_webezy_io_v1_MessageExtensions = [_field_webezy_io_v1_MessageExtensions_fields]
# Packing all fields for [webezy_io_v1_FieldsExtensions]
_msg_fields_webezy_io_v1_FieldsExtensions = [_field_webezy_io_v1_FieldsExtensions_validation]
    
# Construct messages

# Constructing message [webezy_io_v1_ConsoleLoggingOptions]
_msg_webezy_io_v1_ConsoleLoggingOptions = helpers.WZMessage(name='ConsoleLoggingOptions',
                                 description='The console logger options wrapper message',
                                 fields=_msg_fields_webezy_io_v1_ConsoleLoggingOptions,
                                 extension_type=None,
                                 extensions=None)

# Constructing message [webezy_io_v1_FieldValidation]
_msg_webezy_io_v1_FieldValidation = helpers.WZMessage(name='FieldValidation',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_FieldValidation,
                                 extension_type=None,
                                 extensions=None)

# Constructing message [webezy_io_v1_FileExtensions]
_msg_webezy_io_v1_FileExtensions = helpers.WZMessage(name='FileExtensions',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_FileExtensions,
                                 extension_type='FileOptions',
                                 extensions=None)

# Constructing message [webezy_io_v1_ServiceExtensions]
_msg_webezy_io_v1_ServiceExtensions = helpers.WZMessage(name='ServiceExtensions',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_ServiceExtensions,
                                 extension_type='ServiceOptions',
                                 extensions=None)

# Constructing message [webezy_io_v1_MessageExtensions]
_msg_webezy_io_v1_MessageExtensions = helpers.WZMessage(name='MessageExtensions',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_MessageExtensions,
                                 extension_type='MessageOptions',
                                 extensions=None)

# Constructing message [webezy_io_v1_FieldsExtensions]
_msg_webezy_io_v1_FieldsExtensions = helpers.WZMessage(name='FieldsExtensions',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_FieldsExtensions,
                                 extension_type='FieldOptions',
                                 extensions=None)

    
# Construct packages

_pkg_webezy_io_v1 = helpers.WZPackage(name='io',
                                                messages=[_msg_webezy_io_v1_ConsoleLoggingOptions,_msg_webezy_io_v1_FieldValidation,_msg_webezy_io_v1_FileExtensions,_msg_webezy_io_v1_ServiceExtensions,_msg_webezy_io_v1_MessageExtensions,_msg_webezy_io_v1_FieldsExtensions],
                                                enums=[_enum_webezy_io_v1_LoggingLevels,_enum_webezy_io_v1_ValidationTypes,_enum_webezy_io_v1_Validations],
                                                extensions=None)

# Unpacking package [webezy_io_v1]
_pkg_webezy_io_v1_name, _pkg_webezy_io_v1_messages, _pkg_webezy_io_v1_enums, _pkg_webezy_io_v1_ext, _pkg_webezy_io_v1_domain = _pkg_webezy_io_v1.to_tuple()
    
# Add packages

# Adding package [webezy_io_v1]
_pkg_webezy_io_v1 = _architect.AddPackage(_pkg_webezy_io_v1_name,
                                                    dependencies=[],
                                                    description='This is the webezy.io package for most of the core modules that are handy to use at webezy.io projects.',
                                                    domain=_pkg_webezy_io_v1_domain,
                                                    extensions=_pkg_webezy_io_v1_ext)
    
msgs_map = {}

# Add packages messages

for m in _pkg_webezy_io_v1_messages:
	msg_name, msg_fields, msg_desc, msg_opt, msg_domain = m
	temp_msg = _architect.AddMessage(_pkg_webezy_io_v1, msg_name, msg_fields, msg_desc, msg_opt, msg_domain)
	msgs_map[temp_msg.full_name] = temp_msg
    
# Add packages enums

for e in _pkg_webezy_io_v1_enums:
	enum_name, enum_values, enum_desc, enum_domain = e
	_architect.AddEnum(_pkg_webezy_io_v1, enum_name, enum_values, enum_desc, enum_domain)
    
_architect.Save()
    