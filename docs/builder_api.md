## Builder plugins

Webezy.io allows developer to create thier own modules that inherit from `webezyio.builder` class, this small modules can be activate on specific hooks and mainly in use with building the proto files, code files and project structure as general.

As you may have noted webezyio has it's `Architect` class an `Builder` class which responsible as thier names applies - __Design and bring some feel to the project (`Architect`) \ To construct in reality from the highlevel reprepresentationresntation of resource, to actual working code (`Builder`)__

While currently `Architect` plugins are not supported (But we do plan to open this module as well).

The `Builder` Class has been created in plug and play concept for easier and more granluar modules which can be dropped or added without affectively changing how Webezy.io CLI works.

This feature allows you as the developer to further enrich you project creating process with custom files, modules or even changing the projec structure itself to your demands and needs.

[See plugins directory for examples](../webezyio//builder/plugins/)
