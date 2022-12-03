# Service templating

A unique feature allow you to develop locally your project and generate a template or a "Snapshot" of your project resources which can be shared or built on top for versions or branches the generated script currently in `Python` only. (Future use may include Typescript as well)

This script can be consumed by the `Webezy.io CLI` to generate your webezy.json and all other directories structure, then you can normally like every webezy project edit or add resources as you wish ! as it was your own services from scratch, allowing you to develop fast and even build your own "Opensource" template which can be reused or refactored as user wish.

Also you can create a new template which holds generated code to `WebezyArchitect` class based on your already pre-defined services, which we use this technique to distribute services templates that can be installed on different projects.

## Create a template from service
```sh
webezy template <path/to/webezy.json> --out-path templates --template-name <SomeTemplate>
```

## Load a template for blank service
```sh
webezy template <mycustom.template.py> --load
```

[WebezyArchitect API Example](../../webezyio/tests/blank/test.py)

__Builtins Templates__:

You can use quick start templates that are built in the webezyio.commons.template module as follows:

```sh
# A sample python server
wz new <SomeProject> --template @webezyio/SamplePy
# A sample typescript server
wz new <SomeProject> --template @webezyio/SampleTs
```

[HelloWorld Python Template](../../webezyio/commons/templates/webezyio/HelloWorldPy.template.py) - `@webezyio/HelloWorldPy`

[HelloWorld Typescript Template](../../webezyio/commons/templates/webezyio/HelloWorldTs.template.py) - `@webezyio/HelloWorldTs`

[SamplePy Template](https://github.com/Webezy-io/webezyio/blob/main/webezyio/commons/templates/webezyio/SamplePy.template.py) - `@webezyio/SamplePy`

[SampleTs Template](https://github.com/Webezy-io/webezyio/blob/main/webezyio/commons/templates/webezyio/SamplePy.template.py) - `@webezyio/SamplePy`

[Publisher Subscriber Typescript Template](../../webezyio/commons/templates/webezyio/PubSubTs.template.py) - `@webezyio/PubSubTs`

> __Note__ You can list all available templates with the following command: `wz template list`

## Configure template options
Each template can be configured in `webezy.json` file under `"config"` value for easy generating without elborate CLI commands:

__`webezy.json`__

```json
{
  "config": {
    "template": {
      "outPath": "template",
      "name": "SamplePy",
      "description": "A basic sample project for webezyio. It is included with examples for all RPC's types and using Enums + Nested Messages, including 'Well Known' messages from google",
      "include": [
        "typescript.ts",
        "python.py",
        "services"
      ],
      "author": "Amit Shmulevitch",
      "includeCode": true
    }
  }
}
```

Or alternatively __`config.py`__

```py
template={
  "outPath": "template",
  "name": "SamplePy",
  "description": "A basic sample project for webezyio.\
    It is included with examples for all RPC's types\
    and using Enums + Nested Messages, including 'Well Known'\
    messages from google",
  "include": [
    "typescript.ts",
    "python.py",
    "services"
  ],
  "author": "Amit Shmulevitch",
  "includeCode": True
}
```


With those specifications described above we can now call the `template` command without any further arguments.
```sh
wz template webezy.json
```
> __Note__ the "includeCode" key it can be passed as `-c` / `--code` argument to `wz template` command, it is passed to the exporter of template and includes all files listed under project while searching for `"include"` list of files and folders then cross checking the `"exclude"` list against them - Each file listed in the "includes" array will be compressed and attached to the template script.

> __Warning__ DO NOT set sensitive information on template code files that are included on template, such as keys and secrets as it will be copied to the template script.

## Read more
See more info on [templating and project configurations](./custom_configurations.md#template-configurations)