# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SylkServer.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper

from typing import overload, Iterator, List, Dict
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10SylkServer.proto\x12\x12sylk.SylkServer.v1\"C\n\nSylkServer\x12\x35\n\x08language\x18\x01 \x01(\x0e\x32#.sylk.SylkServer.v1.ServerLanguages*^\n\x0fServerLanguages\x12\x1b\n\x17UNKNOWN_SERVERLANGUAGES\x10\x00\x12\n\n\x06python\x10\x01\x12\n\n\x06nodejs\x10\x02\x12\x0e\n\ntypescript\x10\x03\x12\x06\n\x02go\x10\x04\x42\x31Z/github.com/sylk/core/services/protos/SylkServerb\x06proto3')

_SERVERLANGUAGES = DESCRIPTOR.enum_types_by_name['ServerLanguages']
ServerLanguages = enum_type_wrapper.EnumTypeWrapper(_SERVERLANGUAGES)
UNKNOWN_SERVERLANGUAGES = 0
python = 1
nodejs = 2
typescript = 3
go = 4


_SYLKSERVER = DESCRIPTOR.message_types_by_name['SylkServer']

@overload
class SylkServer(_message.Message):
	"""webezyio generated message [sylk.SylkServer.v1.SylkServer]
	A class respresent a SylkServer type
	
	"""
	language = enum_type_wrapper.EnumTypeWrapper # type: enum_type_wrapper.EnumTypeWrapper

	def __init__(self, language=enum_type_wrapper.EnumTypeWrapper):
		"""
		Attributes:
		----------
		language : enum_type_wrapper.EnumTypeWrapper
			
		"""
		pass
SylkServer = _reflection.GeneratedProtocolMessageType('SylkServer', (_message.Message,), {
  'DESCRIPTOR' : _SYLKSERVER,
  '__module__' : 'SylkServer_pb2'
  # @@protoc_insertion_point(class_scope:sylk.SylkServer.v1.SylkServer)
  })
_sym_db.RegisterMessage(SylkServer)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z/github.com/sylk/core/services/protos/SylkServer'
  _SERVERLANGUAGES._serialized_start=109
  _SERVERLANGUAGES._serialized_end=203
  _SYLKSERVER._serialized_start=40
  _SYLKSERVER._serialized_end=107
# @@protoc_insertion_point(module_scope)