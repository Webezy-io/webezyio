# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import WebezyApi_pb2 as WebezyApi__pb2


class MessagesStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateMessage = channel.unary_unary(
                '/Messages/CreateMessage',
                request_serializer=WebezyApi__pb2.CreateMessageRequest.SerializeToString,
                response_deserializer=WebezyApi__pb2.CreateMessageResponse.FromString,
                )
        self.UpdateMessage = channel.unary_unary(
                '/Messages/UpdateMessage',
                request_serializer=WebezyApi__pb2.UpdateMessageRequest.SerializeToString,
                response_deserializer=WebezyApi__pb2.UpdateMessageResponse.FromString,
                )
        self.DeleteMessage = channel.unary_unary(
                '/Messages/DeleteMessage',
                request_serializer=WebezyApi__pb2.DeleteMessageRequest.SerializeToString,
                response_deserializer=WebezyApi__pb2.DeleteMessageResponse.FromString,
                )
        self.GetMessage = channel.unary_unary(
                '/Messages/GetMessage',
                request_serializer=WebezyApi__pb2.GetMessageRequest.SerializeToString,
                response_deserializer=WebezyApi__pb2.GetMessageResponse.FromString,
                )


class MessagesServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateMessage(self, request, context):
        """[webezyio] - None
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateMessage(self, request, context):
        """[webezyio] - None
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteMessage(self, request, context):
        """[webezyio] - None
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMessage(self, request, context):
        """[webezyio] - None
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MessagesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateMessage,
                    request_deserializer=WebezyApi__pb2.CreateMessageRequest.FromString,
                    response_serializer=WebezyApi__pb2.CreateMessageResponse.SerializeToString,
            ),
            'UpdateMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateMessage,
                    request_deserializer=WebezyApi__pb2.UpdateMessageRequest.FromString,
                    response_serializer=WebezyApi__pb2.UpdateMessageResponse.SerializeToString,
            ),
            'DeleteMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteMessage,
                    request_deserializer=WebezyApi__pb2.DeleteMessageRequest.FromString,
                    response_serializer=WebezyApi__pb2.DeleteMessageResponse.SerializeToString,
            ),
            'GetMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMessage,
                    request_deserializer=WebezyApi__pb2.GetMessageRequest.FromString,
                    response_serializer=WebezyApi__pb2.GetMessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Messages', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Messages(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Messages/CreateMessage',
            WebezyApi__pb2.CreateMessageRequest.SerializeToString,
            WebezyApi__pb2.CreateMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Messages/UpdateMessage',
            WebezyApi__pb2.UpdateMessageRequest.SerializeToString,
            WebezyApi__pb2.UpdateMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Messages/DeleteMessage',
            WebezyApi__pb2.DeleteMessageRequest.SerializeToString,
            WebezyApi__pb2.DeleteMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Messages/GetMessage',
            WebezyApi__pb2.GetMessageRequest.SerializeToString,
            WebezyApi__pb2.GetMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
