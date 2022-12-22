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
from typing import overload
from webezyio import _fs,_helpers,_pretty,config as _config
from webezyio.commons.pretty import print_error, print_note, print_warning
from webezyio.commons.protos import WebezyConfig
from google.protobuf.json_format import MessageToDict,ParseDict

log = logging.getLogger('webezyio.cli.main')

class WebezyProjectConfig:

    def __init__(self,**kwargs) -> None:
        """Initalize a custom webezy.io project configurations
        Args
        ----
            
            client_channel_opt (Tuple[Tuple[str,any]])
            custom_templates (List[Tuple(str,str)])
            custom_plugins (List[Tuple(str,str)])
            template - Template options

        """
        self.client_channel_opt = kwargs.get('client_channel_opt')
        self.custom_templates = kwargs.get('custom_templates')
        self.custom_plugins = kwargs.get('custom_plugins')
        self.template = kwargs.get('template')
        self.deployment = kwargs.get('deployment')
        self.monitor = kwargs.get('monitor')
        self.proxy = kwargs.get('proxy')
        self.docs = kwargs.get('docs')

    def config(self):
        temp_dict = {}
        if self.client_channel_opt:
            temp_dict['client_channel_opt'] = self.client_channel_opt
        if self.custom_templates:
            temp_dict['custom_templates'] = self.custom_templates
        if self.custom_plugins:
            temp_dict['custom_plugins'] = self.custom_plugins
        if self.template:
            temp_dict['template'] = self.template
        if self.deployment:
            temp_dict['deployment'] = self.deployment
        if self.monitor:
            temp_dict['monitor'] = self.monitor
        if self.proxy:
            temp_dict['proxy'] = self.proxy
        if self.docs:
            temp_dict['docs'] = self.docs

        return temp_dict

def parse_project_config(root_path:str,proto=False):
    if proto:
        webezy_config = WebezyConfig()
        global_config = parse_global_config_proto()
        # print_note(f'{global_config.host = }\n{global_config.port = }\n{global_config.docs = }\n{global_config.template = }\n{global_config.monitor = }\n{global_config.proxy = }\n{global_config.webezyio_templates = }\n{global_config.first_run = }\n{global_config.token = }\n{global_config.analytics = }\n')
        webezy_config.MergeFrom(global_config)
        
        config_file = parse_config_file_proto(root_path)

        # print_note(f'{config_file.host = }\n{config_file.port = }\n{config_file.docs = }\n{config_file.template = }\n{config_file.monitor = }\n{config_file.proxy = }\n{config_file.webezyio_templates = }\n{config_file.first_run = }\n{config_file.token = }\n{config_file.analytics = }\n')
        # print_note(type(config_file))
        if config_file is not None:
            webezy_config.MergeFrom(config_file)
        webezy_json_configs = parse_webezy_json_configs_proto(root_path)
        print_note(f'{webezy_json_configs.host = }\n{webezy_json_configs.port = }\n{webezy_json_configs.docs = }\n{webezy_json_configs.template = }\n{webezy_json_configs.monitor = }\n{webezy_json_configs.proxy = }\n{webezy_json_configs.webezyio_templates = }\n{webezy_json_configs.first_run = }\n{webezy_json_configs.token = }\n{webezy_json_configs.analytics = }\n')

        if webezy_json_configs is not None:
            webezy_config.MergeFrom(webezy_json_configs)
        # print_note(f'{webezy_config.host = }\n{webezy_config.port = }\n{webezy_config.docs = }\n{webezy_config.template = }\n{webezy_config.monitor = }\n{webezy_config.proxy = }\n{webezy_config.webezyio_templates = }\n{webezy_config.first_run = }\n{webezy_config.token = }\n{webezy_config.analytics = }\n')

    else:
        global_config = parse_global_config_dict()
        # print_note(global_config,True,'Global Configs')

        wz_json_configs = parse_webezy_json_configs(root_path)
        # print_note(wz_json_configs,True,'webezy.json')

        config_file = parse_config_file_dict(root_path)
        # print_note(config_file,True,'config.py')

    
        merged_configs = None 
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 9:
            merged_configs = global_config | wz_json_configs

            if config_file:
                merged_configs = merged_configs | config_file 
        else:

            merged_configs = {**global_config, **wz_json_configs } 
            # print_note(merged_configs,True,'merged_configs.py')

            if config_file is not None:
                merged_configs = {**merged_configs, **config_file }
    # print_note(merged_configs,True,'Merged Config')
    return webezy_config

