
"""Init script for webezy.io template testproject
Generated thanks to -

                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| | _ | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |(_)|_| \___/ 
                                   |___/              



Author: Unknown
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
                    prog = 'TEST-PROJECT',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--domain',default='webezy')           # optional argument
parser.add_argument('--project-name',default='TEST-PROJECT')           # optional argument

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
_enum_values_webezy_io_v1_LoggingLevels = [helpers.WZEnumValue('UNKNWON_LOG_LEVEL',0),helpers.WZEnumValue('DEBUG',1),helpers.WZEnumValue('INFO',2),helpers.WZEnumValue('WARNING',3),helpers.WZEnumValue('ERROR',4)]
# Instantiating all enum values for [webezy_io_v1_ValidationTypes]
_enum_values_webezy_io_v1_ValidationTypes = [helpers.WZEnumValue('UNKNOWN_VALIDATION',0),helpers.WZEnumValue('NUMERIC',1),helpers.WZEnumValue('TEXT',2)]
# Instantiating all enum values for [webezy_io_v1_NumericValidations]
_enum_values_webezy_io_v1_NumericValidations = [helpers.WZEnumValue('UNKNOWN_NUM_VALIDATION',0),helpers.WZEnumValue('EQ',1),helpers.WZEnumValue('LT',2),helpers.WZEnumValue('GT',3),helpers.WZEnumValue('LTE',4),helpers.WZEnumValue('GTE',5),helpers.WZEnumValue('NOT',6)]
        
# Creating enums   

# Constructing enum [webezy_io_v1_LoggingLevels]
_enum_webezy_io_v1_LoggingLevels = helpers.WZEnum('LoggingLevels',enum_values=_enum_values_webezy_io_v1_LoggingLevels)
# Constructing enum [webezy_io_v1_ValidationTypes]
_enum_webezy_io_v1_ValidationTypes = helpers.WZEnum('ValidationTypes',enum_values=_enum_values_webezy_io_v1_ValidationTypes)
# Constructing enum [webezy_io_v1_NumericValidations]
_enum_webezy_io_v1_NumericValidations = helpers.WZEnum('NumericValidations',enum_values=_enum_values_webezy_io_v1_NumericValidations) 
        
"""Packages and thier resources"""
# Construct fields    

# Constructing a field for [webezy_io_v1_ConsoleLoggingOptions_level]
_field_webezy_io_v1_ConsoleLoggingOptions_level = helpers.WZField(name='level',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.io.v1.LoggingLevels',
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_ClientLogging_ConsoleLogger]
_field_webezy_io_v1_ClientLogging_ConsoleLogger = helpers.WZField(name='ConsoleLogger',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.io.v1.ConsoleLoggingOptions',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldInputValidation_field]
_field_webezy_io_v1_FieldInputValidation_field = helpers.WZField(name='field',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldInputValidation_validation]
_field_webezy_io_v1_FieldInputValidation_validation = helpers.WZField(name='validation',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.io.v1.ValidationTypes',
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldInputValidation_numeric_filter]
_field_webezy_io_v1_FieldInputValidation_numeric_filter = helpers.WZField(name='numeric_filter',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_ENUM',
                              message_type=None,
                              enum_type=_DOMAIN+'.io.v1.NumericValidations',
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldInputValidation_text_filter]
_field_webezy_io_v1_FieldInputValidation_text_filter = helpers.WZField(name='text_filter',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_STRING',
                              message_type=None,
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_RequestValidation_fields]
_field_webezy_io_v1_RequestValidation_fields = helpers.WZField(name='fields',
                              description='None',
                              label='LABEL_REPEATED',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.io.v1.FieldInputValidation',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Constructing a field for [webezy_io_v1_FieldValidation_field_validation]
_field_webezy_io_v1_FieldValidation_field_validation = helpers.WZField(name='field_validation',
                              description='None',
                              label='LABEL_OPTIONAL',
                              type='TYPE_MESSAGE',
                              message_type=_DOMAIN + '.io.v1.FieldInputValidation',
                              enum_type=None,
                              key_type=None,
                              value_type=None,
                              oneof_fields=None, # Not supporting templating with oneof_fields !
                              extensions=None)

# Packing all fields for [webezy_io_v1_ConsoleLoggingOptions]
_msg_fields_webezy_io_v1_ConsoleLoggingOptions = [_field_webezy_io_v1_ConsoleLoggingOptions_level]
# Packing all fields for [webezy_io_v1_ClientLogging]
_msg_fields_webezy_io_v1_ClientLogging = [_field_webezy_io_v1_ClientLogging_ConsoleLogger]
# Packing all fields for [webezy_io_v1_FieldInputValidation]
_msg_fields_webezy_io_v1_FieldInputValidation = [_field_webezy_io_v1_FieldInputValidation_field,_field_webezy_io_v1_FieldInputValidation_validation,_field_webezy_io_v1_FieldInputValidation_numeric_filter,_field_webezy_io_v1_FieldInputValidation_text_filter]
# Packing all fields for [webezy_io_v1_RequestValidation]
_msg_fields_webezy_io_v1_RequestValidation = [_field_webezy_io_v1_RequestValidation_fields]
# Packing all fields for [webezy_io_v1_FieldValidation]
_msg_fields_webezy_io_v1_FieldValidation = [_field_webezy_io_v1_FieldValidation_field_validation]
    
# Construct messages

# Constructing message [webezy_io_v1_ConsoleLoggingOptions]
_msg_webezy_io_v1_ConsoleLoggingOptions = helpers.WZMessage(name='ConsoleLoggingOptions',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_ConsoleLoggingOptions,
                                 extension_type=None,
                                 extensions=None)

# Constructing message [webezy_io_v1_ClientLogging]
_msg_webezy_io_v1_ClientLogging = helpers.WZMessage(name='ClientLogging',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_ClientLogging,
                                 extension_type='FileOptions',
                                 extensions=None)

# Constructing message [webezy_io_v1_FieldInputValidation]
_msg_webezy_io_v1_FieldInputValidation = helpers.WZMessage(name='FieldInputValidation',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_FieldInputValidation,
                                 extension_type=None,
                                 extensions=None)

# Constructing message [webezy_io_v1_RequestValidation]
_msg_webezy_io_v1_RequestValidation = helpers.WZMessage(name='RequestValidation',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_RequestValidation,
                                 extension_type='MessageOptions',
                                 extensions=None)

# Constructing message [webezy_io_v1_FieldValidation]
_msg_webezy_io_v1_FieldValidation = helpers.WZMessage(name='FieldValidation',
                                 description='None',
                                 fields=_msg_fields_webezy_io_v1_FieldValidation,
                                 extension_type='FieldOptions',
                                 extensions=None)

    
# Construct packages

_pkg_webezy_io_v1 = helpers.WZPackage(name='io',
                                                messages=[_msg_webezy_io_v1_ConsoleLoggingOptions,_msg_webezy_io_v1_ClientLogging,_msg_webezy_io_v1_FieldInputValidation,_msg_webezy_io_v1_RequestValidation,_msg_webezy_io_v1_FieldValidation],
                                                enums=[_enum_webezy_io_v1_LoggingLevels,_enum_webezy_io_v1_ValidationTypes,_enum_webezy_io_v1_NumericValidations],
                                                extensions=None)

# Unpacking package [webezy_io_v1]
_pkg_webezy_io_v1_name, _pkg_webezy_io_v1_messages, _pkg_webezy_io_v1_enums = _pkg_webezy_io_v1.to_tuple()
    
# Add packages

# Adding package [webezy_io_v1]
_pkg_webezy_io_v1 = _architect.AddPackage(_pkg_webezy_io_v1_name,
                                                    dependencies=[],
                                                    description='None')
    
msgs_map = {}

# Add packages messages

for m in _pkg_webezy_io_v1_messages:
	msg_name, msg_fields, msg_desc, msg_opt = m
	temp_msg = _architect.AddMessage(_pkg_webezy_io_v1, msg_name, msg_fields, msg_desc, msg_opt)
	msgs_map[temp_msg.full_name] = temp_msg
    
# Add packages enums

for e in _pkg_webezy_io_v1_enums:
	enum_name, enum_values, enum_desc = e
	_architect.AddEnum(_pkg_webezy_io_v1, enum_name, enum_values, enum_desc)
    
_architect.Save()
    