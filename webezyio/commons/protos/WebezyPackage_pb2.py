# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: WebezyPackage.proto
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


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13WebezyPackage.proto\x12\x17webezy.WebezyPackage.v1\x1a\x1cgoogle/protobuf/struct.proto\"\xec\x04\n\x0bWebezyField\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05index\x18\x04 \x01(\x05\x12<\n\nfield_type\x18\x05 \x01(\x0e\x32(.webezy.WebezyPackage.v1.WebezyFieldType\x12\x38\n\x05label\x18\x06 \x01(\x0e\x32).webezy.WebezyPackage.v1.WebezyFieldLabel\x12\x11\n\tenum_type\x18\x07 \x01(\t\x12\x14\n\x0cmessage_type\x18\x08 \x01(\t\x12\x0c\n\x04type\x18\t \x01(\t\x12\x0c\n\x04kind\x18\n \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x0b \x01(\t\x12:\n\x08key_type\x18\x0c \x01(\x0e\x32(.webezy.WebezyPackage.v1.WebezyFieldType\x12<\n\nvalue_type\x18\r \x01(\x0e\x32(.webezy.WebezyPackage.v1.WebezyFieldType\x12H\n\nextensions\x18\x0e \x03(\x0b\x32\x34.webezy.WebezyPackage.v1.WebezyField.ExtensionsEntry\x12?\n\x0coneof_fields\x18\x0f \x03(\x0b\x32).webezy.WebezyPackage.v1.WebezyOneOfField\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\"|\n\x0fWebezyEnumValue\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06number\x18\x03 \x01(\x05\x12\r\n\x05index\x18\x04 \x01(\x05\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x0c\n\x04kind\x18\x06 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\"\xa5\x01\n\nWebezyEnum\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x38\n\x06values\x18\x04 \x03(\x0b\x32(.webezy.WebezyPackage.v1.WebezyEnumValue\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x0c\n\x04kind\x18\x06 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\"\xfd\x02\n\rWebezyMessage\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x34\n\x06\x66ields\x18\x04 \x03(\x0b\x32$.webezy.WebezyPackage.v1.WebezyField\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x0c\n\x04kind\x18\x06 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\x12@\n\x0e\x65xtension_type\x18\x08 \x01(\x0e\x32(.webezy.WebezyPackage.v1.WebezyExtension\x12J\n\nextensions\x18\t \x03(\x0b\x32\x36.webezy.WebezyPackage.v1.WebezyMessage.ExtensionsEntry\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\"\x98\x03\n\rWebezyPackage\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07package\x18\x03 \x01(\t\x12\x0f\n\x07version\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x0c\n\x04type\x18\x06 \x01(\t\x12\x0c\n\x04kind\x18\x07 \x01(\t\x12\x38\n\x08messages\x18\x08 \x03(\x0b\x32&.webezy.WebezyPackage.v1.WebezyMessage\x12\x32\n\x05\x65nums\x18\t \x03(\x0b\x32#.webezy.WebezyPackage.v1.WebezyEnum\x12J\n\nextensions\x18\n \x03(\x0b\x32\x36.webezy.WebezyPackage.v1.WebezyPackage.ExtensionsEntry\x12\x14\n\x0c\x64\x65pendencies\x18\x0b \x03(\t\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\"\x81\x03\n\x10WebezyOneOfField\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05index\x18\x04 \x01(\x05\x12\x11\n\tenum_type\x18\x05 \x01(\t\x12\x14\n\x0cmessage_type\x18\x06 \x01(\t\x12\x0c\n\x04type\x18\x07 \x01(\t\x12\x0c\n\x04kind\x18\x08 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\t \x01(\t\x12M\n\nextensions\x18\n \x03(\x0b\x32\x39.webezy.WebezyPackage.v1.WebezyOneOfField.ExtensionsEntry\x12<\n\nfield_type\x18\x0b \x01(\x0e\x32(.webezy.WebezyPackage.v1.WebezyFieldType\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01*l\n\x10WebezyFieldLabel\x12\x1c\n\x18UNKNOWN_WEBEZYFIELDLABEL\x10\x00\x12\x12\n\x0eLABEL_OPTIONAL\x10\x01\x12\x12\n\x0eLABEL_REQUIRED\x10\x02\x12\x12\n\x0eLABEL_REPEATED\x10\x03*\xfc\x02\n\x0fWebezyFieldType\x12\x1b\n\x17UNKNOWN_WEBEZYFIELDTYPE\x10\x00\x12\x0f\n\x0bTYPE_DOUBLE\x10\x01\x12\x0e\n\nTYPE_FLOAT\x10\x02\x12\x0e\n\nTYPE_INT64\x10\x03\x12\x0f\n\x0bTYPE_UINT64\x10\x04\x12\x0e\n\nTYPE_INT32\x10\x05\x12\x10\n\x0cTYPE_FIXED64\x10\x06\x12\x10\n\x0cTYPE_FIXED32\x10\x07\x12\r\n\tTYPE_BOOL\x10\x08\x12\x0f\n\x0bTYPE_STRING\x10\t\x12\x0e\n\nTYPE_GROUP\x10\n\x12\x10\n\x0cTYPE_MESSAGE\x10\x0b\x12\x0e\n\nTYPE_BYTES\x10\x0c\x12\x0f\n\x0bTYPE_UINT32\x10\r\x12\r\n\tTYPE_ENUM\x10\x0e\x12\x11\n\rTYPE_SFIXED32\x10\x0f\x12\x11\n\rTYPE_SFIXED64\x10\x10\x12\x0f\n\x0bTYPE_SINT32\x10\x11\x12\x0f\n\x0bTYPE_SINT64\x10\x12\x12\x0c\n\x08TYPE_MAP\x10\x13\x12\x0e\n\nTYPE_ONEOF\x10\x14*\x8c\x01\n\x0fWebezyExtension\x12\x1b\n\x17UNKNOWN_WEBEZYEXTENSION\x10\x00\x12\x0f\n\x0b\x46ileOptions\x10\x01\x12\x12\n\x0eMessageOptions\x10\x02\x12\x10\n\x0c\x46ieldOptions\x10\x03\x12\x12\n\x0eServiceOptions\x10\x04\x12\x11\n\rMethodOptions\x10\x05\x62\x06proto3')

