import itertools
import logging
import os
import sys
import pluggy

from webezyio.builder.src import hookspecs
from webezyio.builder.plugins import WebezyProto, WebezyPy, WebezyReadme,WebezyTs
from webezyio.commons import file_system,helpers,resources,errors
_WELL_KNOWN_PLUGINS = [WebezyProto,WebezyPy,WebezyTs,WebezyReadme] # Many More To Come

class WebezyBuilder:
    """Webezy builder class, it is a wrapper for the implemented plugins and is used to invoking the hooks
    Defined on :module:`webezyio.builder.src.hookspecs`
    """

    def __init__(self, path, hooks=None):
        self._pm = pluggy.PluginManager("builder")
        self._pm.add_hookspecs(hookspecs)
        self._pm.load_setuptools_entrypoints("builder")
        self._webezy_json = self._parse_webezy_json(path)
        self._parse_webezy_context(path)
        self.hooks = hooks
        self._protos_map = {}
        
        if hooks:
            self._register_hooks()
        else:
            self._auto_register_hooks()

        self._parse_protos(path)
        self._validate_json_proto()
        
    def _validate_json_proto(self):
        pass

    def _parse_protos(self,path):
        for svc in self._webezy_json.services:
            sys.path.append(path.split('/webezy.json')[0])
            os.chdir(path.split('/webezy.json')[0])
            try:
                self._protos_map[svc] = resources.parse_proto(file_system.join_path('protos',f'{svc}.proto'))
            except Exception:
                logging.debug("Error while parsing existing protos")

    def _register_hooks(self) -> None:
        for hook in self.hooks:
            self._pm.register(hook)
            logging.debug(f'Registerd plugin -> {self._pm.get_name(hook)}')

    def _auto_register_hooks(self):
        server_lang = self._webezy_json.get_server_language()
        # Default proto
        self._pm.register(WebezyProto)
        # Default Readme
        self._pm.register(WebezyReadme)
        if server_lang == 'python':
            self._pm.register(WebezyPy)
        elif server_lang == 'typescript':
            self._pm.register(WebezyTs)
        else:
            raise errors.WebezyCoderError('ServerLanguage',f'Not supporting {server_lang} as server language at the moment.')
        for p in _WELL_KNOWN_PLUGINS:
            plug_name = self._pm.get_name(p)
            if plug_name is not None:
                logging.debug(f'Registerd plugin -> {plug_name}')

    def _parse_webezy_json(self, path):
        return helpers.WZJson(file_system.rFile(path=path,json=True))

    def _parse_webezy_context(self, path):
        path = path.replace('webezy.json','.webezy/context.json')
        try:
            old_context = file_system.rFile(path=path,json=True)
            context = old_context
            file_system.wFile(path,context,json=True,overwrite=True)

            self._webezy_context= helpers.WZContext(context)

        except Exception:
            logging.warning("No .webezy/context.json file ! - Init .webezy/context.json")
            self._init_context_json(path,True)

    def _init_context_json(self,path,write=False):
        files = []
        for svc in self._webezy_json.services:
            methods = []
            for rpc in self._webezy_json.services[svc].get('methods'):
                rpc_name = rpc.get('name')
                methods.append(resources.WZMethodContext(name=rpc_name,code=f'\t\t# TODO - add code\n\t\tsuper().{rpc_name}(request, context) # Remove when ready\n\n',type='rpc'))
            files.append(resources.WZFileContext(file=f'./services/{svc}.py',methods=methods))
        context = resources.proto_to_dict(resources.WZContext(files=files))
        if write:
            logging.debug("Writing new context")
            file_system.mkdir(path.replace('/context.json',''))
            file_system.wFile(path,context,json=True,overwrite=True)
            self._webezy_context = helpers.WZContext(context)
        else:
            return context

    def InitProjectStructure(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.init_project_structure` hook"""
        results = self._pm.hook.init_project_structure(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results

    def BuildServices(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_services` hook"""
        results = self._pm.hook.write_services(wz_json=self._webezy_json,wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def BuildProtos(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_protos` hook"""
        results = self._pm.hook.write_protos(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results

    def CompileProtos(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.compile_protos` hook"""
        results = self._pm.hook.compile_protos(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results

    def BuildClients(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_clients` hook"""
        results = self._pm.hook.write_clients(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results

    def BuildServer(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_server` hook"""
        results = self._pm.hook.write_server(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results

    def WriteReadme(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_readme` hook"""
        results = self._pm.hook.write_readme(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results

    def RebuildContext(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.rebuild_context` hook"""
        results = self._pm.hook.rebuild_context(wz_json=self._webezy_json,wz_context=self._webezy_context)
        results = list(itertools.chain(*results))
        return results

    def OverrideGeneratedClasses(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.override_generated_classes` hook"""
        results = self._pm.hook.override_generated_classes(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results


    @property
    def WZJson(self):
        return self._webezy_json
