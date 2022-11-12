from asyncio.log import logger
from typing import Tuple,Iterator
import grpc
import sys
from functools import partial
from . import Analytics_pb2_grpc as AnalyticsService
from . import WebezyAnalytics_pb2 as WebezyAnalytics
from . import WebezyCore_pb2 as WebezyCore

class webezycore:

	def __init__(self, host="webezy-core.francecentral.cloudapp.azure.com", port=9000, timeout=1):
		channel = grpc.insecure_channel('{0}:{1}'.format(host, port))
		try:
			grpc.channel_ready_future(channel).result(timeout=timeout)
		except grpc.FutureTimeoutError:
			logger.debug("Error connecting to webezy-core server")
		self.AnalyticsStub = AnalyticsService.AnalyticsStub(channel)

	def PublishCLIEvent(self, request: WebezyAnalytics.CLIEvent, metadata: Tuple[Tuple[str,str]] = ()) -> WebezyCore.OkResponse:
		"""webezyio - This is an analytic event from CLI"""

		return self.AnalyticsStub.PublishCLIEvent(request,metadata=metadata)