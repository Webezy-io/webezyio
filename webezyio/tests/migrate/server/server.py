"""Webezy.io Generated Server Code"""
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
from concurrent import futures
import time
import grpc
import SampleService_pb2_grpc
import SampleService

def serve(host="0.0.0.0:50051"):
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	SampleService_pb2_grpc.add_SampleServiceServicer_to_server(SampleService.SampleService(),server)
	server.add_insecure_port(host)
	server.start()
	print("[*] Started webezyio server at -> %s" % (host))
	try:
		while True:
			time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(0)

if __name__ == "__main__":
	serve()