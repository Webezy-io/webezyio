import logging
import argparse
import os
from webezyio import __version__
import inquirer
from inquirer.themes import Theme, term
from inquirer import errors
import re

from webezyio.architect import WebezyArchitect
from webezyio.commons import helpers
from webezyio.commons import file_system
from webezyio.commons.errors import WebezyProtoError
from webezyio.commons.pretty import print_info, print_note, print_version, print_success, print_warning, print_error
from webezyio.commons.protos.webezy_pb2 import FieldDescriptor, Language
from webezyio.commons.file_system import join_path, mkdir, rFile


def field_exists_validation(new_field, fields, msg):
    if new_field in fields:
        raise WebezyProtoError(
            'Message', f'Field {new_field} already exits under {msg}')
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
    return True


log = logging.getLogger(__name__)


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


class WebezyTheme(Theme):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.cyan
        self.Question.brackets_color = term.cyan
        self.Question.default_color = term.cyan
        self.Checkbox.selection_color = term.bold_black_on_bright_cyan
        self.Checkbox.selection_icon = "❯"
        self.Checkbox.selected_icon = "◉"
        self.Checkbox.selected_color = term.cyan
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = "◯"
        self.List.selection_color = term.bold_black_on_bright_cyan
        self.List.selection_cursor = "❯"
        self.List.unselected_color = term.normal


