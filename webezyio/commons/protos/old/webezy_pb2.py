# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: webezy.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from . import WebezyPrometheus_pb2 as WebezyPrometheus__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cwebezy.proto\x12\x0ewebezy.core.v1\x1a\x1cgoogle/protobuf/struct.proto\x1a\x16WebezyPrometheus.proto\"\x9b\x01\n\x0eWebezyTemplate\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08out_path\x18\x02 \x01(\t\x12\x0f\n\x07include\x18\x03 \x03(\t\x12\x0f\n\x07\x65xclude\x18\x04 \x03(\t\x12\x0c\n\x04tags\x18\x05 \x03(\t\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x07 \x01(\t\x12\x14\n\x0cinclude_code\x18\x08 \x01(\x08\"~\n\rWebezyMonitor\x12\x35\n\x07grafana\x18\x01 \x01(\x0b\x32$.webezy.core.v1.WebezyMonitorGrafana\x12\x36\n\nprometheus\x18\x02 \x01(\x0b\x32\".webezy.WebezyPrometheus.v1.Config\",\n\x14WebezyMonitorGrafana\x12\x14\n\x0cgrafana_path\x18\x01 \x01(\t\"\xe3\x01\n\x0bWebezyProxy\x12\x31\n\x05\x61\x64min\x18\x01 \x01(\x0b\x32\".webezy.core.v1.WebezyProxyAddress\x12\x33\n\x05stats\x18\x02 \x01(\x0b\x32$.webezy.core.v1.WebezyProxyStatsSink\x12\x36\n\tlisteners\x18\x03 \x03(\x0b\x32#.webezy.core.v1.WebezyProxyListener\x12\x34\n\x08\x63lusters\x18\x04 \x03(\x0b\x32\".webezy.core.v1.WebezyProxyCluster\"@\n\x14WebezyProxyStatsSink\x12\x18\n\x10tcp_cluster_name\x18\x01 \x01(\t\x12\x0e\n\x06prefix\x18\x02 \x01(\t\"X\n\x13WebezyProxyListener\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x33\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\".webezy.core.v1.WebezyProxyAddress\"3\n\x12WebezyProxyAddress\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"Z\n\x12WebezyProxyCluster\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x36\n\tendpoints\x18\x02 \x03(\x0b\x32#.webezy.core.v1.WebezyProxyEndpoint\"J\n\x13WebezyProxyEndpoint\x12\x33\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\".webezy.core.v1.WebezyProxyAddress\"\x99\x02\n\x0cWebezyConfig\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\x12\x38\n\ndeployment\x18\x03 \x01(\x0e\x32$.webezy.core.v1.WebezyDeploymentType\x12*\n\x05proxy\x18\x04 \x01(\x0b\x32\x1b.webezy.core.v1.WebezyProxy\x12%\n\x04\x64ocs\x18\x05 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x30\n\x08template\x18\x06 \x01(\x0b\x32\x1e.webezy.core.v1.WebezyTemplate\x12.\n\x07monitor\x18\x07 \x01(\x0b\x32\x1d.webezy.core.v1.WebezyMonitor\"\x94\x03\n\nWebezyJson\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12(\n\x07project\x18\x02 \x01(\x0b\x32\x17.webezy.core.v1.Project\x12:\n\x08services\x18\x03 \x03(\x0b\x32(.webezy.core.v1.WebezyJson.ServicesEntry\x12:\n\x08packages\x18\x04 \x03(\x0b\x32(.webezy.core.v1.WebezyJson.PackagesEntry\x12,\n\x06\x63onfig\x18\x05 \x01(\x0b\x32\x1c.webezy.core.v1.WebezyConfig\x1aR\n\rServicesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.webezy.core.v1.ServiceDescriptor:\x02\x38\x01\x1aR\n\rPackagesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.webezy.core.v1.PackageDescriptor:\x02\x38\x01\"\xda\x02\n\x0e\x46ileDescriptor\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07package\x18\x03 \x01(\t\x12\x0e\n\x06syntax\x18\x04 \x01(\t\x12L\n\x10services_by_name\x18\x05 \x03(\x0b\x32\x32.webezy.core.v1.FileDescriptor.ServicesByNameEntry\x12\x14\n\x07\x63ontent\x18\x06 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x0c\x64\x65pendencies\x18\x07 \x03(\t\x12,\n\x08messages\x18\x08 \x03(\x0b\x32\x1a.webezy.core.v1.Descriptor\x1aX\n\x13ServicesByNameEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.webezy.core.v1.ServiceDescriptor:\x02\x38\x01\x42\n\n\x08_content\":\n\x0cWebezyServer\x12*\n\x08language\x18\x02 \x01(\x0e\x32\x18.webezy.core.v1.Language\"K\n\x0cWebezyClient\x12\x0f\n\x07out_dir\x18\x01 \x01(\t\x12*\n\x08language\x18\x02 \x01(\x0e\x32\x18.webezy.core.v1.Language\"\xd7\x02\n\x07Project\x12\x0f\n\x02id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x0b\n\x03uri\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x14\n\x0cpackage_name\x18\x04 \x01(\t\x12\x0f\n\x07version\x18\x05 \x01(\t\x12\x0c\n\x04type\x18\x06 \x01(\t\x12\x0c\n\x04kind\x18\x07 \x01(\t\x12+\n\nproperties\x18\x08 \x03(\x0b\x32\x17.google.protobuf.Struct\x12\r\n\x05\x66iles\x18\t \x03(\t\x12\x10\n\x08services\x18\n \x03(\t\x12\x17\n\x0fserver_language\x18\x0b \x01(\t\x12,\n\x06server\x18\x0c \x01(\x0b\x32\x1c.webezy.core.v1.WebezyServer\x12-\n\x07\x63lients\x18\r \x03(\x0b\x32\x1c.webezy.core.v1.WebezyClient\x12\x12\n\ngo_package\x18\x0e \x01(\tB\x05\n\x03_id\"r\n\x11ProjectDescriptor\x12(\n\x07project\x18\x01 \x01(\x0b\x32\x17.webezy.core.v1.Project\x12\x33\n\x08services\x18\x02 \x03(\x0b\x32!.webezy.core.v1.ServiceDescriptor\"\x80\x01\n\x13\x45numValueDescriptor\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06number\x18\x03 \x01(\x05\x12\r\n\x05index\x18\x04 \x01(\x05\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x0c\n\x04kind\x18\x06 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\"\x9a\x01\n\x04\x45num\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x33\n\x06values\x18\x04 \x03(\x0b\x32#.webezy.core.v1.EnumValueDescriptor\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x0c\n\x04kind\x18\x06 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\"\xf6\x08\n\x0f\x46ieldDescriptor\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\r\n\x05index\x18\x04 \x01(\x05\x12\x38\n\nfield_type\x18\x05 \x01(\x0e\x32$.webezy.core.v1.FieldDescriptor.Type\x12\x34\n\x05label\x18\x06 \x01(\x0e\x32%.webezy.core.v1.FieldDescriptor.Label\x12\x16\n\tenum_type\x18\x07 \x01(\tH\x00\x88\x01\x01\x12\x0c\n\x04type\x18\x08 \x01(\t\x12\x0c\n\x04kind\x18\t \x01(\t\x12\x19\n\x0cmessage_type\x18\n \x01(\tH\x01\x88\x01\x01\x12\x43\n\nextensions\x18\x0b \x03(\x0b\x32/.webezy.core.v1.FieldDescriptor.ExtensionsEntry\x12\x18\n\x0b\x64\x65scription\x18\x0c \x01(\tH\x02\x88\x01\x01\x12;\n\x08key_type\x18\r \x01(\x0e\x32$.webezy.core.v1.FieldDescriptor.TypeH\x03\x88\x01\x01\x12=\n\nvalue_type\x18\x0e \x01(\x0e\x32$.webezy.core.v1.FieldDescriptor.TypeH\x04\x88\x01\x01\x12\x35\n\x0coneof_fields\x18\x0f \x03(\x0b\x32\x1f.webezy.core.v1.FieldDescriptor\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\"V\n\x05Label\x12\x11\n\rLABEL_UNKNOWN\x10\x00\x12\x12\n\x0eLABEL_OPTIONAL\x10\x01\x12\x12\n\x0eLABEL_REQUIRED\x10\x02\x12\x12\n\x0eLABEL_REPEATED\x10\x03\"\xe6\x02\n\x04Type\x12\x10\n\x0cTYPE_UNKNOWN\x10\x00\x12\x0f\n\x0bTYPE_DOUBLE\x10\x01\x12\x0e\n\nTYPE_FLOAT\x10\x02\x12\x0e\n\nTYPE_INT64\x10\x03\x12\x0f\n\x0bTYPE_UINT64\x10\x04\x12\x0e\n\nTYPE_INT32\x10\x05\x12\x10\n\x0cTYPE_FIXED64\x10\x06\x12\x10\n\x0cTYPE_FIXED32\x10\x07\x12\r\n\tTYPE_BOOL\x10\x08\x12\x0f\n\x0bTYPE_STRING\x10\t\x12\x0e\n\nTYPE_GROUP\x10\n\x12\x10\n\x0cTYPE_MESSAGE\x10\x0b\x12\x0e\n\nTYPE_BYTES\x10\x0c\x12\x0f\n\x0bTYPE_UINT32\x10\r\x12\r\n\tTYPE_ENUM\x10\x0e\x12\x11\n\rTYPE_SFIXED32\x10\x0f\x12\x11\n\rTYPE_SFIXED64\x10\x10\x12\x0f\n\x0bTYPE_SINT32\x10\x11\x12\x0f\n\x0bTYPE_SINT64\x10\x12\x12\x0c\n\x08TYPE_MAP\x10\x13\x12\x0e\n\nTYPE_ONEOF\x10\x14\x42\x0c\n\n_enum_typeB\x0f\n\r_message_typeB\x0e\n\x0c_descriptionB\x0b\n\t_key_typeB\r\n\x0b_value_type\"\xd8\x02\n\nDescriptor\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12/\n\x06\x66ields\x18\x04 \x03(\x0b\x32\x1f.webezy.core.v1.FieldDescriptor\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x0c\n\x04kind\x18\x06 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\x12>\n\nextensions\x18\x08 \x03(\x0b\x32*.webezy.core.v1.Descriptor.ExtensionsEntry\x12/\n\x0e\x65xtension_type\x18\t \x01(\x0e\x32\x17.webezy.core.v1.Options\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\"\x88\x03\n\x11ServiceDescriptor\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x31\n\x07methods\x18\x04 \x03(\x0b\x32 .webezy.core.v1.MethodDescriptor\x12\x13\n\x0b\x63lient_impl\x18\x05 \x01(\t\x12\x13\n\x0bserver_impl\x18\x06 \x01(\t\x12\x0f\n\x07version\x18\x07 \x01(\t\x12\x14\n\x0c\x64\x65pendencies\x18\x08 \x03(\t\x12\x13\n\x0b\x64\x65scription\x18\t \x01(\t\x12\x0c\n\x04type\x18\n \x01(\t\x12\x0c\n\x04kind\x18\x0b \x01(\t\x12\x45\n\nextensions\x18\x0c \x03(\x0b\x32\x31.webezy.core.v1.ServiceDescriptor.ExtensionsEntry\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\"\xfc\x02\n\x11PackageDescriptor\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07package\x18\x03 \x01(\t\x12,\n\x08messages\x18\x04 \x03(\x0b\x32\x1a.webezy.core.v1.Descriptor\x12\x0f\n\x07version\x18\x05 \x01(\t\x12\x14\n\x0c\x64\x65pendencies\x18\x06 \x03(\t\x12#\n\x05\x65nums\x18\x07 \x03(\x0b\x32\x14.webezy.core.v1.Enum\x12\x45\n\nextensions\x18\x08 \x03(\x0b\x32\x31.webezy.core.v1.PackageDescriptor.ExtensionsEntry\x12\x13\n\x0b\x64\x65scription\x18\t \x01(\t\x12\x0c\n\x04type\x18\n \x01(\t\x12\x0c\n\x04kind\x18\x0b \x01(\t\x1aI\n\x0f\x45xtensionsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.Value:\x02\x38\x01\"\xce\x01\n\x10MethodDescriptor\x12\x0b\n\x03uri\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x11\n\tfull_name\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x0c\n\x04kind\x18\x05 \x01(\t\x12\x12\n\ninput_type\x18\x06 \x01(\t\x12\x13\n\x0boutput_type\x18\x07 \x01(\t\x12\x18\n\x10\x63lient_streaming\x18\x08 \x01(\x08\x12\x18\n\x10server_streaming\x18\t \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\n \x01(\t\"A\n\rWebezyContext\x12\x30\n\x05\x66iles\x18\x01 \x03(\x0b\x32!.webezy.core.v1.WebezyFileContext\"e\n\x11WebezyFileContext\x12\x0c\n\x04\x66ile\x18\x01 \x01(\t\x12\x34\n\x07methods\x18\x02 \x03(\x0b\x32#.webezy.core.v1.WebezyMethodContext\x12\x0c\n\x04\x63ode\x18\x03 \x01(\x0c\"?\n\x13WebezyMethodContext\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0c\n\x04type\x18\x03 \x01(\t\"\xc0\x02\n\x11WzResourceWrapper\x12*\n\x07project\x18\x01 \x01(\x0b\x32\x17.webezy.core.v1.ProjectH\x00\x12\x34\n\x07service\x18\x02 \x01(\x0b\x32!.webezy.core.v1.ServiceDescriptorH\x00\x12\x34\n\x07package\x18\x03 \x01(\x0b\x32!.webezy.core.v1.PackageDescriptorH\x00\x12\x32\n\x06method\x18\x04 \x01(\x0b\x32 .webezy.core.v1.MethodDescriptorH\x00\x12-\n\x07message\x18\x05 \x01(\x0b\x32\x1a.webezy.core.v1.DescriptorH\x00\x12$\n\x04\x65num\x18\x06 \x01(\x0b\x32\x14.webezy.core.v1.EnumH\x00\x42\n\n\x08Resource*E\n\x14WebezyDeploymentType\x12\x16\n\x12UNKNOWN_DEPLOYMENT\x10\x00\x12\t\n\x05LOCAL\x10\x01\x12\n\n\x06\x44OCKER\x10\x02*D\n\x08Language\x12\x14\n\x10unknown_language\x10\x00\x12\n\n\x06python\x10\x01\x12\x0e\n\ntypescript\x10\x02\x12\x06\n\x02go\x10\x03*k\n\x07Options\x12\x15\n\x11UNKNOWN_EXTENSION\x10\x00\x12\x0f\n\x0b\x46ileOptions\x10\x01\x12\x12\n\x0eMessageOptions\x10\x02\x12\x10\n\x0c\x46ieldOptions\x10\x03\x12\x12\n\x0eServiceOptions\x10\x04\x62\x06proto3')

