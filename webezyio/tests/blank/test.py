from pprint import pprint
from webezyio import WebezyArchitect, _helpers, _resources
from webezyio import WebezyBuilder, WebezyPy, WebezyTs, WebezyProto, WebezyBase
from webezyio.commons.protos.webezy_pb2 import Language

"""
Webezy Builder - Programaticlly build Webezy.io projects

Architect correct workflow:
-------------------------
* Init
   ||
   |- Architect
   |- Project
   ||
   \/
* Configs
   ||
   |- Domain
   |- Config
   |- Plugins
   ||
   \/
* Packages
   ||
   |- Messages
   |- Enums
   |- Extensions
   ||
   \/
* Services
   ||
   |- RPC's
   ||
   \/
* Save

Builder correct workflow:
-------------------------

* Init
   ||
   |- Builder
   |- Builder.InitProjectStructure
   |- Builder.RebuildContext
   ||
   \/
* Write files
   ||
   |- Builder.BuildProtos
   |- Builder.BuildServices
   |- Builder.BuildServer
   |- Builder.CompileProtos
   |- Builder.WriteReadme
   |- Builder.OverrideGeneratedClasses
   |- Builder.BuildClients
   ||
   \/
* Done
"""

"""Architect pre config"""

# Config values
_DOMAIN = "domain"
# The project path for webezy.json should be the root dir for project
_PATH = "/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/blank/webezy.json"
# The project name
_PROJECT_NAME = "TEST-PROJECT"
# The project server langugae (only 1 server per project - all services impl. should be in same langugae)
_SERVER_LANGUAGE = Language.python
# The project server host and port
_HOST = 'localhost'
_PORT = 50051

"""Messages And Enums"""
# Enums value array
_ENUMS_VALUES = [_helpers.WZEnumValue(
    "UNKNWON", 0), _helpers.WZEnumValue("TEST", 1)]
# [Enum] SampleEnum
SampleEnum = _helpers.WZEnum('SampleEnum', enum_values=_ENUMS_VALUES)

# [Field] BoolExtend
BoolExtend = _helpers.WZField('BoolExtend', type='TYPE_BOOL', label='LABEL_REPEATED',
                              description='This field extending FieldOptions message')
# [Message] ExtensionMessage
ExtensionMessage = _helpers.WZMessage(name='ExtensionMessage',
                                      fields=[BoolExtend],
                                      extension_type=_resources.Options.FieldOptions)

# [Field] ExtendedField
ExtendedField = _helpers.WZField('ExtendedField',
                                 type='TYPE_BOOL',
                                 label='LABEL_OPTIONAL',
                                 extensions={f'{ExtensionMessage.name}.{BoolExtend.name}': True})
# [Field] Timestamp
Timestamp = _helpers.WZField('Timestamp',
                             type='TYPE_MESSAGE',
                             label='LABEL_OPTIONAL',
                             message_type='google.protobuf.Timestamp')
# [Field] Integer
Integer = _helpers.WZField('Integer',
                           type='TYPE_INT32',
                           label='LABEL_OPTIONAL')
# [Field] ChildMessage
ChildMessage = _helpers.WZField('ChildMessage',
                                type='TYPE_MESSAGE',
                                label='LABEL_OPTIONAL',
                                message_type=_resources.construct_full_name(
                                     _resources.ResourceTypes.descriptor,
                                     _resources.ResourceKinds.message,
                                     _DOMAIN,
                                     parent_name='OtherPackage',
                                     name='OtherMessage'))
# [Message] SampleMessage
SampleMessage = _helpers.WZMessage(name='SampleMessage',
                                   fields=[ExtendedField, Timestamp,
                                           Integer, ChildMessage],
                                   description='Some description in sample message')


# [Field] StringField
StringField = _helpers.WZField('StringField',
                               type='TYPE_STRING',
                               label='LABEL_OPTIONAL')
# [Message] OtherMessage
OtherMessage = _helpers.WZMessage(name='OtherMessage',
                                  fields=[StringField],
                                  description='Some description in other message')

"""Packages"""

# Declaring packages, RPC's and services
# [Package] SamplePackage
SamplePackage = _helpers.WZPackage('SamplePackage',
                                   messages=[SampleMessage, ExtensionMessage],
                                   enums=[SampleEnum])
# [Package] OtherPackage
OtherPackage = _helpers.WZPackage('OtherPackage',
                                  messages=[OtherMessage],
                                  enums=[])

