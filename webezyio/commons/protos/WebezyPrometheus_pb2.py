# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: WebezyPrometheus.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor

from typing import overload, Iterator, List, Dict
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16WebezyPrometheus.proto\x12\x1awebezy.WebezyPrometheus.v1\"\'\n\x0cGlobalConfig\x12\x17\n\x0fscrape_interval\x18\x01 \x01(\x05\"8\n\x11StaticConfigLabel\x12\x14\n\x0cservice_name\x18\x01 \x01(\t\x12\r\n\x05group\x18\x02 \x01(\t\"^\n\x0cStaticConfig\x12\x0f\n\x07targets\x18\x01 \x03(\t\x12=\n\x06labels\x18\x02 \x03(\x0b\x32-.webezy.WebezyPrometheus.v1.StaticConfigLabel\"{\n\x0cScrapeConfig\x12\x10\n\x08job_name\x18\x01 \x01(\t\x12\x17\n\x0fscrape_interval\x18\x02 \x01(\x05\x12@\n\x0estatic_configs\x18\x03 \x03(\x0b\x32(.webezy.WebezyPrometheus.v1.StaticConfig\"\x8b\x01\n\x06\x43onfig\x12?\n\rglobal_config\x18\x01 \x01(\x0b\x32(.webezy.WebezyPrometheus.v1.GlobalConfig\x12@\n\x0escrape_configs\x18\x02 \x03(\x0b\x32(.webezy.WebezyPrometheus.v1.ScrapeConfigb\x06proto3')



_GLOBALCONFIG = DESCRIPTOR.message_types_by_name['GlobalConfig']
_STATICCONFIGLABEL = DESCRIPTOR.message_types_by_name['StaticConfigLabel']
_STATICCONFIG = DESCRIPTOR.message_types_by_name['StaticConfig']
_SCRAPECONFIG = DESCRIPTOR.message_types_by_name['ScrapeConfig']
_CONFIG = DESCRIPTOR.message_types_by_name['Config']

@overload
class GlobalConfig:
	"""webezyio generated message [webezy.WebezyPrometheus.v1.GlobalConfig]
	A class respresent a GlobalConfig type
	"""
	scrape_interval = int # type: int

	def __init__(self, scrape_interval=int):
		pass
GlobalConfig = _reflection.GeneratedProtocolMessageType('GlobalConfig', (_message.Message,), {
  'DESCRIPTOR' : _GLOBALCONFIG,
  '__module__' : 'WebezyPrometheus_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPrometheus.v1.GlobalConfig)
  })
_sym_db.RegisterMessage(GlobalConfig)


@overload
class StaticConfigLabel:
	"""webezyio generated message [webezy.WebezyPrometheus.v1.StaticConfigLabel]
	A class respresent a StaticConfigLabel type
	"""
	service_name = str # type: str
	group = str # type: str

	def __init__(self, service_name=str, group=str):
		pass
StaticConfigLabel = _reflection.GeneratedProtocolMessageType('StaticConfigLabel', (_message.Message,), {
  'DESCRIPTOR' : _STATICCONFIGLABEL,
  '__module__' : 'WebezyPrometheus_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPrometheus.v1.StaticConfigLabel)
  })
_sym_db.RegisterMessage(StaticConfigLabel)


@overload
class StaticConfig:
	"""webezyio generated message [webezy.WebezyPrometheus.v1.StaticConfig]
	A class respresent a StaticConfig type
	"""
	targets = List[str] # type: List[str]
	labels = List[StaticConfigLabel] # type: List[StaticConfigLabel]

	def __init__(self, targets=List[str], labels=List[StaticConfigLabel]):
		pass
StaticConfig = _reflection.GeneratedProtocolMessageType('StaticConfig', (_message.Message,), {
  'DESCRIPTOR' : _STATICCONFIG,
  '__module__' : 'WebezyPrometheus_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPrometheus.v1.StaticConfig)
  })
_sym_db.RegisterMessage(StaticConfig)


@overload
class ScrapeConfig:
	"""webezyio generated message [webezy.WebezyPrometheus.v1.ScrapeConfig]
	A class respresent a ScrapeConfig type
	"""
	job_name = str # type: str
	scrape_interval = int # type: int
	static_configs = List[StaticConfig] # type: List[StaticConfig]

	def __init__(self, job_name=str, scrape_interval=int, static_configs=List[StaticConfig]):
		pass
ScrapeConfig = _reflection.GeneratedProtocolMessageType('ScrapeConfig', (_message.Message,), {
  'DESCRIPTOR' : _SCRAPECONFIG,
  '__module__' : 'WebezyPrometheus_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPrometheus.v1.ScrapeConfig)
  })
_sym_db.RegisterMessage(ScrapeConfig)


@overload
class Config:
	"""webezyio generated message [webezy.WebezyPrometheus.v1.Config]
	A class respresent a Config type
	"""
	global_config = GlobalConfig # type: GlobalConfig
	scrape_configs = List[ScrapeConfig] # type: List[ScrapeConfig]

	def __init__(self, global_config=GlobalConfig, scrape_configs=List[ScrapeConfig]):
		pass
Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'WebezyPrometheus_pb2'
  # @@protoc_insertion_point(class_scope:webezy.WebezyPrometheus.v1.Config)
  })
_sym_db.RegisterMessage(Config)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GLOBALCONFIG._serialized_start=54
  _GLOBALCONFIG._serialized_end=93
  _STATICCONFIGLABEL._serialized_start=95
  _STATICCONFIGLABEL._serialized_end=151
  _STATICCONFIG._serialized_start=153
  _STATICCONFIG._serialized_end=247
  _SCRAPECONFIG._serialized_start=249
  _SCRAPECONFIG._serialized_end=372
  _CONFIG._serialized_start=375
  _CONFIG._serialized_end=514
# @@protoc_insertion_point(module_scope)
