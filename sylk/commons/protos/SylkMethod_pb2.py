# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SylkMethod.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor

from typing import overload, Iterator, List, Dict
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10SylkMethod.proto\x12\x12sylk.SylkMethod.v1\x1a\x1cgoogle/protobuf/struct.proto\"\xac\x01\n\nSylkMethod\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x12\n\ninput_type\x18\x04 \x01(\t\x12\x13\n\x0boutput_type\x18\x05 \x01(\t\x12\x18\n\x10\x63lient_streaming\x18\x06 \x01(\x08\x12\x18\n\x10server_streaming\x18\x07 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\tB1Z/github.com/sylk/core/services/protos/SylkMethodb\x06proto3')



_SYLKMETHOD = DESCRIPTOR.message_types_by_name['SylkMethod']

@overload
class SylkMethod(_message.Message):
	"""webezyio generated message [sylk.SylkMethod.v1.SylkMethod]
	A class respresent a SylkMethod type
	
	"""
	uri = str # type: str
	name = str # type: str
	full_name = str # type: str
	input_type = str # type: str
	output_type = str # type: str
	client_streaming = bool # type: bool
	server_streaming = bool # type: bool
	description = str # type: str

	def __init__(self, uri=str, name=str, full_name=str, input_type=str, output_type=str, client_streaming=bool, server_streaming=bool, description=str):
		"""
		Attributes:
		----------
		uri : str
			
		name : str
			
		full_name : str
			
		input_type : str
			
		output_type : str
			
		client_streaming : bool
			
		server_streaming : bool
			
		description : str
			
		"""
		pass
SylkMethod = _reflection.GeneratedProtocolMessageType('SylkMethod', (_message.Message,), {
  'DESCRIPTOR' : _SYLKMETHOD,
  '__module__' : 'SylkMethod_pb2'
  # @@protoc_insertion_point(class_scope:sylk.SylkMethod.v1.SylkMethod)
  })
_sym_db.RegisterMessage(SylkMethod)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z/github.com/sylk/core/services/protos/SylkMethod'
  _SYLKMETHOD._serialized_start=71
  _SYLKMETHOD._serialized_end=243
# @@protoc_insertion_point(module_scope)