_WEBEZYDEPLOYMENTTYPE = DESCRIPTOR.enum_types_by_name['WebezyDeploymentType']
WebezyDeploymentType = enum_type_wrapper.EnumTypeWrapper(_WEBEZYDEPLOYMENTTYPE)
_LANGUAGE = DESCRIPTOR.enum_types_by_name['Language']
Language = enum_type_wrapper.EnumTypeWrapper(_LANGUAGE)
_OPTIONS = DESCRIPTOR.enum_types_by_name['Options']
Options = enum_type_wrapper.EnumTypeWrapper(_OPTIONS)
UNKNOWN_DEPLOYMENT = 0
LOCAL = 1
DOCKER = 2
unknown_language = 0
python = 1
typescript = 2
go = 3
UNKNOWN_EXTENSION = 0
FileOptions = 1
MessageOptions = 2
FieldOptions = 3
ServiceOptions = 4


_WEBEZYTEMPLATE = DESCRIPTOR.message_types_by_name['WebezyTemplate']
_WEBEZYMONITOR = DESCRIPTOR.message_types_by_name['WebezyMonitor']
_WEBEZYMONITORGRAFANA = DESCRIPTOR.message_types_by_name['WebezyMonitorGrafana']
_WEBEZYPROXY = DESCRIPTOR.message_types_by_name['WebezyProxy']
_WEBEZYPROXYSTATSSINK = DESCRIPTOR.message_types_by_name['WebezyProxyStatsSink']
_WEBEZYPROXYLISTENER = DESCRIPTOR.message_types_by_name['WebezyProxyListener']
_WEBEZYPROXYADDRESS = DESCRIPTOR.message_types_by_name['WebezyProxyAddress']
_WEBEZYPROXYCLUSTER = DESCRIPTOR.message_types_by_name['WebezyProxyCluster']
_WEBEZYPROXYENDPOINT = DESCRIPTOR.message_types_by_name['WebezyProxyEndpoint']
_WEBEZYCONFIG = DESCRIPTOR.message_types_by_name['WebezyConfig']
_WEBEZYJSON = DESCRIPTOR.message_types_by_name['WebezyJson']
_WEBEZYJSON_SERVICESENTRY = _WEBEZYJSON.nested_types_by_name['ServicesEntry']
_WEBEZYJSON_PACKAGESENTRY = _WEBEZYJSON.nested_types_by_name['PackagesEntry']
_FILEDESCRIPTOR = DESCRIPTOR.message_types_by_name['FileDescriptor']
_FILEDESCRIPTOR_SERVICESBYNAMEENTRY = _FILEDESCRIPTOR.nested_types_by_name['ServicesByNameEntry']
_WEBEZYSERVER = DESCRIPTOR.message_types_by_name['WebezyServer']
_WEBEZYCLIENT = DESCRIPTOR.message_types_by_name['WebezyClient']
_PROJECT = DESCRIPTOR.message_types_by_name['Project']
_PROJECTDESCRIPTOR = DESCRIPTOR.message_types_by_name['ProjectDescriptor']
_ENUMVALUEDESCRIPTOR = DESCRIPTOR.message_types_by_name['EnumValueDescriptor']
_ENUM = DESCRIPTOR.message_types_by_name['Enum']
_FIELDDESCRIPTOR = DESCRIPTOR.message_types_by_name['FieldDescriptor']
_FIELDDESCRIPTOR_EXTENSIONSENTRY = _FIELDDESCRIPTOR.nested_types_by_name['ExtensionsEntry']
_DESCRIPTOR = DESCRIPTOR.message_types_by_name['Descriptor']
_DESCRIPTOR_EXTENSIONSENTRY = _DESCRIPTOR.nested_types_by_name['ExtensionsEntry']
_SERVICEDESCRIPTOR = DESCRIPTOR.message_types_by_name['ServiceDescriptor']
_SERVICEDESCRIPTOR_EXTENSIONSENTRY = _SERVICEDESCRIPTOR.nested_types_by_name['ExtensionsEntry']
_PACKAGEDESCRIPTOR = DESCRIPTOR.message_types_by_name['PackageDescriptor']
_PACKAGEDESCRIPTOR_EXTENSIONSENTRY = _PACKAGEDESCRIPTOR.nested_types_by_name['ExtensionsEntry']
_METHODDESCRIPTOR = DESCRIPTOR.message_types_by_name['MethodDescriptor']
_WEBEZYCONTEXT = DESCRIPTOR.message_types_by_name['WebezyContext']
_WEBEZYFILECONTEXT = DESCRIPTOR.message_types_by_name['WebezyFileContext']
_WEBEZYMETHODCONTEXT = DESCRIPTOR.message_types_by_name['WebezyMethodContext']
_WZRESOURCEWRAPPER = DESCRIPTOR.message_types_by_name['WzResourceWrapper']
_FIELDDESCRIPTOR_LABEL = _FIELDDESCRIPTOR.enum_types_by_name['Label']
_FIELDDESCRIPTOR_TYPE = _FIELDDESCRIPTOR.enum_types_by_name['Type']
WebezyTemplate = _reflection.GeneratedProtocolMessageType('WebezyTemplate', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYTEMPLATE,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyTemplate)
  })
