# Webezy CLI

> Note: `Webezy CLI` has been moved to new repository [Sylk Build CLI](https://github.com/sylk-build/sylk)

[sylk](https://www.sylk.build) is free and open-source project that aims to be a complete framework for developing micro-services projects.
The underlying communication protocol is [```HTTP2```](https://en.wikipedia.org/wiki/HTTP/2) and for serialization and deserialization is [```protobuf```](https://developers.google.com/protocol-buffers/docs/pythontutorial).
It utulize those communication protocol, message serialization / deserialization and code generator with [```gRPC```](https://grpc.io) open-source project by google. 

sylk.build has been created to give devlopers quick and structerd way for building gRPC services without pain while keeping thins open for further modifications.

In result we are trying not to restrict the implemantations themselves but instead applying small restrictions on the project structure for well defined, re-usable structure that can be used by many languages and scenarios.

The current supported languages are:
|                **Language**               | **Server** | **Client** |  **Status**  |
|:-----------------------------------------:|:----------:|:----------:|:------------:|
|     [Python](./docs/source/python.md)     |    **V**   |    **V**   |    Stable    |
| [Typescript](./docs/source/typescript.md) |    **V**   |    **V**   |    Stable    |
|         [Go](./docs/source/go.md)         |    **V**   |    **V**   | Experimental |
| [Webpack-js](./docs/source/webpack-js.md) |     --     |    **V**   | Experimental |
|                   C#.NET                  |    **X**   |    **X**   |    Planned   |

Get full explanation and many more details on usage at [```sylk.build```](https://www.sylk.build).

The `sylk CLI` is a wrapper for SylkArchitect class which does mainly the processing and execution of creating sylk.jso file.

You can interact with the SylkArchitect class with two main ways:

- __CLI__ - The most common and easy to get you started creating gRPC services.
- __Python API__ - Will be useful for more compehransive project creation flows and for developers who wants to understand how sylk works.

# Installation
Install from pip
```sh
pip install sylk
```
# Docs

Go to [sylk.build Docs](https://docs.sylk.build/) for full explanation.

__Useful Resources__:

- [Awesome gRPC - A curated list of useful resources for gRPC](https://github.com/grpc-ecosystem/awesome-grpc)

- [API Design Guide From Google - Matches well into gRPC specific design patterns](https://cloud.google.com/apis/design/)

# Features:

- __CLI__ Well structerd CLI wrapper to create, edit, run and debug a RPC call to gRPC services
- __Generated Code__ Auto-Generated code classes for Services implemantations and client stubs
    * [Python](./docs/source/languages/python.md)
    * [Typescript](./docs/source/languages/typescript.md)
    * [Go](./docs/source/languages/go.md)
- __Plugins__ Highly pluggable API allow us to create and publish "Extensions" without breaking the code:
    * Readme generator
    * Languages Builder - (Python, Typescript & Go)
    * Proto Builder
    * Dockerize (In-development)
    * Migrate gRPC services to sylk.build project
- __Templating__ As a sylk.build project grows you can template it and share it to your peers for remote work (Branching) or as a 'Built-in' template to be used by other co-workers
- __Unified Extensions__ We have been working on unification process of `Protobuf` Extensions (Calles Custom Options) which will allow us in the future to release more pluggable features directly into your sylk.build workspace

__Tutorials:__
- [Quick Start](https://www.sylk.build/docs/quick-start)

## Quick Start 

> __Note__ Please refer to [CLI docs](https://www.sylk.build/docs/cli) for any question you got, also make sute to use the CLI help `sylk --help` should give you an additional information on every command you may possibly run

To create a [new sylk.build](./docs/source/commands/commands.md#sylk-new) project run the following command:
```sh
sylk new <YourProject>
```
> __Note__ you can create a new project based on template to get started quickly
Sample Python server (Clients are available both in TS + PY)
```sh
sylk n <YourProject> --template @sylk/SamplePy
```
Or the same resources just for Typescript server
```sh
sylk n <YourProject> --template @sylk/SampleTs
```
 - For more information see [Project Templating](./docs/source/templating.md)

Then you will need to navigate into your project

> __Note__ if you didnt specified the `--path` argument when creating new project by default it will create a project under your current directory

```sh
cd <YourProject>
```

After you are under the new project directory you can go ahead and [create sylk.build resources](./docs/source/commands/commands.md#sylk-generate) with those simple commands:

> __Note__ Please note that every sub-command of `generate` and `new` can be shortend with the first letter e.g : `sylk g p` is equivalent to `sylk generate package`

```sh
# Generate new package to hold messages
sylk generate package
# Generate new service to hold RPC's (Methods)
sylk generate service
# Generate message under specified package
sylk generate message
# Generate RPC (Method) under specified service
# Same as running `sylk g r`
sylk generate rpc
```
> __Note__ Make sure before creating new RPC on service that you have imported at least 1 package to be used by the service. for more information visit -> [Package Docs](https://www.sylk.build/docs/tutorials/import-packages)


After you had generated your resources for the project and modified the code (See the docs for more explanation on how to develop your project and make changes [Sample Project](https://www.sylk.build/docs/tutorials/sample-project)).

You can now [build your project](./docs/source/commands/commands.md#sylk-build) and [run your server](./docs/source/commands/commands.md#sylk-run) with those simple commands:

```sh
# First build your project
sylk build
# Then run the server
sylk run 
```

> __Note__ you can auto-build your resources if applicable straight when you are generating them with adding `--build` argument to `sylk generate` comands.

You can use now your client code that has been autogenerated in your specified language(s) on creating the project.

> __Pro-Tip:__ you can always make your commands even shorter with replacing `sylk` with `sylk`

# CLI Usage

Get to know the commands supported by sylk.build CLI and start to use their powers !
__All listed commands can be found here:__
[sylk.build CLI API](./docs/source/commands/commands.md)

The sylk CLI module is essantially a wrapper to the `Architect API` which is just to construct a well defined resource metadata which later on can be used by the `Builder API` to build all resources files (Code files & .proto files)

> __Note__ Each sylk.build CLI command can be called with the abbreviated `sylk`

> __Note__ The CLI has verbose logging system that can be changed accoriding to your needs. we do recommand to keep it to ERROR as default to not overload you with multiple lines for each command - to change the default behaviour run your commands with `sylk --loglevel DEBUG <sub-command>`

# Advanced Usage

There are more advanced use cases for sylk.build which will probably will require some time to get used to sylk.build structure and concepts to really have a useful and meaningful interaction.

__We do recommend to go over [sylk.build Concepts](./docs/source/sylk_concepts.md) before trying some advanced usage__

Some of the features are listed below:

- [Templating](./docs/source/templating.md) - Wrap your project and re-share them among team members or to your won base project templates into other future or existing sylk.build projects.
- [Custom Configurations](./docs/source/custom_configurations.md) - Learn how to define custom configurations for a project to make your life easier.
- [Migration](./docs/source/commands/commands.md#sylk-migrate) - You can now migrate your existing gRPC project to unified structure and resources of sylk.build projects.
- [Extending Protobuf Functionality](./docs/source/extensions.md) - You can configure a custom extension for your resources.

# Batteries Included
sylk.build goal is to make development lifecycles quick and meaningfull while coding a distrubted-system using state of the art technologies.

Some built-ins features are provided so you can jump-start your development right away:

- [sylk.build Official VSCode Extension](https://marketplace.visualstudio.com/items?itemName=sylk.vscode-sylk) - See [docs]()

# Development

We are welcoming any code contribution and help to maintain and release new fetures as well documenting the library.

See our [contirbution page](./docs/source/contirbuting.md)

---
__Created with love by Amit Shmulevitch. 2022 © sylk.build__