_WEBEZYFIELDLABEL = DESCRIPTOR.enum_types_by_name['WebezyFieldLabel']
WebezyFieldLabel = enum_type_wrapper.EnumTypeWrapper(_WEBEZYFIELDLABEL)
_WEBEZYFIELDTYPE = DESCRIPTOR.enum_types_by_name['WebezyFieldType']
WebezyFieldType = enum_type_wrapper.EnumTypeWrapper(_WEBEZYFIELDTYPE)
_WEBEZYEXTENSION = DESCRIPTOR.enum_types_by_name['WebezyExtension']
WebezyExtension = enum_type_wrapper.EnumTypeWrapper(_WEBEZYEXTENSION)
UNKNOWN_WEBEZYFIELDLABEL = 0
LABEL_OPTIONAL = 1
LABEL_REQUIRED = 2
LABEL_REPEATED = 3
UNKNOWN_WEBEZYFIELDTYPE = 0
TYPE_DOUBLE = 1
TYPE_FLOAT = 2
TYPE_INT64 = 3
TYPE_UINT64 = 4
TYPE_INT32 = 5
TYPE_FIXED64 = 6
TYPE_FIXED32 = 7
TYPE_BOOL = 8
TYPE_STRING = 9
TYPE_GROUP = 10
TYPE_MESSAGE = 11
TYPE_BYTES = 12
TYPE_UINT32 = 13
TYPE_ENUM = 14
TYPE_SFIXED32 = 15
TYPE_SFIXED64 = 16
TYPE_SINT32 = 17
TYPE_SINT64 = 18
TYPE_MAP = 19
TYPE_ONEOF = 20
UNKNOWN_WEBEZYEXTENSION = 0
FileOptions = 1
MessageOptions = 2
FieldOptions = 3
ServiceOptions = 4
MethodOptions = 5


