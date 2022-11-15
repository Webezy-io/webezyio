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
import sys
from webezyio import _fs,_helpers,_pretty
log = logging.getLogger('webezyio.cli.main')

class WebezyProjectConfig:

    def __init__(self,**kwargs) -> None:
        self.client_channel_opt = kwargs.get('client_channel_opt')
        self.templates = kwargs.get('templates')

    def config(self):
        return {
            'client_channel_opt': self.client_channel_opt,
            'templates': self.templates
        }

def parse_project_config(root_path:str):
    wz_json_configs = parse_webezy_json_configs(root_path)
    config_file = parse_config_file(root_path)
    merged_configs = None 
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
        merged_configs = wz_json_configs | config_file
    else:
        merged_configs = {**wz_json_configs, **config_file}
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
            client_channel_opt= prj_conf_module.client_channel_opt  if hasattr(prj_conf_module,'client_channel_opt') else None,
            templates= prj_conf_module.templates  if hasattr(prj_conf_module,'templates') else None,
        )

    else:
        log.debug("No custom project config.py file")
    
    return wz_prj_conf.config() if wz_prj_conf is not None else None