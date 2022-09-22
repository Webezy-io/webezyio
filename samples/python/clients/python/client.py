from typing import Tuple,Iterator
import grpc
import sys
from functools import partial
from . import SampleService_pb2_grpc as SampleServiceService
from . import SamplePackage_pb2 as SamplePackage

class python:

	def __init__(self, host="localhost", port=50051, timeout=10):
		channel = grpc.insecure_channel('{0}:{1}'.format(host, port))
		try:
			grpc.channel_ready_future(channel).result(timeout=timeout)
		except grpc.FutureTimeoutError:
			sys.exit('Error connecting to server')
		self.SampleServiceStub = SampleServiceService.SampleServiceStub(channel)

	def SampleUnary(self, request: SamplePackage.SampleMessage, metadata: Tuple[Tuple[str,str]] = ()) -> SamplePackage.SampleMessage:
		"""webezyio"""

		return self.SampleServiceStub.SampleUnary(request,metadata=metadata)