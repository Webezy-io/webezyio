# Builder plugins

Webezy.io allows developer to create thier own modules that inherit from `webezyio.builder` class, this small modules can be activate on specific hooks and mainly in use with building the proto files, code files and project structure as general.

As you may have noted webezyio has it's `Architect` class an `Builder` class which responsible as thier names applies - 

- [`Architect`](./webezyio.architect.rst) __High-Level Design of project__
- [`Builder`](./webezyio.builder.rst) __The "real" processor of resources `Architect` defined to actual working code__

While currently `Architect` plugins are not supported (But we do plan to open this module as well).

The `Builder` Class has been created in "Plug & Play" concept for easier dev workflows and more granluar modules which can be dropped or added without making breeaking changes.

Additionaly custom plugins can be incorporated in `webezyio` projects with well defined `hooks` that the builder register and execute on `wz build` command.

This feature allows you as the developer to further enrich you project creating process with custom files, modules or even changing the projec structure itself to your demands and needs.

See plugins directory for examples - `webezyio/builder/src/plugins`


# Write Custom Plugin

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

