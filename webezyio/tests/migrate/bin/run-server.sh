#!/bin/bash

if [[ $1 == "debug" ]]
then
	echo "Debug Mode: $1"
GRPC_VERBOSITY=DEBUG GRPC_TRACE=all PYTHONPATH=./services/protos:./services python3 server/server.py
else
	PYTHONPATH=./services/protos:./services python3 server/server.py
fi