_sym_db.RegisterMessage(WebezyTemplate)

WebezyMonitor = _reflection.GeneratedProtocolMessageType('WebezyMonitor', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYMONITOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyMonitor)
  })
_sym_db.RegisterMessage(WebezyMonitor)

WebezyMonitorGrafana = _reflection.GeneratedProtocolMessageType('WebezyMonitorGrafana', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYMONITORGRAFANA,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyMonitorGrafana)
  })
_sym_db.RegisterMessage(WebezyMonitorGrafana)

WebezyProxy = _reflection.GeneratedProtocolMessageType('WebezyProxy', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYPROXY,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyProxy)
  })
_sym_db.RegisterMessage(WebezyProxy)

WebezyProxyStatsSink = _reflection.GeneratedProtocolMessageType('WebezyProxyStatsSink', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYPROXYSTATSSINK,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyProxyStatsSink)
  })
_sym_db.RegisterMessage(WebezyProxyStatsSink)

WebezyProxyListener = _reflection.GeneratedProtocolMessageType('WebezyProxyListener', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYPROXYLISTENER,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyProxyListener)
  })
_sym_db.RegisterMessage(WebezyProxyListener)

WebezyProxyAddress = _reflection.GeneratedProtocolMessageType('WebezyProxyAddress', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYPROXYADDRESS,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyProxyAddress)
  })
