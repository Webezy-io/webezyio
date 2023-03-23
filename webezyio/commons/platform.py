from asyncio.log import logger
from typing import Tuple,Iterator
import grpc
from webezyio.commons.config import parse_project_config
from webezyio.commons.pretty import print_error, print_info
from webezyio.commons.protos.Platform_pb2_grpc import PlatformStub
from webezyio.commons.protos.Services_pb2_grpc import ServicesStub
from webezyio.commons.protos.Methods_pb2_grpc import MethodsStub
from webezyio.commons.protos.Packages_pb2_grpc import PackagesStub
from webezyio.commons.protos.Messages_pb2_grpc import MessagesStub
from webezyio.commons.protos.Fields_pb2_grpc import FieldsStub
from webezyio.commons.protos.Enums_pb2_grpc import EnumsStub
from webezyio.commons.protos.EnumValues_pb2_grpc import EnumValuesStub
from webezyio.commons.protos.WebezyApi_pb2 import GetOrganizationRequest, GetProjectRequest, ListPackagesRequest, ListServicesRequest
from webezyio.commons.protos.WebezyJson_pb2 import WebezyJson

_CHANNEL_OPTIONS = (("grpc.keepalive_permit_without_calls", 1),
	("grpc.keepalive_time_ms", 120000),
	("grpc.keepalive_timeout_ms", 20000),
	("grpc.http2.min_time_between_pings_ms", 120000),
	("grpc.http2.max_pings_without_data", 1),)
class WebezyPlatform:

    def __init__(self, path, host="webezy-core-dev.francecentral.cloudapp.azure.com", port=80, timeout=10):
        
        configs = parse_project_config(path)
        token = configs.get('token')

        if 'webezyio-test' not in token:
            print(token)
            print_error('Token is not valid !')
            exit(1)

        channel = grpc.insecure_channel('{0}:{1}'.format(host, port),_CHANNEL_OPTIONS)
        
        try:
            grpc.channel_ready_future(channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            logger.debug("Error connecting to webezy-platform server")

        self.Services = ServicesStub(channel)
        self.Methods = MethodsStub(channel)
        self.Packages = PackagesStub(channel)
        self.Messages = MessagesStub(channel)
        self.Fields = FieldsStub(channel)
        self.Enums = EnumsStub(channel)
        self.EnumValues = EnumValuesStub(channel)
        self.Platform = PlatformStub(channel)

        self.metadata = (('webezy-io-token',token),)

    def dump_project(self,project_id) -> WebezyJson:

        project_id = project_id[1:]
        project = project_id.split('.')[1]
        org = project_id.split('.')[0]
        
        project_services = {}
        services = self.Services.ListServices(
            ListServicesRequest(project_id=project_id),
            metadata=self.metadata
        )

        print_info('\t- Pulling services...')
        for s in services:
            project_services[s.service.name] = s.service

        project_packages = {}
        packages = self.Packages.ListPackages(
            ListPackagesRequest(
                project=project,
                organization=org
            ),
            metadata=self.metadata
        )

        print_info('\t- Pulling packages...')
        for p in packages:
            project_packages['protos/{}/{}.proto'.format(p.package.package.split('.')[2],p.package.package.split('.')[1])] = p.package

        organization = self.Platform.GetOrganization(GetOrganizationRequest(org_id=org),metadata=self.metadata)

        project = self.Platform.GetProject(GetProjectRequest(project=project_id),metadata=self.metadata)
        wz_json = WebezyJson(domain=organization.organization.domain,project=project.project,services=project_services,packages=project_packages)

        return wz_json


        