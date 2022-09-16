#!/bin/bash

declare -a services=("protos")
echo "Init started for proto files"
pwd
DESTDIR="./protos"
for SERVICE in "${services[@]}"; do
    # mkdir -p $DESTDIR
    echo $SERVICE
    python3 -m grpc_tools.protoc --proto_path=$SERVICE/ --python_out=$DESTDIR --grpc_python_out=$DESTDIR $SERVICE/*.proto
done
statuscode=$?
echo "Exit code for protoc -> "$statuscode
cd $DESTDIR
for FILE in *; do
    filename=$FILE
    search="import"
    replace="from . import"
    sed -i".bak" -e "4,20s/^$search/$replace/gi" $filename
    rm -f *.bak
done