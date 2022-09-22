from google.protobuf.timestamp_pb2 import Timestamp
from typing import Iterator
import SampleService_pb2_grpc
import SamplePackage_pb2

class SampleService(SampleService_pb2_grpc.SampleServiceServicer):

	# @rpc @@webezyio - DO NOT REMOVE
	def SampleUnary(self, request: SamplePackage_pb2.SampleMessage, context) -> SamplePackage_pb2.SampleMessage:
		# response = SamplePackage_pb2.SampleMessage(SampleString=None)
		# return response

		super().SampleUnary(request, context)

