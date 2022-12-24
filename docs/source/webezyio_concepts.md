
# Understanding Webezy.io

While it is not nesscesary step to get you started we do recommend to invest few minutes to read an overview of how `Webezy.io` Built and utulizing gRPC, this high level overview will make you approach some scenarios more easly.

## Overview
Webezy.io is a __free__ open-source framework for gRPC.

We provide a __complete__ sets of tools that will help developers creating distributed-systems using the latest __"Battle Tested"__ tech available.

The magic of Webezy.io is that we are utulizing another open-source project called
__[`gRPC`](https://grpc.io/)__ - This google based project has been developed to make use of
`HTTP2` (the newer web protocol) and `Protobufers` togther to overcome some of the most __challenging__ topics
__web and backend developers__ encountring __daily__, such as:

- Desrialization / Serialization
- Streaming (WS)
- Multi Language Services
- Schema Evolution Compatibility
- HTTP Headers Overhead
And many more!


## Sub-modules

* builder - A command-pattern module for easy interacting with webezy.json
* cli - A CLI interface module for webezy
* coder - A pluggable API for all code generating methods
* commons - Common modules and methods, such as retrieving and modifying protos

## Project Structure

Every webezy.io project should look like the following schema:

> __Note__ For simplicity we use for this example 1 service (`SampleService`) and 1 package (`SamplePackage`)
```sh
# Root dir of your project
my-project/
├─ bin/ # Some executable scripts
├─ clients/ # All clients code in multiple languages if specified
│  ├─ python/
│     ├─ client.py
├─ server/ # Server file
│  ├─ server.py
├─ protos/ # Proto defintions files
│  ├─ SampleService.proto
│  ├─ Samplepackage.proto
├─ service/ # Service file and protos compiled files
│  ├─ protos/
│  │  ├─ SampleService_pb2.py
│  │  ├─ SampleService_pb2_grpc.py
│  │  ├─ SamplePackage_pb2.py
│  │  ├─ SamplePackage_pb2_grpc.py
│  ├─ SampleService.py
├─ webezy.json # All project resource descriptions
├─ README.md
├─ .gitignore
```

The main compoenent is the `webezy.json` file which conssisting of all project resources and metadata.

This "Snapshot" of current project state is confined into well structerd json format based on its proto message definition at `webezyio.commons.protos.webezy_pb2.py`.

```proto
message WebezyJson {
    string domain = 1;
    Project project = 2;
    map<string, ServiceDescriptor> services = 3;
    map<string, PackageDescriptor> packages = 4;
    WebezyConfig config = 5;
}
```
> __Note__ See how we utulized protobuffers as main serialization and desrialization in our CLI and core modules

This Json document mainly connsist of 4 components:

- `project` - All project specific metadata this data is only to be consumed by internal Webezy.io CLI and modules.
- `config` - Open metadata for various tasks as one of them is to give plugins and other external modules to have context point.
- `packages` - gRPC driven component for all packages which are centralized place for `Enums` and `Messages` under so called "Package" compoenent to be consumed by a "Service".
- `services` - gRPC driven component for all Services which holds details on RPC's, and Service dependencies which are "Packages" that hold "Messages" that relate to RPC's input and output types.