"""RPC's"""

# [RPC] SampleRPC
SampleRPC = _helpers.WZRPC(name='SampleRPC',
                           client_stream=False,
                           server_stream=False,
                           in_type=f'{_DOMAIN}.{SamplePackage.name}.v1.{SampleMessage.name}',
                           out_type=f'{_DOMAIN}.{SamplePackage.name}.v1.{SampleMessage.name}',
                           description='SampleRPC - Some description for RPC')
# [RPC] TestRPC
TestRPC = _helpers.WZRPC(name='TestRPC',
                         client_stream=True,
                         server_stream=False,
                         in_type=f'{_DOMAIN}.{OtherPackage.name}.v1.{OtherMessage.name}',
                         out_type=f'{_DOMAIN}.{OtherPackage.name}.v1.{OtherMessage.name}',
                         description='TestRPC - Some description for RPC')
# [RPC] OtherRPC
OtherRPC = _helpers.WZRPC(name='OtherRPC',
                          client_stream=True,
                          server_stream=False,
                          in_type=f'{_DOMAIN}.{OtherPackage.name}.v1.{OtherMessage.name}',
                          out_type=f'{_DOMAIN}.{SamplePackage.name}.v1.{SampleMessage.name}',
                          description='OtherRPC - Some description for RPC')

"""Services"""

SampleService = _helpers.WZService('SampleService', methods=[SampleRPC, TestRPC, OtherRPC], dependencies=[
                                   f'{_DOMAIN}.SamplePackage.v1'], description='Some description for SampleService')


def main():
    """Architect flow start"""

    # Init Builder
    ARCHITECT = WebezyArchitect(
        path=_PATH, domain=_DOMAIN, project_name=_PROJECT_NAME)
    # Init Project
    ARCHITECT.AddProject(server_language=Language.Name(_SERVER_LANGUAGE), clients=[])

    # Configs
    ARCHITECT.SetConfig({'host': _HOST, 'port': _PORT})

    # SamplePackage
    name, messages, enums = SamplePackage.to_tuple()

    SAMPLEPACKAGE = ARCHITECT.AddPackage(name, [])
    for msg in messages:
        msg_name, fields, description, options = msg
        ARCHITECT.AddMessage(SAMPLEPACKAGE, msg_name,
                             fields, description, options)

    for enum in enums:
        enum_name, enum_values = enum
        ARCHITECT.AddEnum(SAMPLEPACKAGE, enum_name, enum_values)

    # OtherPackage
    name, messages, enums = OtherPackage.to_tuple()

    OTHERPACKAGE = ARCHITECT.AddPackage(name, [])
    for msg in messages:
        msg_name, fields, description, options = msg
        ARCHITECT.AddMessage(OTHERPACKAGE, msg_name,
                             fields, description, options)

    for enum in enums:
        enum_name, enum_values = enum
        ARCHITECT.AddEnum(OTHERPACKAGE, enum_name, enum_values)

    # SampleService
    service_name, methods, dependencies, description = SampleService.to_tuple()

    SAMPLESERVICE = ARCHITECT.AddService(
        service_name, dependencies, description)
    for rpc in methods:
        rpc_name, in_out, description = rpc
        ARCHITECT.AddRPC(SAMPLESERVICE, rpc_name, in_out, description)

    ARCHITECT.Save()

    """Builder workflow"""

    # Init builder class with webezy.json file
    wzBuilder = WebezyBuilder(path=_PATH)
    # Prebuild hook
    prebuild = wzBuilder.PreBuild()
    # Init project structure hook
    init = wzBuilder.InitProjectStructure()
    # Webezy Context hook
    context = wzBuilder.RebuildContext()
    # Protos file hook
    protos = wzBuilder.BuildProtos()
    # Services impl code hook
    services = wzBuilder.BuildServices()
    # Server code hook
    server = wzBuilder.BuildServer()
    # Compile protos hook (protoc)
    compile = wzBuilder.CompileProtos()
    # Readme hook
    readme = wzBuilder.WriteReadme()
    # Override default proto generated class hook (python only)
    protoclass = wzBuilder.OverrideGeneratedClasses()
    # clients writing hook
    clients = wzBuilder.BuildClients()
    # Postbuild hook
    postbuild = wzBuilder.PostBuild()

    print("Build process done")
    # Or all at once
    # build = wzBuilder.BuildAll()


if __name__ == "__main__":
    main()