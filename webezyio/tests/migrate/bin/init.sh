#!/bin/bash

declare -a services=("protos")
echo "[WEBEZYIO] init.sh starting protoc compiler"
DESTDIR="./protos"
for SERVICE in "${services[@]}"; do
    python3 -m grpc_tools.protoc --proto_path=$SERVICE/ --python_out=$DESTDIR --grpc_python_out=$DESTDIR $SERVICE/*.proto
done
statuscode=$?
echo "Exit code for protoc -> "$statuscode
[[ "$statuscode" != "0" ]] && { echo "Some error occured during init script"; exit 1; }
exit 0