import itertools
import logging
import os
import sys
import pluggy
from webezyio.builder.src import hookspecs
from webezyio.commons import file_system
from webezyio.commons.file_system import rFile
from webezyio.commons.helpers import WZJson
from webezyio.commons.resources import parse_proto
from webezyio.commons.errors import WebezyCoderError
from webezyio.builder.plugins import WebezyProto, WebezyPy,WebezyTs

_WELL_KNOWN_PLUGINS = [WebezyProto,WebezyPy,WebezyTs] # Many More To Come

class WebezyBuilder:
    """Webezy builder class, it is a wrapper for the implemented plugins and is used to invoking the hooks
    Defined on :module:`webezyio.builder.src.hookspecs`
    """

    def __init__(self, path, hooks=None):
        self._pm = pluggy.PluginManager("builder")
        self._pm.add_hookspecs(hookspecs)
        self._pm.load_setuptools_entrypoints("builder")
        self._webezy_json = self._parse_webezy_json(path)
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
                self._protos_map[svc] = parse_proto(file_system.join_path('protos',f'{svc}.proto'))
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
        if server_lang == 'python':
            self._pm.register(WebezyPy)
        elif server_lang == 'typescript':
            self._pm.register(WebezyTs)
        else:
            raise WebezyCoderError('ServerLanguage',f'Not supporting {server_lang} as server language at the moment.')
        for p in _WELL_KNOWN_PLUGINS:
            plug_name = self._pm.get_name(p)
            if plug_name is not None:
                logging.debug(f'Registerd plugin -> {plug_name}')

    def _parse_webezy_json(self, path):
        return WZJson(rFile(path=path,json=True))

    def InitProjectStructure(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.init_project_structure` hook"""
        results = self._pm.hook.init_project_structure(wz_json=self._webezy_json)
        results = list(itertools.chain(*results))
        return results

    def BuildServices(self):
        """Executing the :func:`webezyio.builder.src.hookspecs.write_services` hook"""
        results = self._pm.hook.write_services(wz_json=self._webezy_json)
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

    @property
    def WZJson(self):
        return self._webezy_json
