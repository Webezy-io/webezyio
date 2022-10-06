import logging
import argparse
import os
from posixpath import split
from webezyio import __version__
import inquirer
from inquirer.themes import Theme, term
from inquirer import errors
import re
from webezyio.builder.src.main import WebezyBuilder
from webezyio.architect import WebezyArchitect
from webezyio.cli.theme import WebezyTheme
from webezyio.commons import helpers,file_system,errors,resources
from webezyio.commons.pretty import print_info, print_note, print_version, print_success, print_warning, print_error
from webezyio.commons.protos.webezy_pb2 import FieldDescriptor, Language
from webezyio.cli.commands import new,build,generate,ls,package as pack,run,edit
from prettytable import PrettyTable


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
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_DOUBLE),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_FLOAT),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_INT64),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_INT32),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_BOOL),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_STRING),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_MESSAGE),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_BYTES),
    FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_ENUM),
]
field_label = [
    FieldDescriptor.Label.Name(FieldDescriptor.Label.LABEL_OPTIONAL),
    FieldDescriptor.Label.Name(FieldDescriptor.Label.LABEL_REPEATED)
]



# wz_new_q = [
#     inquirer.List("server", message="Choose server language", choices=[
#                   ('Python', Language.python), ('Typescript', Language.typescript)], default=Language.python),
#     inquirer.Checkbox("clients", message="Choose clients languages (Use arrows keys to enable disable a language)", choices=[
#                       ('Python', Language.python), ('Typescript', Language.typescript)], default=[Language.python]),
#     inquirer.Text("domain", message="Enter domain name", default='domain'),
# ]

wz_g_p_q = [
    inquirer.Text("package", message="Enter package name",
                  validate=validation),
]

wz_g_s_q = [
    inquirer.Text("service", message="Enter service name",
                  validate=validation),
]

wz_g_e_q = [
    inquirer.Text("enum", message="Enter enum name", validate=validation),
]