_sym_db.RegisterMessage(WebezyProxyAddress)

WebezyProxyCluster = _reflection.GeneratedProtocolMessageType('WebezyProxyCluster', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYPROXYCLUSTER,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyProxyCluster)
  })
_sym_db.RegisterMessage(WebezyProxyCluster)

WebezyProxyEndpoint = _reflection.GeneratedProtocolMessageType('WebezyProxyEndpoint', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYPROXYENDPOINT,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyProxyEndpoint)
  })
_sym_db.RegisterMessage(WebezyProxyEndpoint)

WebezyConfig = _reflection.GeneratedProtocolMessageType('WebezyConfig', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYCONFIG,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyConfig)
  })
_sym_db.RegisterMessage(WebezyConfig)

WebezyJson = _reflection.GeneratedProtocolMessageType('WebezyJson', (_message.Message,), {

  'ServicesEntry' : _reflection.GeneratedProtocolMessageType('ServicesEntry', (_message.Message,), {
    'DESCRIPTOR' : _WEBEZYJSON_SERVICESENTRY,
    '__module__' : 'webezy_pb2'
    # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyJson.ServicesEntry)
    })
  ,

  'PackagesEntry' : _reflection.GeneratedProtocolMessageType('PackagesEntry', (_message.Message,), {
    'DESCRIPTOR' : _WEBEZYJSON_PACKAGESENTRY,
    '__module__' : 'webezy_pb2'
    # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyJson.PackagesEntry)
    })
  ,
  'DESCRIPTOR' : _WEBEZYJSON,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyJson)
  })
