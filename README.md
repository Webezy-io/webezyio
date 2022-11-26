# webezy.io (webezyio)

[![Downloads](https://pepy.tech/badge/webezyio)](https://pepy.tech/project/webezyio)

[![Python 3.6](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-360/)

[webezyio](./docs/webezyio_concepts.md) is free and open-source project that aims to be a complete framework for developing micro-services projects.
The underlying communication protocol is [```HTTP2```](https://en.wikipedia.org/wiki/HTTP/2) and for serialization and deserialization is [```protobuf```](https://developers.google.com/protocol-buffers/docs/pythontutorial).
It utulize those communication protocol, message serialization / deserialization and code generator with [```gRPC```](https://grpc.io) open-source project by google. 

Webezy.io has been created to give devlopers quick and structerd way for building gRPC services without pain while keeping thins open for further modifications.

In result we are trying not to restrict the implemantations themselves but instead applying small restrictions on the project structure for well defined, re-usable structure that can be used by many languages and scenarios.

The current supported languages are:
| **Language** | **Server** | **Client** |   **Status**   |
|:------------:|:----------:|:----------:|:--------------:|
|    [Python](./docs/python.md)    |    **V**   |    **V**   |     Stable     |
|  [Typescript](./docs/typescript.md)  |    **V**   |    **V**   |     Stable     |
| [Go](./docs/go.md)           |    **X**   |    **V**   | Experimental   |
| C#.NET       |    **X**   |    **X**   |     Planned    |


Get full explanation and many more details on usage at [```webezy.io```](https://www.webezy.io).

The `webezyio CLI` is a wrapper for WebezyArchitect class which does mainly the processing and execution of creating webezy.jso file.

You can interact with the WebezyArchitect class with two main ways:

- __CLI__ - The most common and easy to get you started creating gRPC services.
- __Python API__ - Will be useful for more compehransive project creation flows and for developers who wants to understand how webezyio works.

# Installation
Install from pip
```sh
pip install webezyio
```
# Docs

Go to [Webezy.io Docs](https://www.webezy.io/docs) for full explanation.

__Useful Resources__:

- [Awesome gRPC - A curated list of useful resources for gRPC](https://github.com/grpc-ecosystem/awesome-grpc)

- [API Design Guide From Google - Matches well into gRPC specific design patterns](https://cloud.google.com/apis/design/)

# Features:

- __CLI__ Well structerd CLI wrapper to create, edit, run and debug a RPC call to gRPC services
- __Generated Code__ Auto-Generated code classes for Services implemantations and client stubs
    * [Python](./docs/python.md)
    * [Typescript](./docs/typescript.md)
    * [Go](./docs/go.md) (Only Client For Now)
- __Plugins__ Highly pluggable API allow us to create and publish "Extensions" without breaking the code:
    * Readme generator
    * Languages Builder - (Python, Typescript & Go)
    * Proto Builder
    * Dockerize (In-development)
    * Migrate gRPC services to Webezy.io project
- __Templating__ As a Webezy.io project grows you can template it and share it to your peers for remote work (Branching) or as a 'Built-in' template to be used by other co-workers
- __Unified Extensions__ We have been working on unification process of `Protobuf` Extensions (Calles Custom Options) which will allow us in the future to release more pluggable features directly into your Webezy.io workspace

__Tutorials:__
- [Quick Start](https://www.webezy.io/docs/quick-start)

## Quick Start 

> __Note__ Please refer to [CLI docs](https://www.webezy.io/docs/cli) for any question you got, also make sute to use the CLI help `webezy --help` should give you an additional information on every command you may possibly run

To create a [new webezy.io](./docs/commands.md#wz-new) project run the following command:
```sh
webezy new <YourProject>
```
> __Note__ you can create a new project based on template to get started quickly
Sample Python server (Clients are available both in TS + PY)
```sh
wz n <YourProject> --template @webezyio/SamplePy
```
Or the same resources just for Typescript server
```sh
wz n <YourProject> --template @webezyio/SampleTs
```
 - For more information see [Project Templating](./docs/templating.md)

Then you will need to navigate into your project

> __Note__ if you didnt specified the `--path` argument when creating new project by default it will create a project under your current directory

```sh
cd <YourProject>
```

After you are under the new project directory you can go ahead and [create webezy.io resources](./docs/commands.md#wz-generate) with those simple commands:

> __Note__ Please note that every sub-command of `generate` and `new` can be shortend with the first letter e.g : `wz g p` is equivalent to `wz generate package`

```sh
# Generate new package to hold messages
webezy generate package
# Generate new service to hold RPC's (Methods)
webezy generate service
# Generate message under specified package
webezy generate message
# Generate RPC (Method) under specified service
# Same as running `wz g r`
webezy generate rpc
```
> __Note__ Make sure before creating new RPC on service that you have imported at least 1 package to be used by the service. for more information visit -> [Package Docs](https://www.webezy.io/docs/tutorials/import-packages)


After you had generated your resources for the project and modified the code (See the docs for more explanation on how to develop your project and make changes [Sample Project](https://www.webezy.io/docs/tutorials/sample-project)).

You can now [build your project](./docs/commands.md#wz-build) and [run your server](./docs/commands.md#wz-run) with those simple commands:

```sh
# First build your project
webezy build
# Then run the server
webezy run 
```

> __Note__ you can auto-build your resources if applicable straight when you are generating them with adding `--build` argument to `webezy generate` comands.

You can use now your client code that has been autogenerated in your specified language(s) on creating the project.

> __Pro-Tip:__ you can always make your commands even shorter with replacing `webezy` with `wz`

# CLI Usage

Get to know the commands supported by Webezy.io CLI and start to use their powers !
__All listed commands can be found here:__
[Webezy.io CLI API](./docs/commands.md)

The webezyio CLI module is essantially a wrapper to the `Architect API` which is just to construct a well defined resource metadata which later on can be used by the `Builder API` to build all resources files (Code files & .proto files)

> __Note__ Each webezy.io CLI command can be called with the abbreviated `wz`

> __Note__ The CLI has verbose logging system that can be changed accoriding to your needs. we do recommand to keep it to ERROR as default to not overload you with multiple lines for each command - to change the default behaviour run your commands with `wz --loglevel DEBUG <sub-command>`

# Advanced Usage

There are more advanced use cases for Webezy.io which will probably will require some time to get used to Webezy.io structure and concepts to really have a useful and meaningful interaction.

__We do recommend to go over [Webezy.io Concepts](./docs/webezyio_concepts.md) before trying some advanced usage__

Some of the features are listed below:

- [Templating](./docs/templating.md) - Wrap your project and re-share them among team members or to your won base project templates into other future or existing Webezy.io projects.
- [Custom Configurations](./docs/custom_configurations.md) - Learn how to define custom configurations for a project to make your life easier.
- [Migration](./docs/commands.md#wz-migrate) - You can now migrate your existing gRPC project to unified structure and resources of Webezy.io projects.
- [Extending Protobuf Functionality](./docs/extensions.md) - You can configure a custom extension for your resources.

# Batteries Included
Webezy.io goal is to make development lifecycles quick and meaningfull while coding a distrubted-system using state of the art technologies.

Some built-ins features are provided so you can jump-start your development right away:

- [Webezy.io Official VSCode Extension](https://marketplace.visualstudio.com/items?itemName=webezy.vscode-webezy) - See [docs]()

# Development

We are welcoming any code contribution and help to maintain and release new fetures as well documenting the library.

See our [contirbution page](./docs/contirbuting.md)

---
__Created with love by Amit Shmulevitch. 2022 © webezy.io__