_WEBEZYFIELD = DESCRIPTOR.message_types_by_name['WebezyField']
_WEBEZYFIELD_EXTENSIONSENTRY = _WEBEZYFIELD.nested_types_by_name['ExtensionsEntry']
_WEBEZYENUMVALUE = DESCRIPTOR.message_types_by_name['WebezyEnumValue']
_WEBEZYENUM = DESCRIPTOR.message_types_by_name['WebezyEnum']
_WEBEZYMESSAGE = DESCRIPTOR.message_types_by_name['WebezyMessage']
_WEBEZYMESSAGE_EXTENSIONSENTRY = _WEBEZYMESSAGE.nested_types_by_name['ExtensionsEntry']
_WEBEZYPACKAGE = DESCRIPTOR.message_types_by_name['WebezyPackage']
_WEBEZYPACKAGE_EXTENSIONSENTRY = _WEBEZYPACKAGE.nested_types_by_name['ExtensionsEntry']
_WEBEZYONEOFFIELD = DESCRIPTOR.message_types_by_name['WebezyOneOfField']
_WEBEZYONEOFFIELD_EXTENSIONSENTRY = _WEBEZYONEOFFIELD.nested_types_by_name['ExtensionsEntry']

@overload
class WebezyOneOfField(_message.Message):
	"""webezyio generated message [webezy.WebezyPackage.v1.WebezyOneOfField]
	A class respresent a WebezyOneOfField type
	
		"""
	uri = str # type: str
	name = str # type: str
	full_name = str # type: str
	index = int # type: int
	enum_type = str # type: str
	message_type = str # type: str
	type = str # type: str
	kind = str # type: str
	description = str # type: str
	extensions = Dict[str,google_dot_protobuf_dot_struct__pb2.Value] # type: Dict[str,google_dot_protobuf_dot_struct__pb2.Value]
	field_type = enum_type_wrapper.EnumTypeWrapper # type: enum_type_wrapper.EnumTypeWrapper

	def __init__(self, uri=str, name=str, full_name=str, index=int, enum_type=str, message_type=str, type=str, kind=str, description=str, extensions=Dict[str,google_dot_protobuf_dot_struct__pb2.Value], field_type=enum_type_wrapper.EnumTypeWrapper):
		"""
		Attributes:
		----------
		uri : str
			
		name : str
			
		full_name : str
			
		index : int
			
		enum_type : str
			
		message_type : str
			
		type : str
			
		kind : str
			
		description : str
			
		extensions : Dict[str,google_dot_protobuf_dot_struct__pb2.Value]
			A map of pluggable extensions into field
		field_type : enum_type_wrapper.EnumTypeWrapper
			
		"""
		pass
WebezyOneOfField = _reflection.GeneratedProtocolMessageType('WebezyOneOfField', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _WEBEZYONEOFFIELD_EXTENSIONSENTRY,
    '__module__' : 'WebezyPackage_pb2'
    # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyOneOfField.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _WEBEZYONEOFFIELD,
  '__module__' : 'WebezyPackage_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyOneOfField)
  })
_sym_db.RegisterMessage(WebezyOneOfField)
_sym_db.RegisterMessage(WebezyOneOfField.ExtensionsEntry)