_sym_db.RegisterMessage(WebezyJson)
_sym_db.RegisterMessage(WebezyJson.ServicesEntry)
_sym_db.RegisterMessage(WebezyJson.PackagesEntry)

FileDescriptor = _reflection.GeneratedProtocolMessageType('FileDescriptor', (_message.Message,), {

  'ServicesByNameEntry' : _reflection.GeneratedProtocolMessageType('ServicesByNameEntry', (_message.Message,), {
    'DESCRIPTOR' : _FILEDESCRIPTOR_SERVICESBYNAMEENTRY,
    '__module__' : 'webezy_pb2'
    # @@protoc_insertion_point(class_scope:webezy.core.v1.FileDescriptor.ServicesByNameEntry)
    })
  ,
  'DESCRIPTOR' : _FILEDESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.FileDescriptor)
  })
_sym_db.RegisterMessage(FileDescriptor)
_sym_db.RegisterMessage(FileDescriptor.ServicesByNameEntry)

WebezyServer = _reflection.GeneratedProtocolMessageType('WebezyServer', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYSERVER,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyServer)
  })
_sym_db.RegisterMessage(WebezyServer)

WebezyClient = _reflection.GeneratedProtocolMessageType('WebezyClient', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYCLIENT,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyClient)
  })
_sym_db.RegisterMessage(WebezyClient)

