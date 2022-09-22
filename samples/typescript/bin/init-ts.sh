#!/bin/bash

echo "[WEBEZYIO] init.sh starting protoc compiler"
npm i
node ./bin/proto.js
npm run build
statuscode=$?
echo "Exit code for protoc -> "$statuscode