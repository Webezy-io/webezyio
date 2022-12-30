####################
  Commands
####################

.. code-block:: bash

    positional arguments:
    {new,n,generate,g,ls,package,edit,template,build,call,extend,run,migrate,configs}
                            Main modules to interact with Webezy CLI.
        new                 Create new project
        n                   A shortend for new commands
        generate            Generate resources commands
        g                   A shortend for generate commands
        ls                  List resources commands
        package             Attach a package into other services / package
        edit                Edit any webezy.io resource
        template            Create a template from your webezy.json / proto files directory / webezy.template.py
        build               Build project resources
        call                Call a RPC
        extend              Extend any webezy.io resource
        run                 Run server on current active project
        migrate             Migrate existing gRPC project to Webezy.io project
        configs             Display Webezy.io Configurations

    options:
    -h, --help            show this help message and exit
    -v, --version         Display webezyio current installed version
    -e, --expand          Expand optional fields for each resource
    --loglevel {DEBUG,DEBUG,WARNING,ERROR,CRITICAL}
                            Log level
    --verbose             Control on verbose logging
    -u, --undo            Undo last webezy.json modification
    -r, --redo            Redo webezy.json modification, if undo has been made.
    --purge               Purge .webezy/contxt.json file


.. toctree::
   :glob:
   :reversed:
   :maxdepth: 2

   *