# webezy

webezyio is free and open-source project that aims to be a complete framework for developing micro-services projects.
The underlying communication protocol is [```HTTP2```](https://en.wikipedia.org/wiki/HTTP/2) and for serialization and deserialization is [```protobuf```](https://developers.google.com/protocol-buffers/docs/pythontutorial).
It utulize those communication protocol, message serialization / deserialization and code generator with [```gRPC```](https://grpc.io) opensource project by google. 

Webezy.io has been created to give deleopers quick and structerd way for building gRPC services without pain while keeping thins open for further modifications.

In result we are trying not to restrict the implemantations themselves but to restrict the project structure to well defined and re-usable by many languages and scenarios.

The current supported languages are:
| **Language** | **Server** | **Client** |   **Status**   |
|:------------:|:----------:|:----------:|:--------------:|
|    Python    |    **V**   |    **V**   |     Stable     |
|  Typescript  |    **V**   |    **V**   |     Stable     |
| Go           |    **X**   |    **X**   | In-Development |
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



__Tutorials:__
- [Sample project](https://www.webezy.io/docs/tutorials/sample-project)

## Quick Start 

> __Note__ Please refer to [CLI docs](https://www.webezy.io/docs/cli) for any question you got, also make sute to use the CLI help `webezy --help` should give you an additional information on every command you may possibly run

To create a new webezy.io project run the following command:
```sh
webezy new <YourProject>
```
> __Note__ you can create a new project based on template to get started quickly
```sh
wz n <YourProject> --template @webezyio/Sample
```
 - For more information see [Project Templating](https://www.webezyio/docs/project-templating)

Then you will need to navigate into your project

> __Note__ if you didnt specified the `--path` argument when creating new project by default it will create a project under your current directory

```sh
cd <YourProject>
```

After you are under the new project directory you can go ahead and create webezy.io resources with those simple commands:

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

You can now build your project and run your server with those simple commands:

```sh
# First build your project
webezy --build
# Then run the server
webezy --run-server
```

> __Note__ you can auto-build your resources if applicable straight when you are generating them with adding `--build` argument to `webezy generate` comands.

You can use now your client code that has been autogenerated in your specified language(s) on creating the project.

> __Pro-Tip:__ you can always make your commands even shorter with replacing `webezy` with `wz`

# CLI Usage
> __Note__ The CLI has verbose logging system that can be changed accoriding to your needs. we do recommand to keep it to ERROR as default to not overload you with multiple lines for each command - to change the default behaviour run your commands with `wz --loglevel DEBUG <sub-command>`
```sh
Command line interface for the webezyio package build awesome gRPC micro-services. For more information please visit https://www.webezy.io there you can find
additional documentation and tutorials.

positional arguments:
  {new,n,generate,g,ls,package,edit,template}
                        Main modules to interact with Webezy CLI.
    new                 Create new project
    n                   A shortend for new commands
    generate            Generate resources commands
    g                   A shortend for generate commands
    ls                  List resources commands
    package             Attach a package into other services / package
    edit                Edit any webezy.io resource
    template            Create a template from your webezy.json / proto files directory / webezy.template.py

optional arguments:
  -h, --help            show this help message and exit
  --run-server          Run server on current active project
  -v, --version         Display webezyio current installed version
  -e, --expand          Expand optional fields for each resource
  -b, --build           Build webezyio project
  --loglevel {DEBUG,DEBUG,WARNING,ERROR,CRITICAL}
                        Log level
  --verbose             Control on verbose logging
  -u, --undo            Undo last webezy.json modification
  -r, --redo            Redo webezy.json modification, if undo has been made.
  --purge               Purge .webezy/contxt.json file

For more information see - https://www.webezy.io/docs/cli | Created with love by Amit Shmulevitch. 2022 © webezy.io [0.0.4]
```

## wz new
Create new `webezy.io` projects, can be new blank project or refrenced from already existing template.
```sh
positional arguments:
  project               Project name

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path for the project root directory
  --port PORT           Port server will run on
  --host HOST           Host name for server
  --domain DOMAIN       Project domain
  --server-language SERVER_LANGUAGE
                        Server language
  --clients [CLIENTS [CLIENTS ...]]
                        Clients language list seprated by spaces
  --build               Clients language list seprated by spaces
  --template {@webezyio/Blank,@webezyio/Sample}
                        Create new project based on template
```

## wz generate
Generate new webezy.io resources under already existing project
```sh
positional arguments:
  {s,p,m,r,e}           Generate a webezyio resource from specific resource type, for e.x "s" stands for "service"

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Name for the resource
  -p PARENT, --parent PARENT
                        Name for the parent resource
  --build               Auto build resources
```
## wz ls
List your project resources

## wz package
Mangae your dependencies inside your project

## wz edit
Edit your webezy.io resources

## wz template
Create or load a project template

# Understanding Webezy.io
While it is not nesscesary step to get you started we do recommend to invest few minutes to read an overview of how `Webezy.io` Built and utulizing gRPC, this high level overview will make you approach some scenarios more easly.

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
├─ .gitignore
├─ README.md
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

## Service templating

A unique feature allow you to develop locally your project and generate a template or a "Snapshot" of your project resources which can be shared or built on top for versions or branches the generated script currently in `Python` only. (Future use may include Typescript as well)

This script can be consumed by the `Webezy.io CLI` to generate your webezy.json and all other directories structure, then you can normally like every webezy project edit or add resources as you wish ! as it was your own services from scratch, allowing you to develop fast and even build your own "Opensource" template which can be reused or refactored as user wish.

Also you can create a new template which holds generated code to `WebezyArchitect` class based on your already pre-defined services, which we use this technique to distribute services templates that can be installed on different projects.

### Create a template from service
```sh
webezy template <path/to/webezy.json> --out-path templates --template-name <SomeTemplate>
```

### Load a template for blank service
```sh
webezy template <mycustom.template.py> --load
```

[WebezyArchitect API Example](./webezyio/tests/blank/test.py)

[SamplePy Template](./webezyio/commons/templates/webezyio/SamplePy.template.py)

### Configure template options
Each template can be configured in `webezy.json` file under `"config"` value for easy generating without elborate CLI commands:
```json
{
  "config": {
    "template": {
      "outPath": "template",
      "name": "SamplePy",
      "description": "A basic sample project for webezyio.\nIt is included with examples for all RPC's types and using Enums + Nested Messages, including 'Well Known' messages from google.",
      "include": [
        "typescript.ts",
        "python.py",
        "services"
      ],
      "author": "Amit Shmulevitch"
    }
  }
}
```
With those specifications described above we can now call the `template` command without any further arguments.
```sh
wz template webezy.json -c
```
> __Note__ the `-c` / `--code` argument it is telling the exporter of template to include all files listed under project while he searching for `"include"` list of files / folders and cross checking the `"exclude"` list.

### Development

We are welcoming any code contribution and help to maintain and release new fetures as well documenting the library.

See our [contirbution page](./docs/contirbuting.md)

## Builder plugins

Webezy.io allows developer to create thier own modules that inherit from `webezyio.builder` class, this small modules can be activate on specific hooks and mainly in use with building the proto files, code files and project structure as general.

As you may have noted webezyio has it's `Architect` class an `Builder` class which responsible as thier names applies - __Design and bring some feel to the project (`Architect`) \ To construct in reality from the highlevel reprepresentationresntation of resource, to actual working code (`Builder`)__

While currently `Architect` plugins are not supported (But we do plan to open this module as well).

The `Builder` Class has been created in plug and play concept for easier and more granluar modules which can be dropped or added without affectively changing how Webezy.io CLI works.

This feature allows you as the developer to further enrich you project creating process with custom files, modules or even changing the projec structure itself to your demands and needs.

[See plugins directory for examples](./webezyio/builder/plugins/)

# VSCode extension

Webezy.io Developed an [Visual Studio Code](https://code.visualstudio.com/) Extension for developing gRPC service with Webezy.io

The extension main use case is to have a visual represntation and helpers while developing your project resources, allow you to easy navigate inside ever-growing projects and easy command executions with native VSCode GUI.

> __Warning__ As the extension is heavily using `webezyio CLI` it is still dependent on installing the webezyio package and CLI and not to be used as "Stand alone"

[Webezy Extension For VSCode](https://marketplace.visualstudio.com/items?itemName=webezy.vscode-webezy)

[Extension Source Code](https://github.com/Webezy-io/vscode-webezy)

---
__Created with love by Amit Shmulevitch. 2022 © webezy.io__