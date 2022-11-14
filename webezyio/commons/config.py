import importlib
import logging
import sys
from webezyio import _fs,_helpers,_pretty
log = logging.getLogger('webezyio.cli.main')

class WebezyProjectConfig:

    def __init__(self,**kwargs) -> None:
        self.client_channel_opt = kwargs.get('client_channel_opt')

    def config(self):
        return {
            'client_channel_opt': self.client_channel_opt
        }

def parse_project_config(root_path:str):
    wz_prj_conf = None
    custom_config_path = _fs.join_path(root_path,'config.py')
    if _fs.check_if_file_exists(custom_config_path):
        
        if _fs.get_current_location() not in sys.path:
            sys.path.append(_fs.get_current_location())
        
        prj_conf_module = importlib.import_module('config')

        wz_prj_conf = WebezyProjectConfig(
            client_channel_opt= prj_conf_module.client_channel_opt  if hasattr(prj_conf_module,'client_channel_opt') else None,
        )

        log.debug(wz_prj_conf.config())
    else:
        log.debug("No custom project config.py file")
    
    return wz_prj_conf.config() if wz_prj_conf is not None else None