def main(args=None):
    """Main CLI processing, with argpars package.
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
    parser_n.add_argument('--build', action='store_true',
                            required=False, help='Clients language list seprated by spaces')

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
    parser_edit.add_argument('--sub-action', help='Choose which sub-action to preform on resource')

    """Run server"""
    parser.add_argument(
        '--run-server',action='store_true', help='Run server on current active project')

    parser.add_argument('-v', '--version', action='store_true',
                        help='Display webezyio current installed version')

    parser.add_argument('-e', '--expand', action='store_true',
                        help='Expand optional fields for each resource')

    parser.add_argument(
        '-b','--build', action='store_true', help='Build webezyio project')
    
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

    # Logging version
    if args.version:
        print_version(__version__.__version__)

    if args.verbose:
        print_note(args,True,'Argument passed to webezy CLI')

    if hasattr(args, 'project'):
        print_info(args,True)
        new.create_new_project(args.project,args.path,args.host,args.port,args.server_language,args.clients,args.domain)
    else:
        if helpers.check_if_under_project():
            
            webezy_json_path = file_system.join_path(os.getcwd(), 'webezy.json')

            WEBEZY_JSON = file_system.rFile(webezy_json_path, json=True)
            WEBEZY_JSON = helpers.WZJson(webezy_json=WEBEZY_JSON)

            if args.expand:
                print_note('Creating resource in expanded mode')

            if args.verbose:
                print_note(WEBEZY_JSON._webezy_json, True, 'webezy.json')

            if hasattr(args, 'resource'):

                namespace = parse_namespace_resource(
                    args.resource, WEBEZY_JSON, args.parent)
                resource_name = f' [{args.name}]' if args.name is not None else ''
                
                print_info(
                    f"Generating new resource '{namespace[0]}'{resource_name}")

                results = inquirer.prompt(
                    namespace[1] if args.name is None else namespace[1][1:], theme=WebezyTheme())

                if results is None:
                    print_error('Must answer all questions')
                    exit(1)

                ARCHITECT = WebezyArchitect(
                    path=webezy_json_path,domain=WEBEZY_JSON.domain,project_name=WEBEZY_JSON.project['name'])
                if namespace[0] == 'package':
                    generate.package(results,WEBEZY_JSON,ARCHITECT,args.expand,args.verbose)
                
                elif namespace[0] == 'service':
                    generate.service(results,WEBEZY_JSON,ARCHITECT,args.expand,args.verbose)
                
                elif namespace[0] == 'message':
                    generate.message(results,WEBEZY_JSON,ARCHITECT,args.expand,args.verbose,args.parent)

                elif namespace[0] == 'rpc':
                    generate.rpc(results,WEBEZY_JSON,ARCHITECT,parent=args.parent)

                elif namespace[0] == 'enum':
                    generate.enum(results,WEBEZY_JSON,ARCHITECT,parent=args.parent)

                if args.build:
                    build.build_all(webezy_json_path)

            elif hasattr(args, 'source') and hasattr(args, 'target'):
                if args.remove:
                    pack.remove_import(args.source,args.target,webezy_json_path,WEBEZY_JSON)
                else:
                    pack.import_package(args.source,args.target,webezy_json_path,WEBEZY_JSON)
            
            elif args.undo:
                path = webezy_json_path.replace('webezy.json','.webezy/cache')
            
                cache_files = file_system.walkFiles(path)
                cache_files.sort()
                last_save = cache_files[len(cache_files)-2 if len(cache_files) > 1 else 1]
                print_note({'cache':cache_files,'action':'undo','active':last_save},pprint=True)
                
                # ARCHITECT = WebezyArchitect(
                    # path=webezy_json_path,save=last_save)
                # ARCHITECT.Save(undo_save=True)
            elif args.redo:
                path = webezy_json_path.replace('webezy.json','.webezy/cache')
            
                cache_files = file_system.walkFiles(path)
                cache_files.sort(reverse=True)
                logging.error(cache_files)
                # ARCHITECT = WebezyArchitect(
                #     path=webezy_json_path,save=cache_files[len(cache_files)-2 if len(cache_files) > 1 else 1])
                # ARCHITECT.Save()
            elif args.build:
                build.build_all(webezy_json_path)
            elif args.purge:
                temp_path = webezy_json_path.replace('webezy.json','.webezy/context.json')
                confirm =inquirer.prompt([inquirer.Confirm('confirm',False,message='You are about to purge the webezy context are you sure?')],theme=WebezyTheme())
                if confirm.get('confirm'):
                    file_system.removeFile(temp_path)
                    print_success("Purged webezy context !")
                else:
                    print_warning("Cancelling purge for webezy context")
            elif args.run_server:
                run.run_server(WEBEZY_JSON)

            elif hasattr(args, 'name'):
                resource = parse_name_to_resource(args.name,WEBEZY_JSON)
                type = resource.get('type')
                ARCHITECT = WebezyArchitect(
                    path=webezy_json_path,domain=WEBEZY_JSON.domain,project_name=WEBEZY_JSON.project['name'])
                if type == 'packages':
                    edit.edit_package(resource,args.action,WEBEZY_JSON,ARCHITECT)
                elif type == 'service':
                    edit.edit_service(resource,args.action,WEBEZY_JSON,ARCHITECT)
                elif type == 'descriptors':
                    kind = resource.get('kind')
                    if kind == resources.ResourceKinds.enum.value:
                        edit.edit_enum(resource,action=args.action,sub_action=args.sub_action,wz_json=WEBEZY_JSON,architect=ARCHITECT,expand=args.expand)
                    elif kind == resources.ResourceKinds.enum_value.value:
                        edit.edit_enum_value(resource,args.action,WEBEZY_JSON,ARCHITECT)
                    elif kind == resources.ResourceKinds.field.value:
                        edit.edit_field(resource,args.action,WEBEZY_JSON,ARCHITECT)
                    elif kind == resources.ResourceKinds.message.value:
                        edit.edit_message(resource=resource,action=args.action,sub_action=args.sub_action,wz_json=WEBEZY_JSON,architect=ARCHITECT,expand=args.expand)
                    elif kind == resources.ResourceKinds.method.value:
                        edit.edit_rpc(resource=resource,action=args.action,sub_action=args.sub_action,wz_json=WEBEZY_JSON,architect=ARCHITECT,expand=args.expand)
            else:
                if hasattr(args, 'full_name'):
                    if args.full_name is None:
                        if hasattr(args, 'type'):
                            ls.list_by_resource(args.type,WEBEZY_JSON)
                    else:
                        ls.list_by_name(args.full_name,WEBEZY_JSON)
                
        else:
            print_warning(
                'Not under valid webezyio project !\n\tMake sure you are on the root directory of your project')

def parse_name_to_resource(full_name,wz_json: helpers.WZJson):
    resource = None
    print(len(full_name.split('.')))
    if len(full_name.split('.')) > 4:
        log.debug("Searching for fields / enum values")
        # Field / Enum Value
        pkg_name = full_name.split('.')[1]
        pkg_v = full_name.split('.')[2]
        pkg_path = f'protos/{pkg_v}/{pkg_name}.proto'
        if wz_json.packages[pkg_path].get('messages') is not None:
            msg_name = '.'.join(full_name.split('.')[:-2])
            search_msg = next((m for m in wz_json.packages[pkg_path].get('messages') if m.get('fullName') == msg_name),None)
            if search_msg is not None:
                search_field = next((f for f in search_msg if f.get('fullName') == full_name), None)
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
        print_error(f'Couldnt find any resource by the name -> {full_name}')
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
            inquirer.Text("rpc", message="Enter rpc name",
                          validate=validation),    
            inquirer.List("type", message="Choose message type", choices=[('Unary', (False, False)), (
                'Client stream', (True, False)), ('Server stream', (False, True)), ('Bidi stream', (True, True))]),
        ]
        if has_service == False:
            wz_g_r_q.append(inquirer.List(
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
            inquirer.Text("message", message="Enter message name",
                          validate=validation),
        ]

        if has_package == False:
            wz_g_m_q.append(inquirer.List(
            "package", message="Choose a package to attach the message", choices=temp_p))

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
            wz_g_e_q.append(inquirer.List('package','Choose a package',choices=temp_p))

        questions = wz_g_e_q

    return namespace, questions
