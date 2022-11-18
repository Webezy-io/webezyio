# Webezy CLI Commands
Below listed all supported Webezy.io CLI commands and their supported arguments.

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
```sh
optional arguments:
  -h, --help            show this help message and exit
  --full-name fullName  Display a resource report for specific resoource by passing in a full name, for e.x domain.test.GetTest will return "GetTest" (RPC) which
                        under "test" (service)
  -t {service,package,message,rpc,enum}, --type {service,package,message,rpc,enum}
                        List a webezyio resource from specific resource type
```

## wz package
Mangae your dependencies inside your project
```sh
positional arguments:
  source        Package full name
  target        Package path or service name

optional arguments:
  -h, --help    show this help message and exit
  -r, --remove  Package path or service name
```
__Import a package into service__

```sh
wz package <domain.package.v1> <servicename>
```

__Import a package into another package__

```sh
wz package <domain.package.v1> <domain.other.v1> 
```

## wz edit
Edit your webezy.io resources

```sh
positional arguments:
  name                  Resource full name

optional arguments:
  -h, --help            show this help message and exit
  -a {add,remove,modify}, --action {add,remove,modify}
                        Choose which action to preform on resource
  --sub-action SUB_ACTION
                        Choose which sub-action to preform on resource
```

__Edit a message__

```sh
wz edit <domain.package.v1.message>
```

## wz build

Build the project resources
```sh
optional arguments:
  -h, --help  show this help message and exit
  --protos    Build resources protos files only
  --code      Build resources code classes files only
```
## wz template
Create or load a project template
```sh
positional arguments:
  path                  Path for webezy.json / protos files directory / webezy.template.py

optional arguments:
  -h, --help            show this help message and exit
  -c, --code            Create a template including code files
  --out-path OUT_PATH   Specify the template file location, defaulted to root project dir
  --template-name TEMPLATE_NAME
                        Specify the template name, defaulted to project package name
  --load                Initalize a template
```

See [Service Templating Section](./docs//templating.md) for more information.

## wz call
Call a service RPC for a running server host
```sh
positional arguments:
  service      Service full path
  rpc          RPC name

optional arguments:
  -h, --help   show this help message and exit
  --debug      Debug the call process
  --host HOST  Pass a host of service
  --port PORT  Pass a port for service
```
For e.x if we want to run a service RPC called "GetUnary" in Service "Test"
we would pass the following command:

```sh
wz call clients/python/Test_pb2_grpc.py GetUnary
```
Not that we passed the relative path from the root directory of the project to the service module under "clients" directory and we used the python client module.

Which will require us to verify we have attached and built a service client in `python`
If you didnt started your prject with `Python` client add the following configuration under `project`.`clients` Array in `webezy.json` file located on your project root directory:
```json
{
  "outDir": "<path-to-project>/clients/python",
  "language": "python"
}
```

Then make sure you re-built the project code so the client modules will be created properly:
```sh
wz build
```

## wz run
Run the project server with attached services
```sh
optional arguments:
  -h, --help  show this help message and exit
  --debug     Start the gRPC server with debug mode attached
```

## wz migrate
Migrate existing gRPC project to a __Webezy.io__ project

```sh
usage: webezy migrate [-h] [--format {json,python}] [--server-language {python,typescript}] [--clients [{python,typescript} [{python,typescript} ...]]] protos

positional arguments:
  protos                Relative path of proto directory

optional arguments:
  -h, --help            show this help message and exit
  --format {json,python}
                        Relative path of proto directory
  --server-language {python,typescript}
                        Chose a server language for migration
  --clients [{python,typescript} [{python,typescript} ...]]
                        Enter one or more clients
```

Go to exisitng gRPC project which hold `.proto` files in __ONE__ parent directory.

Lets say we have our proto file all in one directory under our project called `'Modules'`
we can run the migration plan as follow from the root directory:
```sh
wz migrate --protos Modules
```
It will run the migration for all `.proto` files existing in the directory passed to `--protos` argument.

When the process succeeds we will get an output of all resources parsed into `webezy.json` format at the same path of our original project.

> __Warning__ Migration of project is experimental feature