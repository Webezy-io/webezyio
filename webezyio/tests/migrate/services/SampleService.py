"""Webezy.io service implemantation for -> SampleService"""
import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Iterator
import SampleService_pb2_grpc
import SamplePackage_pb2
import OtherPackage_pb2

class SampleService(SampleService_pb2_grpc.SampleServiceServicer):

	# @rpc @@webezyio - DO NOT REMOVE
	def SampleRPC(self, request: SamplePackage_pb2.SampleMessage, context: grpc.ServicerContext) -> SamplePackage_pb2.SampleMessage:
		# response = SamplePackage_pb2.SampleMessage(ExtendedField=None,Timestamp=None,Integer=None,ChildMessage=None,test=None)
		# return response
		super().SampleRPC(request, context)

	# @rpc @@webezyio - DO NOT REMOVE
	def TestRPC(self, request: Iterator[OtherPackage_pb2.OtherMessage], context: grpc.ServicerContext) -> OtherPackage_pb2.OtherMessage:
		# response = OtherPackage_pb2.OtherMessage(StringField=None)
		# return response

		super().TestRPC(request, context)

	# @rpc @@webezyio - DO NOT REMOVE
	def OtherRPC(self, request: Iterator[OtherPackage_pb2.OtherMessage], context: grpc.ServicerContext) -> SamplePackage_pb2.SampleMessage:
		# response = SamplePackage_pb2.OtherMessage(ExtendedField=None,Timestamp=None,Integer=None,ChildMessage=None,test=None)
		# return response

		super().OtherRPC(request, context)

