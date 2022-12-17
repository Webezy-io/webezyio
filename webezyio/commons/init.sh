#!/bin/bash
# Copyright (c) 2022 Webezy.io.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

declare -a services=("protos")
echo "Init started for proto files" 
pwd
DESTDIR='./protos'
for SERVICE in "${services[@]}"; do
    # mkdir -p $DESTDIR
    echo $SERVICE
    python3 -m grpc_tools.protoc \
        --proto_path=$SERVICE/ \
        --python_out=$DESTDIR \
        --grpc_python_out=$DESTDIR \
        $SERVICE/*.proto
done
statuscode=$?
echo "Exit code for protoc -> "$statuscode
cd $DESTDIR
for FILE in *; do
    filename=$FILE
    search="import"
    replace="from . import"
    sed -i'.bak' -e "4,20s/^$search/$replace/gi" $filename
    rm -f *.bak
done