import itertools
import logging
import os
import sys
import pluggy

from webezyio.builder.src import hookspecs, lru
from webezyio.builder.plugins import WebezyBase, WebezyDocker, WebezyProto, WebezyPy, WebezyPyClient, WebezyReadme, WebezyTsClient, WebezyTsServer
from webezyio.commons import file_system, helpers, resources, errors
from webezyio.commons.pretty import print_error
from webezyio.commons.protos.webezy_pb2 import WzResourceWrapper
_WELL_KNOWN_PLUGINS = [WebezyProto, WebezyPy,WebezyPyClient,WebezyTsClient,WebezyTsServer,
                        WebezyReadme]  # Many More To Come
log = logging.getLogger('webezyio.cli.main')


class WebezyBuilder:
    """Webezy builder class, it is a wrapper for the implemented plugins and is used to invoking the hooks
    Defined on :module:`webezyio.builder.src.hookspecs`
    """

    def __init__(self, path, hooks=None, project_name=None, server_language=None, clients=None):
        self._pm = pluggy.PluginManager("builder")
        self._webezy_context = None
        self._pm.add_hookspecs(hookspecs)
        self._pm.load_setuptools_entrypoints("builder")
        self._webezy_json = self._parse_webezy_json(path)
        self._cache = lru.LruCache[resources.WzResourceWrapper](100)
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
            self._pm.register(hook)
            log.info(f'Registerd plugin -> {self._pm.get_name(hook)}')

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

        # Default docker
        if deployment_type == 'DOCKER':
            self._pm.register(WebezyDocker)

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

        if server_lang == 'typescript':
            self._pm.register(WebezyTsServer)
     
        
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

    def PackageProject(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.package_project` hook"""
        results = self._pm.hook.pre_build(
            wz_json=self._webezy_json, wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def BuildAll(self):
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
        package = self.PackageProject()
        results = [prebuild, init, context, protos, services,
                   server, compile, readme, protoclass, clients, postbuild, package]
        return results

    def BuildOnlyProtos(self):
        prebuild = self.PreBuild()
        init = self.InitProjectStructure()
        context = self.RebuildContext()
        protos = self.BuildProtos()
        results = [prebuild, init, context, protos]
        return results

    def BuildOnlyCode(self):
        services = self.BuildServices()
        server = self.BuildServer()
        compile = self.CompileProtos()
        readme = self.WriteReadme()
        protoclass = self.OverrideGeneratedClasses()
        clients = self.BuildClients()
        postbuild = self.PostBuild()
        package = self.PackageProject()
        results = [services, server, compile, readme, protoclass, clients, postbuild, package]
        return results

    @property
    def WZJson(self):
        return self._webezy_json
