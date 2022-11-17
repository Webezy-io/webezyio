from typing import Tuple,Iterator
import grpc
import sys
from functools import partial
from . import SampleService_pb2_grpc as SampleServiceService
from . import OtherPackage_pb2 as OtherPackage
from . import SamplePackage_pb2 as SamplePackage

# For available channel options in python visit https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h
_CHANNEL_OPTIONS = (("grpc.keepalive_permit_without_calls",1),
	("grpc.keepalive_time_ms",120000),
	("grpc.http2.min_time_between_pings_ms",120000),
	("grpc.keepalive_timeout_ms",20000),
	("grpc.http2.max_pings_without_data",0),)

class testproject:

	def __init__(self, host="localhost", port=50051, timeout=10):
		channel = grpc.insecure_channel('{0}:{1}'.format(host, port),_CHANNEL_OPTIONS)
		try:
			grpc.channel_ready_future(channel).result(timeout=timeout)
		except grpc.FutureTimeoutError:
			sys.exit('Error connecting to server')
		self.SampleServiceStub = SampleServiceService.SampleServiceStub(channel)

	def SampleRPC_WithCall(self, request: SamplePackage.SampleMessage, metadata: Tuple[Tuple[str,str]] = ()) -> Tuple[SamplePackage.SampleMessage, grpc.Call]:
		"""webezyio -  Returns: RPC output and a call object"""

		return self.SampleServiceStub.SampleRPC.with_call(request,metadata=metadata)

	def SampleRPC(self, request: SamplePackage.SampleMessage, metadata: Tuple[Tuple[str,str]] = ()) -> SamplePackage.SampleMessage:
		"""webezyio - """

		return self.SampleServiceStub.SampleRPC(request,metadata=metadata)

	def TestRPC_WithCall(self, request: Iterator[OtherPackage.OtherMessage], metadata: Tuple[Tuple[str,str]] = ()) -> Tuple[OtherPackage.OtherMessage, grpc.Call]:
		"""webezyio -  Returns: RPC output and a call object"""

		return self.SampleServiceStub.TestRPC.with_call(request,metadata=metadata)

	def TestRPC(self, request: Iterator[OtherPackage.OtherMessage], metadata: Tuple[Tuple[str,str]] = ()) -> OtherPackage.OtherMessage:
		"""webezyio - """

		return self.SampleServiceStub.TestRPC(request,metadata=metadata)

	def OtherRPC_WithCall(self, request: Iterator[OtherPackage.OtherMessage], metadata: Tuple[Tuple[str,str]] = ()) -> Tuple[SamplePackage.SampleMessage, grpc.Call]:
		"""webezyio -  Returns: RPC output and a call object"""

		return self.SampleServiceStub.OtherRPC.with_call(request,metadata=metadata)

	def OtherRPC(self, request: Iterator[OtherPackage.OtherMessage], metadata: Tuple[Tuple[str,str]] = ()) -> SamplePackage.SampleMessage:
		"""webezyio - """

		return self.SampleServiceStub.OtherRPC(request,metadata=metadata)