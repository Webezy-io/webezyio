# WebezyGoClient

`WebezyGoClient` is a core plugin for building `Go` client from `webezyio` resources configured on `webezy.json` file.

## Overview

`WebezyGoClient` will be registered on `Builder` plugin-manager once it detects that the project hold a server resource of type `Go`:

Start a `webezyio` project and pass in the `Go` config:

```sh
$ wz new <some-project>

[?] Choose clients languages (Use arrows keys to enable disable a language) (Use arrow keys <-/->): 
   ◯ Python
   ◯ Typescript
 ❯ ◉ Go
   ◯ Webpack-js
```

It will assign the following resource on your `webezy.json` file:

```json
{
    "project": {
        "clients":[
            {
                "outPath" : "/your/project/path/clients/python",
                "language" : "go"
            }
        ] 
    }
}
```


## Generated Files

On `wz build` process `WebezyGoClient` plugin will build the following files:

| File 	| Description 	| Overwrite 	|
|---	|---	|---	|
| `clients/python/__init__.py` 	| The module that wrappes all services stubs | **V** 	|


## Hooks

| Hook 	| Description 	|
|---	|---	|
| `pre_build` 	| **-** 	|
| `post_build` 	| **-** 	|
| `init_project_structure` 	|  	|
| `write_clients` 	| Write `/clients/python/__init__.py` client module file and copies all proto generated modules to `/clients/python/*` 	|
| `compile_protos` 	| Sub process that executing `/bin/init-py.sh` that will compile `.proto` files to `.py` modules 	|


## Mini Hooks


Mini hooks can be used on `WebezyGoClient` to inject the core plugin with additional parameters combined from different `Custom Plugins` that implementing:

- `pre_build_clients`:
Hook implemantation for injecting data into `write_clients` hook execution.

To write a custom plugin that uses `WebezyGoClient` see more information on [Writing Custom Plugin](../custom_plugins.md)

Main hook: `webezyio.builder.plugins.WebezyGoClient`

| Mini Hook 	| Description 	| Parameters 	|
|---	|---	|---	|
| `write_clients():append_imports` 	| Append imports to client class 	| **List[String]**<br>Default: [] 	|
| `write_clients():append_exports` 	| Append export to client class 	| **List[String]**<br>Default: [] 	|
| `write_clients():override_stubs` 	| Override default behaviour of stub generations 	| **String**<br>Default: "" 	|
| `write_clients():append_client_options` 	| Append additional client channel options 	| **Dict[String, String]**<br>Default: {} 	|
| `write_clients():add_before_init` 	| Add code block before class 	| **List[String]**<br>Default: [] 	|
| `write_clients():append_interceptors` 	| Append interceptors 	| **List[String]**<br>Default: [] 	|