def parse_webezy_json_configs(root_path):
    webezy_json_path = _fs.join_path(root_path,'webezy.json')
    WEBEZY_JSON = None
    if _fs.check_if_file_exists(webezy_json_path):
        WEBEZY_JSON = _fs.rFile(webezy_json_path, json=True)
        WEBEZY_JSON = _helpers.WZJson(webezy_json=WEBEZY_JSON)
    return WEBEZY_JSON._config if WEBEZY_JSON is not None else None

def parse_webezy_json_configs_proto(root_path):
    WEBEZY_JSON = None
    if _fs.check_if_file_exists(root_path):
        if 'webezy.json' not in root_path:
            root_path = root_path +'/webezy.json'
        print_error(root_path)

        WEBEZY_JSON = _fs.rFile(root_path, json=True)
        WEBEZY_JSON = _helpers.WZJson(webezy_json=WEBEZY_JSON)
        if WEBEZY_JSON._config:
            return ParseDict(WEBEZY_JSON._config,WebezyConfig())
        else:
            return None

def parse_config_file_proto(root_path) -> WebezyConfig:
    custom_config_path = _fs.join_path(root_path,'config.py')
    wz_prj_conf = None
    if _fs.check_if_file_exists(custom_config_path):
        if _fs.get_current_location() not in sys.path:
            sys.path.append(_fs.get_current_location())
        
        prj_conf_module = importlib.import_module('config')
        if hasattr(prj_conf_module,'configs'):
            wz_prj_conf = get_file_config(prj_conf_module)
        else:
            print_warning('You must configure the parameters under \'configs = WebezyConfig.Config()\' variable')
       
    else:
        log.debug("No custom project config.py file")
    return wz_prj_conf

def parse_config_file_dict(root_path):
    custom_config_path = _fs.join_path(root_path,'config.py')
    wz_prj_conf = None
    if _fs.check_if_file_exists(custom_config_path):
        
        if _fs.get_current_location() not in sys.path:
            sys.path.append(_fs.get_current_location())
        
        prj_conf_module = importlib.import_module('config')
        if hasattr(prj_conf_module,'configs'):
            temp_configs = get_file_config(prj_conf_module)
            wz_prj_conf = WebezyProjectConfig(
                # Client channel options see:  https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h
                client_channel_opt = prj_conf_module.client_channel_opt  if hasattr(prj_conf_module,'client_channel_opt') else None,
                # Custom templates
                custom_templates = prj_conf_module.custom_templates  if hasattr(prj_conf_module,'custom_templates') else None,
                # Custom plugins
                custom_plugins = prj_conf_module.custom_plugins  if hasattr(prj_conf_module,'custom_plugins') else None,
                # Templating options
                template = prj_conf_module.template  if hasattr(prj_conf_module,'template') else None,
                deployment = temp_configs.deployment,
                monitor = MessageToDict(temp_configs.monitor),
                proxy =  MessageToDict(temp_configs.proxy),
                host = temp_configs.host,
                plugins = temp_configs.plugins,
                docs = temp_configs.docs

            )
        else:
            print_warning('You must configure the parameters under \'configs = WebezyConfig.Config()\' variable')
       

    else:
        log.debug("No custom project config.py file")
    return None if wz_prj_conf is None else wz_prj_conf.config()

def parse_global_config_dict() :
    global_config_path = dict_from_module(_config.configs)
    return global_config_path

def parse_global_config_proto():
    # temp_module = dict_from_module(_config)
    if hasattr(_config,'configs'):
        return _config.configs
    else:
        print_error('Global configs are not valid !')
    # if temp_module.get('webezyio_templates'):
    #     temp_webezyi_templates = temp_module['webezyio_templates']
    #     del temp_module['webezyio_templates']
    # global_config_path:Config = ParseDict(temp_module,Config)
    # global_config_path.webezyio_templates = temp_webezyi_templates
    # print(global_config_path.host)
    # temp_config = Config(
    #     # host=global_config_path.host,
    #     # port=global_config_path.port,
    #     docs=global_config_path.docs,
    #     deployment=global_config_path.deployment,
    #     proxy=global_config_path.proxy,
    #     monitor=global_config_path.monitor,
    #     webezyio_templates=global_config_path.webezyio_templates,
    #     token=global_config_path.token,
    #     analytics=global_config_path.analytics,
    #     first_run=global_config_path.first_run,
    #     template=global_config_path.template
    # )
    # return temp_config


def dict_from_module(module):
    context = {}
    for setting in dir(module):
        # you can write your filter here
        if setting.islower() and setting[0] != '_':
            context[setting] = getattr(module, setting)
    return context

def get_file_config(prj_config_module) -> WebezyConfig:
    return prj_config_module.configs