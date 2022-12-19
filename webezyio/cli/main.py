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

from datetime import datetime
from importlib import reload
import importlib
import logging
import argparse
import os
from platform import platform
import subprocess
import sys
import inquirer
from inquirer import errors
import re
from webezyio import __version__, config
from webezyio.architect import WebezyArchitect
from webezyio.cli import theme,prompter
from webezyio.commons import client_wrapper, helpers,file_system,errors,resources, parser, config as prj_conf, protos
from webezyio.commons.pretty import print_info, print_note, print_version, print_success, print_warning, print_error
from webezyio.cli.commands import call, extend, migrate, new,build,generate,ls,package as pack,run,edit,template, config as config_command
from pathlib import Path

_TEMPLATES = config.configs.webezyio_templates
# templates_dir = os.path.dirname(os.path.dirname(__file__))+'/commons/templates'
# for d in file_system.walkDirs(templates_dir):
#     if d != templates_dir:
#         for f in file_system.walkFiles(d):
#             domain = d.split('/')[-1]
#             template_name = f.split('.')[0]
#             _TEMPLATES.append(f'@{domain}/{template_name}')

def field_exists_validation(new_field, fields, msg):
    if new_field in fields:
        raise errors.WebezyProtoError(
            'Message', f'Field {new_field} already exits under {msg}')
    return True

def enum_value_validate(answers, current):
    try:
        int(current)
    except Exception:
        raise errors.ValidationError(
            current, reason='Enum Value MUST be an integer value')
    return True


def validation(answers, current):

    if len(current) == 0:
        raise errors.ValidationError(
            current, reason='Resource name must not be blank')
    if len(re.findall('\s', current)) > 0:
        raise errors.ValidationError(
            current, reason='Resource name must not include blank spaces')
    if len(re.findall('-', current)) > 0:
        raise errors.ValidationError(
            current, reason='Resource name must not include hyphens, underscores are allowed')
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if(regex.search(current) != None):
        raise errors.ValidationError(
            current, reason='Resource name must not include special charcters')
    
    return True

log = logging.getLogger(__name__)
well_known_type = ['google.protobuf.Timestamp','google.protobuf.Struct']

fields_opt = [
    protos.WebezyFieldType.Name(protos.TYPE_DOUBLE),
    protos.WebezyFieldType.Name(protos.TYPE_FLOAT),
    protos.WebezyFieldType.Name(protos.TYPE_INT64),
    protos.WebezyFieldType.Name(protos.TYPE_INT32),
    protos.WebezyFieldType.Name(protos.TYPE_BOOL),
    protos.WebezyFieldType.Name(protos.TYPE_STRING),
    protos.WebezyFieldType.Name(protos.TYPE_MESSAGE),
    protos.WebezyFieldType.Name(protos.TYPE_BYTES),
    protos.WebezyFieldType.Name(protos.TYPE_ENUM),
]
field_label = [
    protos.WebezyFieldLabel.Name(protos.LABEL_OPTIONAL),
    protos.WebezyFieldLabel.Name(protos.LABEL_REPEATED)
]



# wz_new_q = [
#     inquirer.List("server", message="Choose server language", choices=[
#                   ('Python', Language.python), ('Typescript', Language.typescript)], default=Language.python),
#     inquirer.Checkbox("clients", message="Choose clients languages (Use arrows keys to enable disable a language)", choices=[
#                       ('Python', Language.python), ('Typescript', Language.typescript)], default=[Language.python]),
#     inquirer.Text("domain", message="Enter domain name", default='domain'),
# ]

wz_g_p_q = [
    prompter.QText(name="package",message="Enter package name",validate=validation)
]
wz_g_s_q = [
    prompter.QText(name="service",message="Enter service name",validate=validation)
]
wz_g_e_q = [
    prompter.QText(name="enum",message="Enter enum name",validate=validation)
]