wz_new_q = [
    inquirer.List("server", message="Choose server language", choices=[
                  ('Python', Language.python), ('Typescript', Language.typescript)], default=Language.python),
    inquirer.Checkbox("clients", message="Choose clients languages", choices=[
                      ('Python', Language.python), ('Typescript', Language.typescript)], default=[Language.python]),
    inquirer.Text("domain", message="Enter domain name", default='domain'),
]

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
    # print('\n', 'Webezy.io CLI Started', '\n\n')
    # Main cli parser
    parser = argparse.ArgumentParser(prog='webezy',
                                     description='Command line interface for the webezyio package build awesome gRPC micro-services. For more information please visit https://www.webezy.io there you can find additional documentation and tutorials.',
                                     epilog=f'For more information see - https://www.webezy.io/docs/cli | Created with love by Amit Shmulevitch. 2022 © webezy.io [{__version__.__version__}]')

    # Instantiating sub parsers object
    subparsers = parser.add_subparsers(
        help='Main modules to interact with Webezy CLI.')

    parser_new = subparsers.add_parser('new', help='Create new project')
    parser_new.add_argument('project', help='Project name')
    parser_new.add_argument('-p', '--path', required=False,
                            help='Path for the project root directory')
    parser_new.add_argument('--port', default=50051,
                            required=False, help='Port server will run on')
    parser_new.add_argument('--host', default='localhost',
                            required=False, help='Host name for server')

    parser_n = subparsers.add_parser('n', help='A shortend for new commands')
    parser_n.add_argument('project', help='Project name')
    parser_n.add_argument('-p', '--path', required=False,
                          help='Path for the project root directory')

    parser_generate = subparsers.add_parser(
        'generate', help='Generate resources commands')
    parser_generate.add_argument('resource', choices=[
                                 'service', 'package', 'message', 'rpc', 'enum'], help='Generate a webezyio resource from specific resource type')
    parser_generate.add_argument('-n', '--name', help='Name for the resource')
    parser_g = subparsers.add_parser(
        'g', help='A shortend for generate commands')
    parser_g.add_argument('resource', choices=[
                          's', 'p', 'm', 'r', 'e'], help='Generate a webezyio resource from specific resource type, for e.x "s" stands for "service"')
    parser_g.add_argument('-n', '--name', help='Name for the resource')

    parser_list = subparsers.add_parser('ls', help='List resources commands')
    parser_list.add_argument(
        'fullName', help='Display a resource report for specific resoource by passing in a full name, for e.x domain.test.GetTest will return "GetTest" (RPC) which under "test" (service)')
    parser_list.add_argument('-r', '--resource', choices=['service', 'package', 'message',
                             'rpc', 'enum'], help='List a webezyio resource from specific resource type')

    parser_build = subparsers.add_parser(
        'build', help='Build project commands')
    parser_build.add_argument('-t', '--type', required=False, choices=[
                              'code', 'protos', 'all'], default='all', help='Build webezyio project for a specific type')

    parser_build = subparsers.add_parser(
        'config', help='Edit webezyio global configs or edit your own project configs')
    parser.add_argument('-v', '--version', action='store_true',
                        help='Display webezyio current installed version')

    parser_pkg = subparsers.add_parser(
        'package', help='Attach a package into other services / package')
    parser_pkg.add_argument('source', help='Package full name')
    parser_pkg.add_argument('target', help='Package path or service name')

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

    # parser.add_argument(
    #     '--help', action="store_true", help='Log level',
    #     )

    # Parse all command line arguments
    args = parser.parse_args(args)
    log.setLevel(args.loglevel)

    log.debug(args)

    # Logging version
    if args.version:
        print_version(__version__.__version__)

    if hasattr(args, 'project'):
        domain_name = 'domain'
        print_info(f'Creating new webezy project "{args.project}"')
        results = inquirer.prompt(wz_new_q, theme=WebezyTheme())
        if results is None:
            print_warning("Must answer project creation questions")
            exit(1)
        if args.path is not None:
            result_path = inquirer.prompt([inquirer.Path(
                'root_dir', default=args.path, message="Enter a root dir path", exists=False)], theme=WebezyTheme())
        else:
            try:
                root = os.getcwd()
                result_path = inquirer.prompt([inquirer.Path('root_dir', default=join_path(
                    root, args.project), message="Enter a root dir path", exists=False)], theme=WebezyTheme())
            except Exception:
                print_error(
                    f"Error root dir exists\n[{join_path(root,args.project)}]")
                exit(1)

        clients = []

        for k in results:
            if k == 'server':
                server_langugae = Language.Name(results[k])
                print_info(f'Server language: {server_langugae}')
            if k == 'clients':
                for c in results[k]:
                    client_lang = Language.Name(c)
                    out_dir = join_path(
                        result_path['root_dir'], 'clients', client_lang)
                    print_info(f'Adding client: {client_lang}')
                    clients.append(
                        {'out_dir': out_dir, 'language': client_lang})
            if k == 'domain':
                domain_name = results[k]
        # Init Builder
        root_dir = result_path['root_dir']
        webezy_json_path = join_path(root_dir, 'webezy.json')
        mkdir(result_path['root_dir'])
        ARCHITECT = WebezyArchitect(
            path=webezy_json_path, domain=domain_name, project_name=args.project)

        ARCHITECT.AddProject(server_language=server_langugae, clients=clients)
        ARCHITECT.SetConfig({'host': args.host, 'port': args.port})

        ARCHITECT.Save()
        print_success(
            f'Success !\n\tCreated new project "{args.project}"\n\t-> cd {root_dir}\n')

    else:
        if helpers.check_if_under_project():
            webezy_json_path = join_path(os.getcwd(), 'webezy.json')
            WEBEZY_JSON = rFile(webezy_json_path, json=True)
            WEBEZY_JSON = helpers.WZJson(webezy_json=WEBEZY_JSON)
            prj_name = WEBEZY_JSON.project['name']

            if args.verbose:
                print_note(WEBEZY_JSON._webezy_json, True, 'webezy.json')

            if hasattr(args, 'resource'):

                namespace = parse_namespace_resource(
                    args.resource, WEBEZY_JSON)
                resource_name = f' [{args.name}]' if args.name is not None else ''
                print_info(
                    f"Generating new resource '{namespace[0]}'{resource_name}")

                results = inquirer.prompt(
                    namespace[1] if args.name is None else namespace[1][1:], theme=WebezyTheme())

                if results is None:
                    print_error('Must answer all questions')
                    exit(1)

                ARCHITECT = WebezyArchitect(
                    path=webezy_json_path)

                if namespace[0] == 'package':
                    pkg = results['package']
                    if WEBEZY_JSON.packages is not None:
                        try:
                            if WEBEZY_JSON.get_package(pkg):
                                print_error(
                                    f'Package [{pkg}] is already defined under "{prj_name}" project')
                                exit(1)
                        except Exception:
                            log.debug("Package not found continuing...")
                    ARCHITECT.AddPackage(pkg, [])
                    ARCHITECT.Save()
                    print_success(f'Success !\n\tCreated new package "{pkg}"')
                elif namespace[0] == 'service':
                    svc = results['service']
                    ARCHITECT.AddService(namespace[0], [], None)
                    ARCHITECT.Save()
                    print_success(f'Success !\n\tCreated new service "{svc}"')
                elif namespace[0] == 'message':

                    msg_name = results['message']
                    pkg = results['package']
                    msg_full_name = '{0}.{1}'.format(pkg, msg_name)

                    add_field = True
                    temp_fields = []
                    msg_fields = []
                    package = WEBEZY_JSON.get_package(pkg.split('.')[1], False)
                    avail_msgs = []
                    for msg in package.messages:
                        avail_msgs.append((msg.name, msg.full_name))
                    avail_enums = []
                    for enum in package.enums:
                        avail_enums.append((enum.name, enum.full_name))
                    for d in package.dependencies:
                        if 'google.protobuf' in d:
                            # WEBEZY_JSON.get_package()
                            ext_msg_pkg = '.'.join(d.split('.')[:-1])
                            avail_msgs.append(
                                (d.split('.')[-1], '{0}.{1}'.format(ext_msg_pkg, d.split('.')[-1].capitalize())))
                        else:
                            d_package = WEBEZY_JSON.get_package(
                                d.split('.')[1])
                            for msg in d_package.messages:
                                avail_msgs.append((msg.name, msg.full_name))

                    while add_field == True:

                        opt = []
                        for f in fields_opt:
                            opt.append((f.split('_')[1].lower(), f))
                        labels = []

                        for l in field_label:
                            labels.append((l.split('_')[1].lower(), l))
                        field = inquirer.prompt([
                            inquirer.Text(
                                'field', 'Choose field name', validate=validation),
                            inquirer.List(
                                'fieldLabel', 'Choose field label', choices=labels),
                            inquirer.List(
                                'fieldType', 'Choose field type', choices=opt),
                        ], theme=WebezyTheme())

                        message_type = None
                        enum_type = None

                        if field['fieldType'] == FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_MESSAGE):
                            message = inquirer.prompt([
                                inquirer.List(
                                    'message', 'Choose available messages', choices=avail_msgs)
                            ], theme=WebezyTheme())
                            message_type = message['message']

                        elif field['fieldType'] == FieldDescriptor.Type.Name(FieldDescriptor.Type.TYPE_ENUM):
                            message = inquirer.prompt([
                                inquirer.List(
                                    'enum', 'Choose available enums', choices=avail_enums)
                            ], theme=WebezyTheme())
                            enum_type = message['enum']

                        if field is None:
                            add_field = False
                        else:
                            new_field = field['field']
                            field_exists_validation(
                                new_field, temp_fields, msg_full_name)
                            temp_fields.append(new_field)
                            msg_fields.append(helpers.WZField(
                                new_field, field['fieldType'], field['fieldLabel'], message_type=message_type, enum_type=enum_type).to_dict())
                            nextfield = inquirer.prompt([
                                inquirer.Confirm(
                                    'continue', message='Add more fields?', default=True)
                            ], theme=WebezyTheme())
                            if nextfield is None:
                                add_field = False
                            else:
                                if nextfield['continue'] == False:
                                    add_field = False

                        if args.verbose:
                            print_note(field, True, 'Added field')

                    ARCHITECT.AddMessage(WEBEZY_JSON.get_package(pkg.split('.')[1], False), msg_name,
                                         msg_fields, 'description', None)
                    ARCHITECT.Save()

                elif namespace[0] == 'rpc':
                    rpc = results['rpc']
                    svc = results['service']
                    full_name = '{0}.{1}'.format(svc, rpc)

                    if WEBEZY_JSON.get_rpc(full_name) is not None:
                        print_error(
                            f'RPC [{rpc}] is already defined under "{svc}" service')
                        exit(1)

                    dependencies = WEBEZY_JSON.services[svc.split(
                        '.')[1]].get('dependencies')

                    if dependencies is None:
                        print_error(
                            f'Dependencies not listed under "{svc}"\n\tTry attache first a packge to service')
                        exit(1)

                    avail = []
                    for d in dependencies:
                        pkg = WEBEZY_JSON.get_package(d.split('.')[1])
                        msgs = pkg.get('messages')
                        if msgs is not None:
                            for m in msgs:
                                avail.append(m['fullName'])
                    if len(avail) == 0:
                        print_error('Messages not listed under packages')
                        exit(1)

                    inputs_outputs = inquirer.prompt([
                        inquirer.List(
                            "input_type", message="Choose the input type", choices=avail),
                        inquirer.List(
                            "output_type", message="Choose the output type", choices=avail),
                    ])
                    if inputs_outputs is None:
                        print_error('IN/OUT Types are required for RPC')
                        exit(1)

                    ARCHITECT.AddRPC(WEBEZY_JSON.get_service(svc.split('.')[1], False), rpc, [
                                     (results['type'][0], inputs_outputs['input_type']), (results['type'][1], inputs_outputs['output_type'])], None)
                    ARCHITECT.Save()

                elif namespace[0] == 'service':
                    pass
                elif namespace[0] == 'enum':
                    pass
            elif hasattr(args, 'source') and hasattr(args, 'target'):
                importing_into_pkg = False
                old_pkg = None
                old_svc = None
                ARCHITECT = WebezyArchitect(
                    path=webezy_json_path)

                if len(args.target.split('.')) > 2:
                    importing_into_pkg = True
                    old_pkg = WEBEZY_JSON.get_package(
                        args.target('/')[-1].split('.')[0])
                    dep = []
                    if old_pkg.get('dependencies') is not None:
                        dep = old_pkg.get('dependencies')
                        if args.source not in old_pkg.get('dependencies'):
                            dep = old_pkg.get('dependencies')
                            dep.append(args.source)
                        else:
                            print_warning(
                                f"Package '{args.source}' already injected into '{args.target}' package")
                            exit(1)
                    else:
                        dep.append(args.source)

                    ARCHITECT.AddPackage(pkg, dep)

                else:
                    dep = []
                    old_svc = WEBEZY_JSON.get_service(args.target)
                    if old_svc.get('dependencies') is not None:
                        dep = old_svc.get('dependencies')
                        if args.source not in old_svc.get('dependencies'):
                            dep = old_pkg.get('dependencies')
                            dep.append(args.source)
                        else:
                            print_warning(
                                f"Package '{args.source}' already injected into '{args.target}' service")
                            exit(1)
                    else:
                        dep.append(args.source)

                    ARCHITECT.AddService(old_svc.get('name'), dep, None)
                    ARCHITECT.Save()

                importing_into_pkg = 'package' if importing_into_pkg == True else 'service'
                print_info(
                    f"Attaching package '{args.source}' -> '{args.target}' {importing_into_pkg}")
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
            else:
                parser.print_help()
        else:
            print_warning(
                'Not under valid webezyio project !\n\tMake sure you are on the root directory of your project')


def parse_namespace_resource(name, wz_json: helpers.WZJson):
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

        wz_g_r_q = [
            inquirer.Text("rpc", message="Enter rpc name",
                          validate=validation),
            inquirer.List(
                "service", message="Choose a service to attach the rpc", choices=temp_s),
            inquirer.List("type", message="Choose message type", choices=[('Unary', (False, False)), (
                'Client stream', (True, False)), ('Server stream', (False, True)), ('Bidi stream', (True, True))]),
        ]
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
            temp_p.append((packages[pkg]['name'], packages[pkg]['package']))

        wz_g_m_q = [
            inquirer.Text("message", message="Enter message name",
                          validate=validation),
            inquirer.List(
                "package", message="Choose a package to attach the message", choices=temp_p),
        ]

        questions = wz_g_m_q

    elif namespace == 'e':
        namespace = 'enum'
        questions = wz_g_e_q

    return namespace, questions