@overload
class WebezyField(_message.Message):
	"""webezyio generated message [webezy.WebezyPackage.v1.WebezyField]
	A class respresent a WebezyField type
	The webezy field descriptor
		"""
	uri = str # type: str
	name = str # type: str
	full_name = str # type: str
	index = int # type: int
	field_type = enum_type_wrapper.EnumTypeWrapper # type: enum_type_wrapper.EnumTypeWrapper
	label = enum_type_wrapper.EnumTypeWrapper # type: enum_type_wrapper.EnumTypeWrapper
	enum_type = str # type: str
	message_type = str # type: str
	type = str # type: str
	kind = str # type: str
	description = str # type: str
	key_type = enum_type_wrapper.EnumTypeWrapper # type: enum_type_wrapper.EnumTypeWrapper
	value_type = enum_type_wrapper.EnumTypeWrapper # type: enum_type_wrapper.EnumTypeWrapper
	extensions = Dict[str,google_dot_protobuf_dot_struct__pb2.Value] # type: Dict[str,google_dot_protobuf_dot_struct__pb2.Value]
	oneof_fields = List[WebezyOneOfField] # type: List[WebezyOneOfField]

	def __init__(self, uri=str, name=str, full_name=str, index=int, field_type=enum_type_wrapper.EnumTypeWrapper, label=enum_type_wrapper.EnumTypeWrapper, enum_type=str, message_type=str, type=str, kind=str, description=str, key_type=enum_type_wrapper.EnumTypeWrapper, value_type=enum_type_wrapper.EnumTypeWrapper, extensions=Dict[str,google_dot_protobuf_dot_struct__pb2.Value], oneof_fields=List[WebezyOneOfField]):
		"""
		Attributes:
		----------
		uri : str
			The field URI
		name : str
			The field name
		full_name : str
			The field full name <domain>.<package>.<version>.<message>.<field>
		index : int
			The field index at the message level hierarchy
		field_type : enum_type_wrapper.EnumTypeWrapper
			The field type
		label : enum_type_wrapper.EnumTypeWrapper
			The field label
		enum_type : str
			If field is type ENUM this field MUST be populated with full resource name of the ENUM
		message_type : str
			If the field type is of type MESSAGE then this field MUST be populated with the full resource name of the MESSAGE
		type : str
			The message resource type
		kind : str
			The message resource kind
		description : str
			The field human readable description
		key_type : enum_type_wrapper.EnumTypeWrapper
			If field is of type MAP then this field MUST be populated with the map< KEY,> type
		value_type : enum_type_wrapper.EnumTypeWrapper
			If field is of type MAP then this field MUST be populated with the map<, VALUE> type
		extensions : Dict[str,google_dot_protobuf_dot_struct__pb2.Value]
			The field extensions
		oneof_fields : List[WebezyOneOfField]
			
		"""
		pass
WebezyField = _reflection.GeneratedProtocolMessageType('WebezyField', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _WEBEZYFIELD_EXTENSIONSENTRY,
    '__module__' : 'WebezyPackage_pb2'
    # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyField.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _WEBEZYFIELD,
  '__module__' : 'WebezyPackage_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyField)
  })
_sym_db.RegisterMessage(WebezyField)
_sym_db.RegisterMessage(WebezyField.ExtensionsEntry)


@overload
class WebezyEnumValue(_message.Message):
	"""webezyio generated message [webezy.WebezyPackage.v1.WebezyEnumValue]
	A class respresent a WebezyEnumValue type
	The webezy enum value descriptor
		"""
	uri = str # type: str
	name = str # type: str
	number = int # type: int
	index = int # type: int
	type = str # type: str
	kind = str # type: str
	description = str # type: str

	def __init__(self, uri=str, name=str, number=int, index=int, type=str, kind=str, description=str):
		"""
		Attributes:
		----------
		uri : str
			Enum value URI
		name : str
			Enum value name
		number : int
			Enum value number (value)
		index : int
			The enum value index at the enum values array
		type : str
			Enum value type
		kind : str
			Enum value kind
		description : str
			Human readable description for the enum value
		"""
		pass
WebezyEnumValue = _reflection.GeneratedProtocolMessageType('WebezyEnumValue', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYENUMVALUE,
  '__module__' : 'WebezyPackage_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyEnumValue)
  })
_sym_db.RegisterMessage(WebezyEnumValue)