Project = _reflection.GeneratedProtocolMessageType('Project', (_message.Message,), {
  'DESCRIPTOR' : _PROJECT,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.Project)
  })
_sym_db.RegisterMessage(Project)

ProjectDescriptor = _reflection.GeneratedProtocolMessageType('ProjectDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _PROJECTDESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.ProjectDescriptor)
  })
_sym_db.RegisterMessage(ProjectDescriptor)

EnumValueDescriptor = _reflection.GeneratedProtocolMessageType('EnumValueDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _ENUMVALUEDESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.EnumValueDescriptor)
  })
_sym_db.RegisterMessage(EnumValueDescriptor)

Enum = _reflection.GeneratedProtocolMessageType('Enum', (_message.Message,), {
  'DESCRIPTOR' : _ENUM,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.Enum)
  })
_sym_db.RegisterMessage(Enum)

FieldDescriptor = _reflection.GeneratedProtocolMessageType('FieldDescriptor', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _FIELDDESCRIPTOR_EXTENSIONSENTRY,
    '__module__' : 'webezy_pb2'
    # @@protoc_insertion_point(class_scope:webezy.core.v1.FieldDescriptor.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _FIELDDESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.FieldDescriptor)
  })
_sym_db.RegisterMessage(FieldDescriptor)
_sym_db.RegisterMessage(FieldDescriptor.ExtensionsEntry)

Descriptor = _reflection.GeneratedProtocolMessageType('Descriptor', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _DESCRIPTOR_EXTENSIONSENTRY,
    '__module__' : 'webezy_pb2'
    # @@protoc_insertion_point(class_scope:webezy.core.v1.Descriptor.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _DESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.Descriptor)
  })
_sym_db.RegisterMessage(Descriptor)
_sym_db.RegisterMessage(Descriptor.ExtensionsEntry)

ServiceDescriptor = _reflection.GeneratedProtocolMessageType('ServiceDescriptor', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _SERVICEDESCRIPTOR_EXTENSIONSENTRY,
    '__module__' : 'webezy_pb2'
    # @@protoc_insertion_point(class_scope:webezy.core.v1.ServiceDescriptor.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _SERVICEDESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.ServiceDescriptor)
  })
