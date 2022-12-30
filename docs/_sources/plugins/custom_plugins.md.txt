# Writing Custom Plugins

`Webezy.io` Allow developers to build and use custom plugins in thier `webezyio` projects.

Thos plugins can add functionality to your project or even inject the `Core Plugins` with additional supported parameters.

`webezyio` plugins are written using [`Pluggy`](https://pluggy.readthedocs.io/en/stable/#) framework.

You can write as a `Webezy.io` developer a custom plugin that will be hooked to `webezyio` project, the plugin should interact with `webezy.json` file with well-defined utils and helpers.
The main modules you will interact with when writing a `webezyio` plugin are:
- [Builder](./webezyio.builder.rst) - Use the `webezyio.builder.hookimpl` as the decorator for your hook implemeantations
- [WZJson](./webezyio.commons.rst) - A wrapper class to easy interactions with webezy.json

# What Plugins Shouldn't do

`webezyio` plugins __MUST__ not modify existing resource on project it should only parse the project resources and metadata from `webezy.json` by `webezyio.commons.helpers.WZJson` interface and add functionality for the project like additional modules and code files to be auto-generated.

# What Plugins Should do

The main power of `webezyio` plugins is at the project extensions and configurations, you can extend the `protobuf` own functionality with [`Custom Options`](./extensions.md) later after adding the extensions to you resources you can apply additional functionality that reuqires some dynamic user input from the extensions.

All plugins should be written in `Python` and should have the following structure at-least:
```sh
# Root dir of your project must prefixed with `webezyio-`
webezyio-my-plugin/
├─ webezyio_my_plugin.py
├─ README.md
├─ setup.py
```

The setup script for the plugin must include `entry_points` -> `webezyio` this how `webezyio` core module install and register a plugins that installed on the same `venv`

`setup.py`
```py
from setuptools import setup

setup(
    name="webezyio-my-plugin",
    install_requires="webezyio",
    entry_points={"webezyio": ["my_plugin = webezyio_my_plugin"]},
    py_modules=["webezyio_my_plugin"],
    version = "0.0.1"
)
```

Write the hooks implmeantations, see [Hookspecs](./webezyio.builder.src.rst) for all the available hooks that will be executed at `wz build` command

`webezyio_my_plugin.py`
```py
from webezyio.builder import hookimpl
from webezyio.commons.helpers import WZContext, WZJson

@hookimpl
def pre_build(wz_json: WZJson, wz_context: WZContext):
    """Here the caller expects us to return a list."""
    print_info("Starting webezyio build process %s plugin" % (__name__))


@hookimpl
def post_build(wz_json: WZJson, wz_context: WZContext):
    """Here the caller passes a mutable object, so we mess with it directly."""
    print_success("Finished webezyio build process %s plugin" % (__name__))
```

Install the plugin with `pip`
```sh
pip install -e .
```

Now add the plugin name to your own `webezy.json` file under `config`->`plugins`:
```json
{
    "config": {
        "plugins": ["webezyio-my-plugin"]
    }
}
```

After succesfull packaging and installation of your new plugin `webezyio` should recognize it by the `entry_points` -> `webezyio` at `wz build` command execution and will execute all the registered hooks that the plugin implement.

On `wz build` command you should see the following log for your plugin registering -
```sh
[*] Loaded installed plugins: 1
[*] Registering plugin -> my_plugin
[*] Loaded Plugin -> my_plugin
---------------------------------------------
'webezyio_my_plugin'
---------------------------------------------
```

## Extending `Webezy.io` Functionality

By writing custom plugins developer can inject data by implementing `pre_build_xxx` hook and enrich a `Core Plugin` like `WebezyTsServer` with additional parameters which will have different results once the project is built.

A plugin can implement one of the [`pre_build_xxx`](#hooks) hooks and return a set of predefined /dynamic data based on `webezy.json` file this data should be in a well-formatted structure that the targeted plugin will know how to execute.

For e.x if we wish to add functionality to `WebezyTsServer` plugin which implements `write_server` hook as well as others - we can write a small impl. code in our custom plugin to inject some additional data when the `WebezyTsServer` will excute `write_server` hook.

```python
@hookimpl
def pre_build_server(wz_json: WZJson, wz_context: WZContext):
    print_info("Running pre build server")
    return {
        'webezyio.builder.plugins.WebezyTsServer:write_server():overwrite':False,
        'webezyio.builder.plugins.WebezyTsServer:write_server():append_imports':["// Importing custom class from webezyio-mongo-ts plugin","import { WebezyioMongo } from './services/utils/mongo/models';"],
        'webezyio.builder.plugins.WebezyTsServer:write_server():add_before_init':'const db = new WebezyioMongo()',
        # 'webezyio.builder.plugins.WebezyTsServer:append_server_options':[("grpc.max_send_message_length", 256)],
        'webezyio.builder.plugins.WebezyTsServer:write_server():inject_service':{'mongoApi':'db'},
        'webezyio.builder.plugins.WebezyTsServer:write_server():append_startup_promise':['db.ready.then()']
    }
```

> __Note__ The paths are important to be a valid full path to `Target Plugin` : `Target Hook` : `Target parameter` -  so `'webezyio.builder.plugins.WebezyTsServer:write_server():overwrite` will target the `WebeztTsServer` plugin and will inject the data when `write_server()` hook impl. excutes on `WebezyTsServer` - and the hook impl. knows how to handle `overwrite` parameter - For more info see [WebezyTsServer Plugin Docs](WebezyTsServer.md)

### Hooks

Each build process `Webezy.io` initiate a `Builder` instance which excuting and managing all registered `Hooks` from the different custom `webezyio-xxx` plugins and core plugins `WebezyXxx`

Some hook have `pre_build_xxx` data injection when excuted, this allow us to write plugins in ageneric way and attach at runtime dynamic context within "Custom Plugin" that implements `pre_build_xxx` hook.

For a list of [supported hooks](../webezyio.builder.rst)

For a list of [Core Plugins](../webezyio.builder.plugins.rst)
