# webezy

webezyio is free and open-source project that aims to be a complete framework for developing micro-services projects.
The underlying communication protocol is [```HTTP2```](https://en.wikipedia.org/wiki/HTTP/2) and for serialization and deserialization is [```protobuf```](https://developers.google.com/protocol-buffers/docs/pythontutorial).
It utulize those communication protocol, message serialization / deserialization and code generator with [```gRPC```](https://grpc.io) opensource project by google. 

Get full explanation and many more details on usage at [```webezy.io```](https://www.webezy.io).



# Installation
Install from pip
```sh
pip install webezy
```

# Sub-modules

* builder - A command-pattern module for easy interacting with webezy.json
* cli - A CLI interface module for webezy
* coder - A pluggable API for all code generating methods
* commons - Common modules and methods, such as retrieving and modifying protos

# Usage

# Docs

Go to [Webezy.io Docs](https://www.webezy.io/docs) for full explanation.

### Dev-docs
You can build the auto generated docs from the webezyio modules.
It will generate module and function documnetations based on DocsString written on code.

```sh
cd ./docs && make html
```

Open ```./docs/build/html/index.html``` in a browser.