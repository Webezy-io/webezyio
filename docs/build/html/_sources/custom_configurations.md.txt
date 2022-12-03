# Project Custom Configurations
Each Webezy.io project can be configured to developer needs with creating a `config.py` file at the root directory of yout Webezy.io project another place is the `webezy.json` file under `configs` key or any [Global Configurations](#global-configurations).

## Global Configurations
Each `webezyio` package install on your development environment will included with "Global" configuration file which is overided by default from one of the following sources:

- `webzy.json` - Project main resource descriptions which located under each Webezy.io project at the root directory

- `config.py` - Like `webezy.json` file it may be included as optional override for developers and will overwrite any existing field at the "Global" level and at `webezy.json`

> __Warning__ Do not try and edit the `Global` configurations file as it can be override by other custom configuration locations (Mentioned above)

__Supported Configurations__




## Template configurations

__`templates`__ Make custom templates available for your project.
  You can make custom templates from local or remote project and "import" a template generator script to be used in your new project or already existing project.
  Configure in `config.py` file the following parameters:
```py
templates=[('<TemplateId>','<TemplatePath>')]
```
  - `<TemplateId>` should be replaced with unique and valid id to be identified and imported at your project with Webezy.io CLI, for example our builtins are constructed the same way: `@<domain>/<name><Py/Ts>`
  
  > __Note__ That `<Py/Ts>` is acting as indicator for the supported server language for that specific template

  - `<TemplatePath>` is the relative path to the template generator script - You can generate a template from already running project:

```sh
wz template webezy.json --template-name <SomeTemplate>
```