@overload
class WebezyEnum(_message.Message):
	"""webezyio generated message [webezy.WebezyPackage.v1.WebezyEnum]
	A class respresent a WebezyEnum type
	The webezy enum descriptor
		"""
	uri = str # type: str
	name = str # type: str
	full_name = str # type: str
	values = List[WebezyEnumValue] # type: List[WebezyEnumValue]
	type = str # type: str
	kind = str # type: str
	description = str # type: str

	def __init__(self, uri=str, name=str, full_name=str, values=List[WebezyEnumValue], type=str, kind=str, description=str):
		"""
		Attributes:
		----------
		uri : str
			Enum URI
		name : str
			Enum name
		full_name : str
			Enum full name <domain>.<package>.<version>.<enum>
		values : List[WebezyEnumValue]
			Array of enum value
		type : str
			Enum type
		kind : str
			Enum kind
		description : str
			Enum human readable description
		"""
		pass
WebezyEnum = _reflection.GeneratedProtocolMessageType('WebezyEnum', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYENUM,
  '__module__' : 'WebezyPackage_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyEnum)
  })
_sym_db.RegisterMessage(WebezyEnum)


@overload
class WebezyMessage(_message.Message):
	"""webezyio generated message [webezy.WebezyPackage.v1.WebezyMessage]
	A class respresent a WebezyMessage type
	The webezy message descriptor
		"""
	uri = str # type: str
	name = str # type: str
	full_name = str # type: str
	fields = List[WebezyField] # type: List[WebezyField]
	type = str # type: str
	kind = str # type: str
	description = str # type: str
	extension_type = enum_type_wrapper.EnumTypeWrapper # type: enum_type_wrapper.EnumTypeWrapper
	extensions = Dict[str,google_dot_protobuf_dot_struct__pb2.Value] # type: Dict[str,google_dot_protobuf_dot_struct__pb2.Value]

	def __init__(self, uri=str, name=str, full_name=str, fields=List[WebezyField], type=str, kind=str, description=str, extension_type=enum_type_wrapper.EnumTypeWrapper, extensions=Dict[str,google_dot_protobuf_dot_struct__pb2.Value]):
		"""
		Attributes:
		----------
		uri : str
			Message URI
		name : str
			Message name
		full_name : str
			Message full name <domain>.<package>.<version>.<message>
		fields : List[WebezyField]
			The fields array under the specified message type
		type : str
			Message type
		kind : str
			Message kind
		description : str
			Human readable message description
		extension_type : enum_type_wrapper.EnumTypeWrapper
			Optional if to extend this message
		extensions : Dict[str,google_dot_protobuf_dot_struct__pb2.Value]
			A map of pluggable extensions into message
		"""
		pass
WebezyMessage = _reflection.GeneratedProtocolMessageType('WebezyMessage', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _WEBEZYMESSAGE_EXTENSIONSENTRY,
    '__module__' : 'WebezyPackage_pb2'
    # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyMessage.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _WEBEZYMESSAGE,
  '__module__' : 'WebezyPackage_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyMessage)
  })
_sym_db.RegisterMessage(WebezyMessage)
_sym_db.RegisterMessage(WebezyMessage.ExtensionsEntry)


