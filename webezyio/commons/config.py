# Copyright (c) 2022 Webezy.io.

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import importlib
import logging
import os
import sys
from webezyio import _fs,_helpers,_pretty,config as _config
log = logging.getLogger('webezyio.cli.main')

class WebezyProjectConfig:

    def __init__(self,**kwargs) -> None:
        """Initalize a custom webezy.io project configurations
        Args
        ----
            
            client_channel_opt (Tuple[Tuple[str,any]])
            custom_templates (List[Tuple(str,str)])
            custom_plugins (List[Tuple(str,str)])

        """
        self.client_channel_opt = kwargs.get('client_channel_opt')
        self.custom_templates = kwargs.get('custom_templates')
        self.custom_plugins = kwargs.get('custom_plugins')

    def config(self):
        return {
            'client_channel_opt': self.client_channel_opt,
            'custom_templates': self.custom_templates,
            'custom_plugins': self.custom_plugins
        }

def parse_project_config(root_path:str):

    global_config = parse_global_config()
    wz_json_configs = parse_webezy_json_configs(root_path)
    config_file = parse_config_file(root_path)
    
    merged_configs = None 
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
        merged_configs = global_config | wz_json_configs
        merged_configs = merged_configs | config_file
    else:
        merged_configs = {**global_config, **wz_json_configs, **config_file}
    # _pretty.print_info({'config':config_file,'webezy':wz_json_configs},True,merged_configs)
    return merged_configs

def parse_webezy_json_configs(root_path):
    webezy_json_path = _fs.join_path(root_path,'webezy.json')
    WEBEZY_JSON = None
    if _fs.check_if_file_exists(webezy_json_path):
        WEBEZY_JSON = _fs.rFile(webezy_json_path, json=True)
        WEBEZY_JSON = _helpers.WZJson(webezy_json=WEBEZY_JSON)
    return WEBEZY_JSON._config if WEBEZY_JSON is not None else None

def parse_config_file(root_path):
    custom_config_path = _fs.join_path(root_path,'config.py')
    if _fs.check_if_file_exists(custom_config_path):
        
        if _fs.get_current_location() not in sys.path:
            sys.path.append(_fs.get_current_location())
        
        prj_conf_module = importlib.import_module('config')

        wz_prj_conf = WebezyProjectConfig(
            # Client channel options see:  https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h
            client_channel_opt= prj_conf_module.client_channel_opt  if hasattr(prj_conf_module,'client_channel_opt') else None,
            # Custom templates
            custom_templates= prj_conf_module.custom_templates  if hasattr(prj_conf_module,'custom_templates') else None,
            # Custom plugins
            custom_plugins= prj_conf_module.custom_plugins  if hasattr(prj_conf_module,'custom_plugins') else None,

        )

    else:
        log.debug("No custom project config.py file")
    
    return wz_prj_conf.config() if wz_prj_conf is not None else None

def parse_global_config():
    global_config_path = dict_from_module(_config)
    return global_config_path

def dict_from_module(module):
    context = {}
    for setting in dir(module):
        # you can write your filter here
        if setting.islower() and setting[0] != '_':
            context[setting] = getattr(module, setting)

    return context