_sym_db.RegisterMessage(ServiceDescriptor)
_sym_db.RegisterMessage(ServiceDescriptor.ExtensionsEntry)

PackageDescriptor = _reflection.GeneratedProtocolMessageType('PackageDescriptor', (_message.Message,), {

  'ExtensionsEntry' : _reflection.GeneratedProtocolMessageType('ExtensionsEntry', (_message.Message,), {
    'DESCRIPTOR' : _PACKAGEDESCRIPTOR_EXTENSIONSENTRY,
    '__module__' : 'webezy_pb2'
    # @@protoc_insertion_point(class_scope:webezy.core.v1.PackageDescriptor.ExtensionsEntry)
    })
  ,
  'DESCRIPTOR' : _PACKAGEDESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.PackageDescriptor)
  })
_sym_db.RegisterMessage(PackageDescriptor)
_sym_db.RegisterMessage(PackageDescriptor.ExtensionsEntry)

MethodDescriptor = _reflection.GeneratedProtocolMessageType('MethodDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _METHODDESCRIPTOR,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.MethodDescriptor)
  })
_sym_db.RegisterMessage(MethodDescriptor)

WebezyContext = _reflection.GeneratedProtocolMessageType('WebezyContext', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYCONTEXT,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyContext)
  })
_sym_db.RegisterMessage(WebezyContext)

WebezyFileContext = _reflection.GeneratedProtocolMessageType('WebezyFileContext', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYFILECONTEXT,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyFileContext)
  })
_sym_db.RegisterMessage(WebezyFileContext)

WebezyMethodContext = _reflection.GeneratedProtocolMessageType('WebezyMethodContext', (_message.Message,), {
  'DESCRIPTOR' : _WEBEZYMETHODCONTEXT,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WebezyMethodContext)
  })
_sym_db.RegisterMessage(WebezyMethodContext)

WzResourceWrapper = _reflection.GeneratedProtocolMessageType('WzResourceWrapper', (_message.Message,), {
  'DESCRIPTOR' : _WZRESOURCEWRAPPER,
  '__module__' : 'webezy_pb2'
  # @@protoc_insertion_point(class_scope:webezy.core.v1.WzResourceWrapper)
  })