@overload
class WebezyPackage(_message.Message):
	"""webezyio generated message [webezy.WebezyPackage.v1.WebezyPackage]
	A class respresent a WebezyPackage type
	The webezy package descriptor
		"""
	uri = str # type: str
	name = str # type: str
	package = str # type: str
	version = str # type: str
	description = str # type: str
	type = str # type: str
	kind = str # type: str
	messages = List[WebezyMessage] # type: List[WebezyMessage]
	enums = List[WebezyEnum] # type: List[WebezyEnum]
	extensions = Dict[str,google_dot_protobuf_dot_struct__pb2.Value] # type: Dict[str,google_dot_protobuf_dot_struct__pb2.Value]
	dependencies = List[str] # type: List[str]

	def __init__(self, uri=str, name=str, package=str, version=str, description=str, type=str, kind=str, messages=List[WebezyMessage], enums=List[WebezyEnum], extensions=Dict[str,google_dot_protobuf_dot_struct__pb2.Value], dependencies=List[str]):
		"""
		Attributes:
		----------
		uri : str
			Package URI
		name : str
			Package name
		package : str
			The package unique full name
		version : str
			Package version
		description : str
			Package human readable description
		type : str
			Package type
		kind : str
			Pakcage king
		messages : List[WebezyMessage]
			The package messages array
		enums : List[WebezyEnum]
			The package enums array
		extensions : Dict[str,google_dot_protobuf_dot_struct__pb2.Value]
			The package pluggable extensions
		dependencies : List[str]
			
		"""
		pass
WebezyPackage = _reflection.GeneratedProtocolMessageType('WebezyPackage', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _WEBEZYPACKAGE_EXTENSIONSENTRY,
    '__module__' : 'WebezyPackage_pb2'
    # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyPackage.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _WEBEZYPACKAGE,
  '__module__' : 'WebezyPackage_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPackage.v1.WebezyPackage)
  })
_sym_db.RegisterMessage(WebezyPackage)
_sym_db.RegisterMessage(WebezyPackage.ExtensionsEntry)



if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _WEBEZYFIELD_EXTENSIONSENTRY._options = None
  _WEBEZYFIELD_EXTENSIONSENTRY._serialized_options = b'8\001'
  _WEBEZYMESSAGE_EXTENSIONSENTRY._options = None
  _WEBEZYMESSAGE_EXTENSIONSENTRY._serialized_options = b'8\001'
  _WEBEZYPACKAGE_EXTENSIONSENTRY._options = None
  _WEBEZYPACKAGE_EXTENSIONSENTRY._serialized_options = b'8\001'
  _WEBEZYONEOFFIELD_EXTENSIONSENTRY._options = None
  _WEBEZYONEOFFIELD_EXTENSIONSENTRY._serialized_options = b'8\001'
  _WEBEZYFIELDLABEL._serialized_start=2178
  _WEBEZYFIELDLABEL._serialized_end=2286
  _WEBEZYFIELDTYPE._serialized_start=2289
  _WEBEZYFIELDTYPE._serialized_end=2669
  _WEBEZYEXTENSION._serialized_start=2672
  _WEBEZYEXTENSION._serialized_end=2812
  _WEBEZYFIELD._serialized_start=79
  _WEBEZYFIELD._serialized_end=699
  _WEBEZYFIELD_EXTENSIONSENTRY._serialized_start=626
  _WEBEZYFIELD_EXTENSIONSENTRY._serialized_end=699
  _WEBEZYENUMVALUE._serialized_start=701
  _WEBEZYENUMVALUE._serialized_end=825
  _WEBEZYENUM._serialized_start=828
  _WEBEZYENUM._serialized_end=993
  _WEBEZYMESSAGE._serialized_start=996
  _WEBEZYMESSAGE._serialized_end=1377
  _WEBEZYMESSAGE_EXTENSIONSENTRY._serialized_start=626
  _WEBEZYMESSAGE_EXTENSIONSENTRY._serialized_end=699
  _WEBEZYPACKAGE._serialized_start=1380
  _WEBEZYPACKAGE._serialized_end=1788
  _WEBEZYPACKAGE_EXTENSIONSENTRY._serialized_start=626
  _WEBEZYPACKAGE_EXTENSIONSENTRY._serialized_end=699
  _WEBEZYONEOFFIELD._serialized_start=1791
  _WEBEZYONEOFFIELD._serialized_end=2176
  _WEBEZYONEOFFIELD_EXTENSIONSENTRY._serialized_start=626
  _WEBEZYONEOFFIELD_EXTENSIONSENTRY._serialized_end=699
# @@protoc_insertion_point(module_scope)