def main(args=None):
    # Print webezy 'Logo'
    print(theme.logo_ascii_art_color)
    # If first run of CLI ask for analytic usage
    if config.configs.first_run:
        confirm_analytics = prompter.QConfirm(name='analytic',message='We want to gather some basic usage and bug report while you are using webezyio CLI',color='warning',default=True)
        analytic = prompter.ask_user_question(questions=[confirm_analytics])
        p = Path(__file__).parents[1]
        hash_token=platform()+':'+datetime.today().isoformat()

        config_file = ''.join(file_system.rFile(file_system.join_path(p,'config.py')))
        config_file = config_file.replace('token=""','token="{}"'.format(hash_token))
        file_system.wFile(file_system.join_path(p,'config.py'),content=config_file,overwrite=True)

        if analytic is None or analytic.get('analytic') == False:
            reload(config)
            helpers.send_analytic_event({'DisabledAnalytic':hash_token})
            config_file = config_file.replace('analytics=True','analytics=False')
        else:
            config_file = config_file.replace('analytics=False','analytics=True')
        config_file = config_file.replace('first_run=True','first_run=False')
        file_system.wFile(file_system.join_path(p,'config.py'),content=config_file,overwrite=True)

    """
    Main CLI processing, with argpars package.
    """
    # Main cli parser
    parser = argparse.ArgumentParser(prog='webezy',
                                     description='Command line interface for the webezyio package build awesome gRPC micro-services. For more information please visit https://www.webezy.io there you can find additional documentation and tutorials.',
                                     epilog=f'For more information see - https://www.webezy.io/docs/cli | Created with love by Amit Shmulevitch. 2022 © webezy.io [{__version__.__version__}]')

    # Instantiating sub parsers object
    subparsers = parser.add_subparsers(
        help='Main modules to interact with Webezy CLI.')

    """New command"""
    parser_new = subparsers.add_parser('new', help='Create new project')
    parser_new.add_argument('project', help='Project name')
    parser_new.add_argument('-p', '--path', required=False,
                            help='Path for the project root directory')
    parser_new.add_argument('--port', default=50051,
                            required=False, help='Port server will run on')
    parser_new.add_argument('--host', default='localhost',
                            required=False, help='Host name for server')
    parser_new.add_argument('--domain',
                            required=False, help='Project domain')
    parser_new.add_argument('--server-language',
                            required=False, help='Server language')
    parser_new.add_argument('--clients', nargs='*',
                            required=False, help='Clients language list seprated by spaces')
    parser_new.add_argument('--template', default=_TEMPLATES[0],
                            required=False, help='Create new project based on template')
  

    parser_n = subparsers.add_parser('n', help='A shortend for new commands')
    parser_n.add_argument('project', help='Project name')
    parser_n.add_argument('-p', '--path', required=False,
                          help='Path for the project root directory')
    parser_n.add_argument('--port', default=50051,
                            required=False, help='Port server will run on')
    parser_n.add_argument('--host', default='localhost',
                            required=False, help='Host name for server')
    parser_n.add_argument('--domain',
                            required=False, help='Project domain')
    parser_n.add_argument('--server-language',
                            required=False, help='Server language')
    parser_n.add_argument('--clients', nargs='*',
                            required=False, help='Clients language list seprated by spaces')
   
    parser_n.add_argument('--template', choices=_TEMPLATES,default=_TEMPLATES[0],
                            required=False, help='Create new project based on template')
    """Generate command"""

    parser_generate = subparsers.add_parser(
        'generate', help='Generate resources commands')
    parser_generate.add_argument('resource', choices=[
                                 'service', 'package', 'message', 'rpc', 'enum'], help='Generate a webezyio resource from specific resource type')
    parser_generate.add_argument('-n', '--name', help='Name for the resource')
    parser_generate.add_argument('-p', '--parent', help='Name for the parent resource')
    parser_generate.add_argument('--build', action='store_true',
                            required=False, help='Auto build resources')

    parser_g = subparsers.add_parser(
        'g', help='A shortend for generate commands')
    parser_g.add_argument('resource', choices=[
                          's', 'p', 'm', 'r', 'e'], help='Generate a webezyio resource from specific resource type, for e.x "s" stands for "service"')
    parser_g.add_argument('-n', '--name', help='Name for the resource')
    parser_g.add_argument('-p', '--parent', help='Name for the parent resource')
    parser_g.add_argument('--build', action='store_true',
                            required=False, help='Auto build resources')

    """List command"""

    parser_list = subparsers.add_parser('ls', help='List resources commands')

    parser_list.add_argument(
        '--full-name',metavar='fullName',required=False, help='Display a resource report for specific resoource by passing in a full name, for e.x domain.test.GetTest will return "GetTest" (RPC) which under "test" (service)')
    parser_list.add_argument('-t', '--type', choices=['service', 'package', 'message',
                             'rpc', 'enum'], help='List a webezyio resource from specific resource type')
    
    """Package command"""
    
    parser_pkg = subparsers.add_parser(
        'package', help='Attach a package into other services / package')
    parser_pkg.add_argument('source', help='Package full name')
    parser_pkg.add_argument('target', help='Package path or service name')
    parser_pkg.add_argument('-r','--remove',action='store_true', help='Package path or service name')

    """Edit command"""
    
    parser_edit = subparsers.add_parser(
        'edit', help='Edit any webezy.io resource')
    parser_edit.add_argument('name', help='Resource full name')
    parser_edit.add_argument('-a','--action',choices=['add','remove','modify'], help='Choose which action to preform on resource')
    parser_edit.add_argument('--sub-actions',nargs='*', help='Choose which sub-action to preform on resource')

    """Template command"""
    parser_template = subparsers.add_parser(
        'template', help='Create a template from your webezy.json / proto files directory / webezy.template.py')
    parser_template.add_argument('path', help='Path for webezy.json / protos files directory / webezy.template.py')
    parser_template.add_argument('-c','--code', action='store_true', help='Create a template including code files')
    parser_template.add_argument('--out-path', help='Specify the template file location, defaulted to root project dir')
    parser_template.add_argument('--template-name', help='Specify the template name, defaulted to project package name')
    parser_template.add_argument('--load',action='store_true', help='Initalize a template')

    """Build command"""
    parser_build = subparsers.add_parser(
        'build', help='Build project resources')
    parser_build.add_argument('--protos',action='store_true', help='Build resources protos files only')
    parser_build.add_argument('--code',action='store_true', help='Build resources code classes files only')

    """Call command"""
    parser_call = subparsers.add_parser(
        'call', help='Call a RPC')
    parser_call.add_argument('service', help='Service full path')
    parser_call.add_argument('rpc', help='RPC name')
    parser_call.add_argument('--debug',action='store_true', help='Debug the call process')
    parser_call.add_argument('--host',default='localhost', help='Pass a host of service')
    parser_call.add_argument('--port',default=50051, help='Pass a port for service')
    parser_call.add_argument('--timeout',default=10, help='An optional duration of time in seconds to allow for the RPC')

    """Extend command"""
    
    parser_extend = subparsers.add_parser(
        'extend', help='Extend any webezy.io resource')
    parser_extend.add_argument('name', help='Resource full name')
    parser_extend.add_argument('--extension', help='Extension full name')

    """Run server"""
    parser_run_server = subparsers.add_parser(
        'run', help='Run server on current active project')
    parser_run_server.add_argument(
        '--debug',action='store_true', help='Start the gRPC server with debug mode attached')


    """Migrate command"""
    praser_migrate = subparsers.add_parser('migrate',help='Migrate existing gRPC project to Webezy.io project')
    praser_migrate.add_argument('protos',help='Relative path of proto directory')
    praser_migrate.add_argument('--format',choices=['json','python'],help='Relative path of proto directory')
    praser_migrate.add_argument('--server-language',default='python',choices=['python','typescript'],help='Chose a server language for migration')
    praser_migrate.add_argument('--clients',nargs='*',default=['python'],choices=['python','typescript'],help='Enter one or more clients')

    """Configs command"""
    parse_configs = subparsers.add_parser(
        'configs', help='Display Webezy.io Configurations')
    parse_configs.add_argument('--edit',action="store_true", help='Edit configurations')
    parse_configs.add_argument('--dict',action="store_true",default=False, help='Display all configs of of current project in dictionary mode')


    # Utils
    parser.add_argument('-v', '--version', action='store_true',
                        help='Display webezyio current installed version')

    parser.add_argument('-e', '--expand', action='store_true',
                        help='Expand optional fields for each resource')

    # Log level optional argument
    parser.add_argument(
        '--loglevel', default='ERROR', help='Log level',
        choices=['DEBUG', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL', ])

    parser.add_argument(
        '--verbose', action='store_true', help='Control on verbose logging')
    
    parser.add_argument(
        '-u','--undo', action='store_true', help='Undo last webezy.json modification')
    parser.add_argument(
        '-r','--redo', action='store_true', help='Redo webezy.json modification, if undo has been made.')


    parser.add_argument('--purge',action='store_true',help='Purge .webezy/contxt.json file')
    # Parse all command line arguments
    args = parser.parse_args(args)
    
    log.setLevel(args.loglevel)
    log.debug(args)

    if config.configs.analytics:
        helpers.send_analytic_event(args)

    # Logging version
    if args.version:
        print_version(__version__.__version__)
        exit(0)

    if args.verbose:
        print_note(args,True,'Argument passed to webezy CLI')

    if hasattr(args, 'project'):
        """New command process"""

        # print_info(args,True)
        new.create_new_project(args.project,args.path,args.host,args.port,args.server_language,args.clients,args.domain,template=args.template)
        exit(0)
    else:
        if helpers.check_if_under_project():
            
            # webezy_project_config = prj_conf.parse_project_config(os.getcwd())
            webezy_json_path = file_system.join_path(os.getcwd(), 'webezy.json')

            try:
                WEBEZY_JSON = file_system.rFile(webezy_json_path, json=True)
                WEBEZY_JSON = helpers.WZJson(webezy_json=WEBEZY_JSON)
            except:
                print_error("Error - webezy.json file is not valid !")
                exit(1)
                
            if args.expand:
                print_note('Creating resource in expanded mode')

            if args.verbose:
                print_note(WEBEZY_JSON._webezy_json, True, 'webezy.json')

            if hasattr(args, 'resource'):
                """Generate command process"""

                # Small validations:
                # Project name
                if WEBEZY_JSON.project.get('name') is None:
                    print_warning("Project name value is not specified !")
                # Project domain 
                if WEBEZY_JSON.domain is None:
                    print_warning("Project domain value is not specified !")

                namespace = parse_namespace_resource(
                    args.resource, WEBEZY_JSON, args.parent)
                resource_name = f' [{args.name}]' if args.name is not None else ''
                
                print_info(
                    f"Generating new resource '{namespace[0]}'{resource_name}")
                results = prompter.ask_user_question(
                    questions=namespace[1] if args.name is None else namespace[1][1:])

                if results is None:
                    print_error('Must answer all questions')
                    exit(1)

                ARCHITECT = WebezyArchitect(
                    path=webezy_json_path,domain=WEBEZY_JSON.domain,project_name=WEBEZY_JSON.project.get('name'))
                if namespace[0] == 'package':
                    generate.package(results,WEBEZY_JSON,ARCHITECT,args.expand,args.verbose)
                
                elif namespace[0] == 'service':
                    generate.service(results,WEBEZY_JSON,ARCHITECT,args.expand,args.verbose)
                
                elif namespace[0] == 'message':
                    generate.message(results,WEBEZY_JSON,ARCHITECT,args.expand,args.verbose,args.parent)

                elif namespace[0] == 'rpc':
                    generate.rpc(results,WEBEZY_JSON,ARCHITECT,parent=args.parent,expand=args.expand)

                elif namespace[0] == 'enum':
                    generate.enum(results,WEBEZY_JSON,ARCHITECT,parent=args.parent)

                if args.build:
                    build.build_all(webezy_json_path)

            elif hasattr(args, 'source') and hasattr(args, 'target'):
                """Package command process"""

                if args.remove:
                    pack.remove_import(args.source,args.target,webezy_json_path,WEBEZY_JSON)
                else:
                    pack.import_package(args.source,args.target,webezy_json_path,WEBEZY_JSON)
            
            elif args.undo:
                """Undo command process"""

                path = webezy_json_path.replace('webezy.json','.webezy/cache')
            
                cache_files = file_system.walkFiles(path)
                cache_files.sort()
                last_save = cache_files[len(cache_files)-2 if len(cache_files) > 1 else 1]
                print_note({'cache':cache_files,'action':'undo','active':last_save},pprint=True)
                
                # ARCHITECT = WebezyArchitect(
                    # path=webezy_json_path,save=last_save)
                # ARCHITECT.Save(undo_save=True)
            elif args.redo:
                """Redo command process"""
                
                path = webezy_json_path.replace('webezy.json','.webezy/cache')
            
                cache_files = file_system.walkFiles(path)
                cache_files.sort(reverse=True)
                logging.error(cache_files)
                # ARCHITECT = WebezyArchitect(
                #     path=webezy_json_path,save=cache_files[len(cache_files)-2 if len(cache_files) > 1 else 1])
                # ARCHITECT.Save()
            elif hasattr(args, 'protos') and hasattr(args, 'code'):
                """Build command process"""

                if args.code:
                    print_info("Building project resources code files")
                    build.build_code(webezy_json_path)
                elif args.protos:
                    print_info("Building project resources proto's files")
                    build.build_protos(webezy_json_path)
                elif args.code == False and args.protos == False:
                    print_info("Building project resources")
                    build.build_all(webezy_json_path)
                    
            elif args.purge:
                """Purge command process"""

                temp_path = webezy_json_path.replace('webezy.json','.webezy/context.json')
                confirm_purge = prompter.QConfirm(name='confirm',message='You are about to purge the webezy context are you sure?',default=False)
                confirm = prompter.ask_user_question(questions=[confirm_purge])
                if confirm.get('confirm'):
                    file_system.removeFile(temp_path)
                    print_success("Purged webezy context !")
                else:
                    print_warning("Cancelling purge for webezy context")
            elif hasattr(args,'debug') and hasattr(args, 'rpc') == False:
                """Run command process"""

                run.run_server(WEBEZY_JSON,args.debug)

            elif hasattr(args, 'name') and hasattr(args,'extension') == False:
                """Edit command process"""

                resource = parse_name_to_resource(args.name,WEBEZY_JSON)
                type = resource.get('type')
                ARCHITECT = WebezyArchitect(
                    path=webezy_json_path,domain=WEBEZY_JSON.domain,project_name=WEBEZY_JSON.project.get('name'))
                if type == 'packages':
                    edit.edit_package(resource,args.action,WEBEZY_JSON,ARCHITECT)
                elif type == 'service':
                    edit.edit_service(resource,args.action,WEBEZY_JSON,ARCHITECT)
                elif type == 'descriptors':
                    kind = resource.get('kind')
                    if kind == resources.ResourceKinds.enum.value:
                        edit.edit_enum(resource,action=args.action,sub_actions=args.sub_actions,wz_json=WEBEZY_JSON,architect=ARCHITECT,expand=args.expand)
                    elif kind == resources.ResourceKinds.enum_value.value:
                        edit.edit_enum_value(resource,args.action,WEBEZY_JSON,ARCHITECT)
                    elif kind == resources.ResourceKinds.field.value:
                        edit.edit_field(resource,action=args.action,sub_actions=args.sub_actions,wz_json=WEBEZY_JSON,architect=ARCHITECT,expand=args.expand)
                    elif kind == resources.ResourceKinds.message.value:
                        edit.edit_message(resource=resource,action=args.action,sub_actions=args.sub_actions,wz_json=WEBEZY_JSON,architect=ARCHITECT,expand=args.expand)
                    elif kind == resources.ResourceKinds.method.value:
                        edit.edit_rpc(resource=resource,action=args.action,sub_actions=args.sub_actions,wz_json=WEBEZY_JSON,architect=ARCHITECT,expand=args.expand)
            
            elif hasattr(args,'name') and hasattr(args,'extension'):
                """Extend command process"""

                resource = parse_name_to_resource(args.name,WEBEZY_JSON)
                extend.extend_resource(resource,args.extension,WEBEZY_JSON)

            elif hasattr(args, 'path'):
                """Template command process"""
                ARCHITECT = WebezyArchitect(
                    path=webezy_json_path,domain=WEBEZY_JSON.domain,project_name=WEBEZY_JSON.project.get('name'))
                template_commands(args,WEBEZY_JSON,ARCHITECT)
            
            elif hasattr(args, 'service') and hasattr(args, 'rpc'):
                """Call command process"""
                print_note(f"Calling {args.service}->{args.rpc}")
                call.CallRPC(args.service,args.rpc,WEBEZY_JSON,host=args.host,port=args.port,debug=args.debug,timeout=int(args.timeout))
            
            elif hasattr(args, 'edit'):
                """Config command"""
                if args.edit:
                    print_warning('Nout supporting editing of webezy.io configurations through the CLI yet...')
                else:
                    config_command.display_configs(WEBEZY_JSON.path,dictionary=args.dict)
            else:
                if hasattr(args, 'full_name'):
                    if args.full_name is None:
                        if hasattr(args, 'type'):
                            ls.list_by_resource(args.type,WEBEZY_JSON)
                    else:
                        ls.list_by_name(args.full_name,WEBEZY_JSON)
                else:
                    if hasattr(args,'protos'):
                        print_warning("Cant migrate existing Webezy.io project !")
                        exit(1)
                    parser.print_help()
            
        else:
            if hasattr(args,'protos'):
                migrate.migrate_project(args.protos,output_path=file_system.get_current_location(),format='json',server_language=args.server_language,clients=args.clients)
            elif hasattr(args, 'path'):
                template_commands(args)
            else:
                print_warning(
                    'Not under valid webezyio project !\n\tMake sure you are on the root directory of your project')
                parser.print_help()

def parse_name_to_resource(full_name,wz_json: helpers.WZJson):
    resource = None
    if len(full_name.split('.')) > 4:
        log.debug("Searching for fields / enum values")
        # Field / Enum Value
        pkg_name = full_name.split('.')[1]
        pkg_v = full_name.split('.')[2]
        pkg_path = f'protos/{pkg_v}/{pkg_name}.proto'
        if wz_json.packages[pkg_path].get('messages') is not None:
            msg_name = '.'.join(full_name.split('.')[:-1])
            search_msg = next((m for m in wz_json.packages[pkg_path].get('messages') if m.get('fullName') == msg_name),None)
            if search_msg is not None:
                search_field = next((f for f in search_msg.get('fields') if f.get('fullName') == full_name), None)
                if search_field is not None:
                    resource = search_field
       
    elif len(full_name.split('.')) == 4:
        #  Message / Enum 
        log.debug("Searching for Messages / enum")

        pkg_name = full_name.split('.')[1]
        pkg_v = full_name.split('.')[2]
        pkg_path = f'protos/{pkg_v}/{pkg_name}.proto'
        if wz_json.packages.get(pkg_path) is None:

            if wz_json.services.get(pkg_name).get('methods') is not None and resource is None:
                log.debug("Searching for RPC")
                rpc_name = full_name.split('.')[-1]
                search_rpc = next((e for e in wz_json.services[pkg_name].get('methods') if e.get('name') == rpc_name),None)
                if search_rpc is not None:
                    resource = search_rpc
            else:
                print_error(f'Resource cant be found as {pkg_path} does not exists')
                exit(1)
        else:

            if wz_json.packages.get(pkg_path).get('messages') is not None:
                search_msg = next((m for m in wz_json.packages[pkg_path].get('messages') if m.get('fullName') == full_name),None)
                if search_msg is not None:
                    resource = search_msg
            
            if wz_json.packages.get(pkg_path).get('enums') is not None and resource is None:
                search_enum = next((e for e in wz_json.packages[pkg_path].get('enums') if e.get('fullName') == full_name),None)
                if search_enum is not None:
                    resource = search_enum

    elif len(full_name.split('.')) == 3:
        # Package
        log.debug("Searching for Package")
        pkg_name = full_name.split('.')[1]
        pkg_v = full_name.split('.')[2]
        pkg_path = f'protos/{pkg_v}/{pkg_name}.proto'
        if wz_json.packages.get(pkg_path) is not None:
           resource = wz_json.packages.get(pkg_path)
    elif len(full_name.split('.')) == 1:
        # Service / Project
        if wz_json.services.get(full_name) is not None:
           resource = wz_json.services.get(full_name)

    if resource is None:
        print_error(f'Can not find any resource by the name -> {full_name}\n\t-> Try running: $ wz ls')
        exit(1)
    else:
        log.debug('Found resource {0}:{1}'.format(resource.get('type'),resource.get('kind')))

    return resource

def parse_namespace_resource(name, wz_json: helpers.WZJson,parent:str=None):
    questions = []
    namespace = name[0]
    if namespace == 's':
        namespace = 'service'
        questions = wz_g_s_q
    elif namespace == 'p':
        namespace = 'package'

        questions = wz_g_p_q
    elif namespace == 'r':
        namespace = 'rpc'
        services = wz_json.services
        temp_s = []
        if services is None or len(services) == 0:
            print_error(
                "No listed services in webezy.json file\n\tCreate a new service first then return to create a 'message'")
            exit(1)

        for svc in services:
            temp_s.append((services[svc]['name'], services[svc]['fullName']))
        has_service = False
        if parent is not None:
            for s in temp_s:
                if parent in s[0]:
                    parent = s[1]
                    has_service = True

            if has_service == False:
                print_error(f"Service -> {parent} not exists under {wz_json.project.get('name')}")
                exit(1)
        wz_g_r_q = [
            prompter.QText(name="rpc",message="Enter rpc name",validate=validation),
            prompter.QList(name="type", message="Choose message type", choices=[('Unary', (False, False)), (
                'Client stream', (True, False)), ('Server stream', (False, True)), ('Bidi stream', (True, True))]),
        ]

        if has_service == False:
            wz_g_r_q.append(prompter.QList(
                "service", message="Choose a service to attach the rpc", choices=temp_s))
        questions = wz_g_r_q

    elif namespace == 'm':
        namespace = 'message'
        packages = wz_json.packages
        temp_p = []

        if packages is None or len(packages) == 0:
            print_error(
                "No listed packages in webezy.json file\n\tCreate a new package first then return to create a 'message'")
            exit(1)

        for pkg in packages:
            temp_p.append(('{0} [{1}]'.format(packages[pkg]['name'],packages[pkg]['package'])))
        
        has_package = False
        if parent is not None:
            for p in temp_p:
                if parent in p:
                    has_package = True
            if has_package == False:
                print_error(f"Package -> {parent} not exists under {wz_json.project.get('name')}")
                exit(1)

        wz_g_m_q = [
            prompter.QText(name="message", message="Enter message name",
                          validate=validation),
        ]

        if has_package == False:
            wz_g_m_q.append(prompter.QList(
            name="package", message="Choose a package to attach the message", choices=temp_p))

        questions = wz_g_m_q

    elif namespace == 'e':
        namespace = 'enum'
        packages = wz_json.packages
        temp_p = []

        if packages is None or len(packages) == 0:
            print_error(
                "No listed packages in webezy.json file\n\tCreate a new package first then return to create a 'message'")
            exit(1)

        for pkg in packages:
            temp_p.append(('{0} [{1}]'.format(packages[pkg]['name'],packages[pkg]['package']), packages[pkg]['package']))
        has_parent = False

        if parent is not None:
            for p in temp_p:
                if p[1] == parent:
                    has_parent = True
            if has_parent == False:
                print_error(f"{parent} Is not under current project")
                exit(1)
        else:
            wz_g_e_q.append(
                prompter.QList(name='package',message='Choose a package',choices=temp_p))

        questions = wz_g_e_q

    return namespace, questions

def template_commands(args,wz_json:helpers.WZJson=None,architect=None):
    try:
        if args.path == 'list':
            prj_configs = prj_conf.parse_project_config(wz_json.path)
            print_info([temp for temp in prj_configs.get('webezyio_templates') if 'Blank' not in temp],True,'Webezy Builtins')
            if prj_configs is not None:
                print_note(prj_configs.get('custom_templates'),True,'Custom Templates [config.py]')
        else:
            if file_system.check_if_file_exists(args.path):
                if args.load:
                    template.load_template(args.path)
                else:
                    if 'webezy.json' in args.path:
                        prj_configs = prj_conf.parse_project_config(wz_json.path,proto=True)
                        WEBEZY_JSON = file_system.rFile(args.path, json=True)
                        WEBEZY_JSON = helpers.WZJson(webezy_json=WEBEZY_JSON)
                        filename = WEBEZY_JSON.project.get('packageName') if args.template_name is None else args.template_name
                        save_file_location = args.path.replace('webezy.json','{0}.template.py'.format(filename)) if args.out_path is None else file_system.join_path(args.out_path,'{0}.template.py'.format(filename))
                        if prj_configs.template is not None:
                            filename = filename if prj_configs.template.name is None else filename
                            save_file_location = save_file_location if prj_configs.template.out_path is None else file_system.join_path(WEBEZY_JSON.path.replace('webezy.json',''),prj_configs.template.out_path,'{0}.template.py'.format(filename))

                        parent_path = file_system.join_path(file_system.get_current_location(),os.path.dirname(save_file_location))
                        include_code = args.code if prj_configs.template is None else prj_configs.template.include_code if  prj_configs.template.include_code is not None else False

                        if file_system.check_if_dir_exists(parent_path):
                            file_system.wFile(save_file_location,template.create_webezy_template_py(WEBEZY_JSON,include_code,prj_configs),overwrite=True)
                            print_success("Generated project template for '{0}'\n\t-> {1}".format(WEBEZY_JSON.project.get('name'),save_file_location))
                        else:
                            print_warning("Path to template output path does not exist ! [{0}] - Will try to create the sub-dir".format(save_file_location))                        
                            file_system.wFile(save_file_location,template.create_webezy_template_py(WEBEZY_JSON,include_code,prj_configs),overwrite=True,force=True)
                            print_success("Generated project template for '{0}'\n\t-> {1}".format(WEBEZY_JSON.project.get('name'),save_file_location))
                            exit(1)
                    # elif '.proto' in args.path:
                    #     parse = parser.WebezyParser(path=args.path)
                    #     print(parse)
                    else:
                        if file_system.check_if_dir_exists(args.path):
                            # builder = WebezyBuilder(path=file_system.get_current_location(),hooks=[WebezyMigrate])
                            # builder.PreBuild()
                            # print_info(file_system.join_path(file_system.get_current_location(),args.path))
                            # builder.ParseProtosToResource(project_name="test",protos_dir=file_system.join_path(file_system.get_current_location(),args.path),clients=[],server_language="python")
                            # builder.PostBuild()
                            raise errors.WebezyProtoError("Not supported yet","Will be used to pass a directory path which holds proto files")
                        else:
                            raise errors.WebezyProtoError("Export Service Template Error","File type not supported")
            elif file_system.check_if_dir_exists(args.path):
                raise errors.WebezyProtoError("Not supported yet","Will be used to pass a directory path which holds proto files")
            else:
                # Handle custom template import / builtin template
                if '@' in args.path:
                    prj_configs = prj_conf.parse_project_config(wz_json.path)
                    if args.path in config.webezyio_templates:
                        # Check if suffix of template name is Py
                        if 'Py' == args.path[len(args.path)-2:] and wz_json.project.get('server').get('language') != 'python':
                            raise errors.WebezyValidationError("Not supporting server language","The [{0}] template is only supporting 'python' as server language please try and run - wz template {1} --load".format(args.path,args.path.replace('Py','Ts')))
                        # Check if suffix of template name is Ts
                        if 'Ts' == args.path[len(args.path)-2:] and wz_json.project.get('server').get('language') != 'typescript':
                            raise errors.WebezyValidationError("Not supporting server language","The [{0}] template is only supporting 'typescript' as server language please try and run - wz template {1} --load".format(args.path,args.path.replace('Ts','Py')))
                        # Attach template from builtins
                        helpers.attach_template(architect,args.path)
                    else:
                        # Handle custom templates
                        if prj_configs is not None:
                            print_warning("Attaching custom templates. If you want to attach a builtin template drop the 'templates' array in config.py file.")
                            if prj_configs.get('custom_templates'):
                                for temp in prj_configs.get('custom_templates'):
                                    template_path = file_system.join_path(file_system.get_current_location(),temp[1])
                                    if temp[0] == args.path:
                                        if file_system.check_if_file_exists(template_path):
                                            # Attach template from custom templates
                                            print_info("Running template file for {0}".format(args.path))
                                            subprocess.run(['python',template_path,'--domain',architect._domain,'--project-name',architect._project_name])
                                        else:
                                            raise errors.WebezyValidationError("Template not found","The template file is not found on : {0}".format(template_path))
                                    else:
                                        raise errors.WebezyValidationError("Template not found","Custom template [{0}] not listed on 'templates' array at config.py file.".format(args.path))
                            else:
                                raise errors.WebezyValidationError("Config templates are empty","Please make sure you configurd a list of templates in your custom config.py file under root project directory")
                else:
                    raise errors.WebezyProtoError("Export Service Template Error","Make sure you are passing a valid path to webezy.json / protos directory / webezy.template.py script for WebezyArchitect - or a valid id for the template!")
    except Exception as e:
        print_error(e,True,e.__class__.__name__+' : '+e.resource if hasattr(e,'resource') else '')