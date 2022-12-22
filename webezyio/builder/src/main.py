import importlib
import itertools
import logging
import os
import sys
import pluggy

from webezyio.builder.src import hookspecs, lru
from webezyio.builder.plugins import WebezyBase, WebezyDocker, WebezyGoServer, WebezyMonitor, WebezyProto, WebezyProxy, WebezyPy, WebezyPyClient, WebezyReadme, WebezyTsClient, WebezyTsServer,WebezyGoClient,WebezyWebpack
from webezyio.commons import file_system, helpers, resources, errors
from webezyio.commons.pretty import print_error, print_info, print_warning

# ADD MORE WELL KNOWN PLUGINS HERE
_WELL_KNOWN_PLUGINS = [WebezyProto, WebezyPy,WebezyPyClient,WebezyTsServer,WebezyTsClient,WebezyGoServer,WebezyGoClient,WebezyWebpack,
                        WebezyReadme]  # Many More To Come

log = logging.getLogger('webezyio.cli.main')

class WebezyBuilder:
    """
    Webezy builder class, it is a wrapper for the implemented plugins and is used to invoking the hooks
    Defined on :module:`webezyio.builder.src.hookspecs`
    """

    def __init__(self, path, hooks=None, project_name=None, server_language=None, clients=None, configs:resources.WebezyConfig=None):
        self._configs = configs
        self._pm = pluggy.PluginManager("webezyio")
        self._webezy_context = None
        self._pm.add_hookspecs(hookspecs)
        
        loaded_plugins = self._pm.load_setuptools_entrypoints("webezyio")
        # print_info(importlib_metadata.distributions())
        print_info("Loaded installed plugins: {}".format(loaded_plugins))
        if hasattr(self._configs,'plugins'):
            # If plugins array specified under `WebezyConfig.plugins` and not empty -
            # The plugins specified under project configurations will be cross-validated against the `load_setuptools_entrypoints()` values
            # Which should result with the installed packages that includes entry_points { 'webezyio' : [...] }
            if len(self._configs.plugins) > 0:
                plugins_omit_prefix = list(map(lambda x: '_'.join(x.split('webezyio-')[1].split('-')) ,self._configs.plugins))
                self.import_custom_plugins(self._configs.plugins)
                for name, mod in self._pm.list_name_plugin():
                    print_info(name,True,plugins_omit_prefix)
                    if name not in plugins_omit_prefix:
                        self._pm.set_blocked(name)
            # If `WebezyConfig.plugins` is empty array - 
            # We block the installed package to not "automaticlly" import installed packahges to avoid unattended behaviour
            else:
                print_warning("All installed webezyio-XXX plugins will be blocked, since `WebezyConfig.plugins` array is empty")
                for name, mod in self._pm.list_name_plugin():
                    self._pm.set_blocked(name)


        for name, mod in self._pm.list_name_plugin():
            if mod is None:
                print_warning("Found \"webezyio-{}\" plugin that is not passed to `WebezyConfig.plugins` array".format(name))
            else:
                print_info(mod.__name__,True,'Loaded Plugin -> {}'.format(name))

        self._plugins = pluggy.PluginManager("plugins")
        self._plugins.add_hookspecs(hookspecs)
        self._plugins.load_setuptools_entrypoints("plugins")

        self._webezy_json = self._parse_webezy_json(path)
        # self._cache = lru.LruCache[resources.WzResourceWrapper](100)
        self.hooks = hooks
        self._protos_map = {}
        self._path = path
        self._project_name = project_name
        self._server_language = server_language
        self._clients = clients

        if hooks:
            self._register_hooks()
        else:
            self._auto_register_hooks()

       

        self._parse_webezy_context(path)
        self._parse_protos(path)
        self._validate_json_proto()
    def _validate_json_proto(self):
        pass

    def _parse_protos(self, path):
        if self._webezy_json is not None:
            if self._webezy_json.services is not None:
                for svc in self._webezy_json.services:
                    sys.path.append(path.split('/webezy.json')[0])
                    os.chdir(path.split('/webezy.json')[0])
                    try:
                        self._protos_map[svc] = resources.parse_proto(
                            file_system.join_path('protos', f'{svc}.proto'))
                    except Exception:
                        log.debug("Error while parsing existing protos")

    def _register_hooks(self) -> None:
        for hook in self.hooks:
            if hook in _WELL_KNOWN_PLUGINS:
                self._pm.register(hook)
                print_info(f'Registerd well known plugin -> {self._pm.get_name(hook)}')
            else:
                self._plugins.register(hook)
                print_info(f'Registerd custom plugin -> {self._plugins.get_name(hook)}')

    def _auto_register_hooks(self):
        server_lang = self._webezy_json.get_server_language()

        deployment_type = self._webezy_json._config.get('deployment') if self._webezy_json._config.get('deployment') is not None else 'LOCAL'
        proxy = self._webezy_json._config.get('proxy')

        # Default base
        self._pm.register(WebezyBase)
        # Default proto
        self._pm.register(WebezyProto)
        # Default Readme
        self._pm.register(WebezyReadme)
        client_py = next((c for c in self._webezy_json.project.get('clients') if c.get('language') == 'python'),False)
        client_ts = next((c for c in self._webezy_json.project.get('clients') if c.get('language') == 'typescript'),False)
        client_go = next((c for c in self._webezy_json.project.get('clients') if c.get('language') == 'go'),False)
        client_webpack = next((c for c in self._webezy_json.project.get('clients') if c.get('language') == 'webpack'),False)

        # Default docker
        if deployment_type == 'DOCKER':
            print_error("WebezyDocker plugins not supported yet !")
            self._pm.register(WebezyDocker)
            self._pm.register(WebezyProxy)
            self._pm.register(WebezyMonitor)

        # Default proxy
        if proxy is not None:
            pass

        # Code generators plugins
        if server_lang == 'python':
            self._pm.register(WebezyPy)
        elif client_py != False:
            self._pm.register(WebezyPyClient)
           
        if client_ts:
            self._pm.register(WebezyTsClient)

        if client_go:
            self._pm.register(WebezyGoClient)

        if client_webpack:
            self._pm.register(WebezyWebpack)

        if server_lang == 'typescript':
            self._pm.register(WebezyTsServer)
        if server_lang == 'go':
            self._pm.register(WebezyGoServer)
        
        for p in _WELL_KNOWN_PLUGINS:
            plug_name = self._pm.get_name(p)
            if plug_name is not None:
                log.debug(f'Registerd plugin -> {plug_name}')

    def _parse_webezy_json(self, path):
        try:
            return helpers.WZJson(file_system.rFile(path=path, json=True))
        except Exception:
            return None

    def _parse_webezy_context(self, path):
        path = path.replace('webezy.json', '.webezy/context.json')
        try:
            old_context = file_system.rFile(path=path, json=True)
            context = old_context
            file_system.wFile(path, context, json=True, overwrite=True)
            self._webezy_context = helpers.WZContext(context)
            # print(self._webezy_context)

        except Exception:
            log.warning(
                "No .webezy/context.json file ! - Init .webezy/context.json")
            results = self._pm.hook.init_context(
                wz_json=self._webezy_json, wz_context=None)
            results = list(itertools.chain(*results))
            # print(results)
            try:
                context = file_system.rFile(path=path, json=True)
                self._webezy_context = helpers.WZContext(context)
            except Exception as e:
                log.warning(
                    "Error init context, make sure you import a plugin that implement the `init_context` hook")

    def InitProjectStructure(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.init_project_structure` hook"""
        results = self._pm.hook.init_project_structure(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def BuildServices(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_services` hook"""
        results = self._pm.hook.write_services(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def BuildProtos(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_protos` hook"""
        results = self._pm.hook.write_protos(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def CompileProtos(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.compile_protos` hook"""
        results = self._pm.hook.compile_protos(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def BuildClients(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_clients` hook"""
        results = self._pm.hook.write_clients(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def BuildServer(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_server` hook"""
        results = self._pm.hook.write_server(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def WriteReadme(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_readme` hook"""
        results = self._pm.hook.write_readme(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def RebuildContext(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.rebuild_context` hook"""
        results = self._pm.hook.rebuild_context(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def OverrideGeneratedClasses(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.override_generated_classes` hook"""
        results = self._pm.hook.override_generated_classes(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def PreBuild(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.pre_build` hook"""
        results = self._pm.hook.pre_build(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def PostBuild(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.post_build` hook"""
        results = self._pm.hook.post_build(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def ParseProtosToResource(self, protos_dir=None, project_name=None, server_language=None, clients=[],domain=None):
        """Executing the :func:`webezyio.builder.src.hookspecs.parse_protos_to_resource` hook"""
        path = self._path.replace(
            'webezy.json', 'protos') if protos_dir is None else protos_dir
        server_language = self._server_language if server_language is None else server_language
        project_name = self._project_name if project_name is None else project_name if self._project_name is None else 'unknown-project'
        clients = self._clients if len(clients) == 0 else clients
        results = self._pm.hook.parse_protos_to_resource(
            protos_dir=path, project_name=project_name, server_language=server_language, clients=clients,domain=domain)
        results = list(itertools.chain(*results))
        return results
    
    def BuildMongo(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_models` hook"""
        results = self._plugins.hook.write_models(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def InitPackages(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.init_packages` hook"""
        results = self._plugins.hook.init_packages(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    # def PackageProject(self):
    #     """Executing the :func:`webezyio.builder.src.hookspecs.package_project` hook"""
    #     results = self._pm.hook.pre_build(
    #         wz_json=self._webezy_json, wz_context=self._webezy_context)
    #     results = list(itertools.chain(*results))
    #     return results

    def BuildAll(self):
        custom_plugins = self.BuildCustomPlugins()
        prebuild = self.PreBuild()
        init = self.InitProjectStructure()
        context = self.RebuildContext()
        protos = self.BuildProtos()
        services = self.BuildServices()
        server = self.BuildServer()
        compile = self.CompileProtos()
        readme = self.WriteReadme()
        protoclass = self.OverrideGeneratedClasses()
        clients = self.BuildClients()
        postbuild = self.PostBuild()

        # package = self.PackageProject()
        results = [prebuild, init, context, protos, services,
                   server, compile, readme, protoclass, clients, postbuild, custom_plugins]
        return results

    def BuildOnlyProtos(self):
        custom_plugins = self.BuildCustomPlugins()
        prebuild = self.PreBuild()
        init = self.InitProjectStructure()
        context = self.RebuildContext()
        protos = self.BuildProtos()

        results = [prebuild, init, context, protos, custom_plugins]
        return results

    def BuildOnlyCode(self):
        custom_plugins = self.BuildCustomPlugins()
        services = self.BuildServices()
        server = self.BuildServer()
        compile = self.CompileProtos()
        readme = self.WriteReadme()
        protoclass = self.OverrideGeneratedClasses()
        clients = self.BuildClients()
        postbuild = self.PostBuild()
        # package = self.PackageProject()
        results = [services, server, compile, readme, protoclass, clients, postbuild, custom_plugins]
        return results

    def BuildCustomPlugins(self):
        init_packages = self.InitPackages()
        mongo = self.BuildMongo()
        # TODO add more plugins here
        return [init_packages, mongo]
    @property
    def WZJson(self):
        return self._webezy_json

    def import_custom_plugins(self,plugins):
        for p in plugins:
            try:
                sys.path.append(file_system.get_current_location())
                mod = importlib.import_module(p)
                self._plugins.register(mod)
                print_info(f'Registerd custom plugin -> {mod.__name__}')
            except Exception as e:
                pass
                # print_error(e,True,'Local module import error')