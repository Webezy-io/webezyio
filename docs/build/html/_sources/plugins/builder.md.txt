# Builder Plugins

Webezy.io allows developer to create thier own modules that inherit from `webezyio.builder` class, this small modules can be activate on specific hooks and mainly in use with building the proto files, code files and project structure as general.

As you may have noted webezyio has it's `Architect` class an `Builder` class which responsible as thier names applies - 

- [`Architect`](./webezyio.architect.rst) __High-Level Design of project__
- [`Builder`](./webezyio.builder.rst) __The "real" processor of resources `Architect` defined to actual working code__

While currently `Architect` plugins are not supported (But we do plan to open this module as well).

The `Builder` Class has been created in "Plug & Play" concept for easier dev workflows and more granluar modules which can be dropped or added without making breeaking changes.

Additionaly custom plugins can be incorporated in `webezyio` projects with well defined `hooks` that the builder register and execute on `wz build` command.

This feature allows you as the developer to further enrich you project creating process with custom files, modules or even changing the projec structure itself to your demands and needs.

See plugins directory for examples - `webezyio/builder/src/plugins`