_sym_db.RegisterMessage(WzResourceWrapper)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _WEBEZYJSON_SERVICESENTRY._options = None
  _WEBEZYJSON_SERVICESENTRY._serialized_options = b'8\001'
  _WEBEZYJSON_PACKAGESENTRY._options = None
  _WEBEZYJSON_PACKAGESENTRY._serialized_options = b'8\001'
  _FILEDESCRIPTOR_SERVICESBYNAMEENTRY._options = None
  _FILEDESCRIPTOR_SERVICESBYNAMEENTRY._serialized_options = b'8\001'
  _FIELDDESCRIPTOR_EXTENSIONSENTRY._options = None
  _FIELDDESCRIPTOR_EXTENSIONSENTRY._serialized_options = b'8\001'
  _DESCRIPTOR_EXTENSIONSENTRY._options = None
  _DESCRIPTOR_EXTENSIONSENTRY._serialized_options = b'8\001'
  _SERVICEDESCRIPTOR_EXTENSIONSENTRY._options = None
  _SERVICEDESCRIPTOR_EXTENSIONSENTRY._serialized_options = b'8\001'
  _PACKAGEDESCRIPTOR_EXTENSIONSENTRY._options = None
  _PACKAGEDESCRIPTOR_EXTENSIONSENTRY._serialized_options = b'8\001'
  _WEBEZYDEPLOYMENTTYPE._serialized_start=5989
  _WEBEZYDEPLOYMENTTYPE._serialized_end=6058
  _LANGUAGE._serialized_start=6060
  _LANGUAGE._serialized_end=6128
  _OPTIONS._serialized_start=6130
  _OPTIONS._serialized_end=6237
  _WEBEZYTEMPLATE._serialized_start=87
  _WEBEZYTEMPLATE._serialized_end=242
  _WEBEZYMONITOR._serialized_start=244
  _WEBEZYMONITOR._serialized_end=370
  _WEBEZYMONITORGRAFANA._serialized_start=372
  _WEBEZYMONITORGRAFANA._serialized_end=416
  _WEBEZYPROXY._serialized_start=419
  _WEBEZYPROXY._serialized_end=646
  _WEBEZYPROXYSTATSSINK._serialized_start=648
  _WEBEZYPROXYSTATSSINK._serialized_end=712
  _WEBEZYPROXYLISTENER._serialized_start=714
  _WEBEZYPROXYLISTENER._serialized_end=802
  _WEBEZYPROXYADDRESS._serialized_start=804
  _WEBEZYPROXYADDRESS._serialized_end=855
  _WEBEZYPROXYCLUSTER._serialized_start=857
  _WEBEZYPROXYCLUSTER._serialized_end=947
  _WEBEZYPROXYENDPOINT._serialized_start=949
  _WEBEZYPROXYENDPOINT._serialized_end=1023
  _WEBEZYCONFIG._serialized_start=1026
  _WEBEZYCONFIG._serialized_end=1307
  _WEBEZYJSON._serialized_start=1310
  _WEBEZYJSON._serialized_end=1714
  _WEBEZYJSON_SERVICESENTRY._serialized_start=1548
  _WEBEZYJSON_SERVICESENTRY._serialized_end=1630
  _WEBEZYJSON_PACKAGESENTRY._serialized_start=1632
  _WEBEZYJSON_PACKAGESENTRY._serialized_end=1714
  _FILEDESCRIPTOR._serialized_start=1717
  _FILEDESCRIPTOR._serialized_end=2063
  _FILEDESCRIPTOR_SERVICESBYNAMEENTRY._serialized_start=1963
  _FILEDESCRIPTOR_SERVICESBYNAMEENTRY._serialized_end=2051
  _WEBEZYSERVER._serialized_start=2065
  _WEBEZYSERVER._serialized_end=2123
  _WEBEZYCLIENT._serialized_start=2125
  _WEBEZYCLIENT._serialized_end=2200
  _PROJECT._serialized_start=2203
  _PROJECT._serialized_end=2546
  _PROJECTDESCRIPTOR._serialized_start=2548
  _PROJECTDESCRIPTOR._serialized_end=2662
  _ENUMVALUEDESCRIPTOR._serialized_start=2665
  _ENUMVALUEDESCRIPTOR._serialized_end=2793
  _ENUM._serialized_start=2796
  _ENUM._serialized_end=2950
  _FIELDDESCRIPTOR._serialized_start=2953
  _FIELDDESCRIPTOR._serialized_end=4095
  _FIELDDESCRIPTOR_EXTENSIONSENTRY._serialized_start=3498
  _FIELDDESCRIPTOR_EXTENSIONSENTRY._serialized_end=3571
  _FIELDDESCRIPTOR_LABEL._serialized_start=3573
  _FIELDDESCRIPTOR_LABEL._serialized_end=3659
  _FIELDDESCRIPTOR_TYPE._serialized_start=3662
  _FIELDDESCRIPTOR_TYPE._serialized_end=4020
  _DESCRIPTOR._serialized_start=4098
  _DESCRIPTOR._serialized_end=4442
  _DESCRIPTOR_EXTENSIONSENTRY._serialized_start=3498
  _DESCRIPTOR_EXTENSIONSENTRY._serialized_end=3571
  _SERVICEDESCRIPTOR._serialized_start=4445
  _SERVICEDESCRIPTOR._serialized_end=4837
  _SERVICEDESCRIPTOR_EXTENSIONSENTRY._serialized_start=3498
  _SERVICEDESCRIPTOR_EXTENSIONSENTRY._serialized_end=3571
  _PACKAGEDESCRIPTOR._serialized_start=4840
  _PACKAGEDESCRIPTOR._serialized_end=5220
  _PACKAGEDESCRIPTOR_EXTENSIONSENTRY._serialized_start=3498
  _PACKAGEDESCRIPTOR_EXTENSIONSENTRY._serialized_end=3571
  _METHODDESCRIPTOR._serialized_start=5223
  _METHODDESCRIPTOR._serialized_end=5429
  _WEBEZYCONTEXT._serialized_start=5431
  _WEBEZYCONTEXT._serialized_end=5496
  _WEBEZYFILECONTEXT._serialized_start=5498
  _WEBEZYFILECONTEXT._serialized_end=5599
  _WEBEZYMETHODCONTEXT._serialized_start=5601
  _WEBEZYMETHODCONTEXT._serialized_end=5664
  _WZRESOURCEWRAPPER._serialized_start=5667
  _WZRESOURCEWRAPPER._serialized_end=5987
# @@protoc_insertion_point(module_scope)
