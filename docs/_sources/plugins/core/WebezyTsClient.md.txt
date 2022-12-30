# WebezyTsClient

`WebezyTsClient` is a core plugin for building `Typescript` client from `webezyio` resources configured on `webezy.json` file.

## Overview

`WebezyTsClient` will be registered on `Builder` plugin-manager once it detects that the project hold a server resource of type `typescript`:

Start a `webezyio` project and pass in the `typescript` config:

```sh
$ wz new <some-project>

[?] Choose clients languages (Use arrows keys to enable disable a language) (Use arrow keys <-/->): 
   ◯ Python
 ❯ ◉ Typescript
   ◯ Go
   ◯ Webpack-js
```

It will assign the following resource on your `webezy.json` file:

```json
{
    "project": {
        "clients":[
            {
                "outPath" : "/your/project/path/clients/typescript",
                "language" : "typescript"
            }
        ] 
    }
}
```


## Generated Files

On `wz build` process `WebezyTsClient` plugin will build the following files:

| File 	| Description 	| Overwrite 	|
|---	|---	|---	|
| `services/index.ts` 	| The module that wrappes all services stubs | **V** 	|


## Hooks

| Hook 	| Description 	|
|---	|---	|
| `pre_build` 	| **-** 	|
| `post_build` 	| **-** 	|
| `init_project_structure` 	|  	|
| `write_clients` 	| Write `services/index.ts` file 	|
| `compile_protos` 	| Copy compiled `proto` modules to `clients/typescript/protos/*` 	|


## Mini Hooks


Mini hooks can be used on `WebezyTsClient` to inject the core plugin with additional parameters combined from different `Custom Plugins` that implementing:

- `pre_build_clients`:
Hook implemantation for injecting data into `write_clients` hook execution.

To write a custom plugin that uses `WebezyTsClient` see more information on [Writing Custom Plugin](../custom_plugins.md)

Main hook: `webezyio.builder.plugins.WebezyTsClient`

| Mini Hook 	| Description 	| Parameters 	|
|---	|---	|---	|
| `write_clients():append_imports` 	| Append imports to client class 	| **List[String]**<br>Default: [] 	|
| `write_clients():append_exports` 	| Append export to client class 	| **List[String]**<br>Default: [] 	|
| `write_clients():override_stubs` 	| Override default behaviour of stub generations 	| **String**<br>Default: "" 	|
| `write_clients():append_client_options` 	| Append additional client channel options 	| **Dict[String, String]**<br>Default: {} 	|
| `write_clients():add_before_init` 	| Add code block before class 	| **List[String]**<br>Default: [] 	|
| `write_clients():append_interceptors` 	| Append interceptors 	| **List[String]**<br>Default: [] 	|