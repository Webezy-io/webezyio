import logging
from webezyio.cli.theme import WebezyTheme
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success
from webezyio.commons.file_system import join_path,mkdir
from webezyio.commons.protos.webezy_pb2 import Language
from webezyio.architect import WebezyArchitect
import os
import inquirer
from inquirer import errors

def validate_client(answers, current):
    if len(current) ==0:
        raise errors.ValidationError(current,"Must chose at least 1 client !")
    return True

def validate_domain(answers, current):
    if '.' in current:
        raise errors.ValidationError(current,"Domain name MUST not include suffix like '.com' / '.io' and so on.")
    return True

wz_new_q = [
    inquirer.List("server", message="Choose server language", choices=[
                  ('Python', Language.python), ('Typescript', Language.typescript)], default=Language.python),
    inquirer.Checkbox("clients", message="Choose clients languages (Use arrows keys to enable disable a language)", choices=[
                      ('Python', Language.python), ('Typescript', Language.typescript)], default=[Language.python],validate=validate_client),
    inquirer.Text("domain", message="Enter domain name", default='domain',validate=validate_domain),
]

def create_new_project(project_name:str,path:str=None,host:str=None,port:int=None):

    domain_name = 'domain'
    print_info(f'Creating new webezy project "{project_name}"')
    results = inquirer.prompt(wz_new_q, theme=WebezyTheme())
    
    if results is None:
        print_warning("Must answer project creation questions")
        exit(1)
    
    if path is not None:
        result_path = inquirer.prompt([inquirer.Path(
            'root_dir', default=path, message="Enter a root dir path", exists=False)], theme=WebezyTheme())
    else:
        try:
            root = os.getcwd()
            result_path = inquirer.prompt([inquirer.Path('root_dir', default=join_path(
                root, project_name), message="Enter a root dir path", exists=False)], theme=WebezyTheme())
        except Exception:
            print_error(
                f"Error root dir exists\n[{join_path(root,project_name)}]")
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

    out_dir = join_path(
                    result_path['root_dir'], 'clients', Language.Name(results['server']))
    if next((c for c in clients if c.get('language') == Language.Name(results['server']) ),None) is None:
        clients.append({'out_dir': out_dir, 'language': results['server']})
    root_dir = result_path['root_dir']
    webezy_json_path = join_path(root_dir, 'webezy.json')
    mkdir(result_path['root_dir'])

    ARCHITECT = WebezyArchitect(
        path=webezy_json_path, domain=domain_name, project_name=project_name)

    ARCHITECT.AddProject(server_language=server_langugae, clients=clients)

    ARCHITECT.SetConfig({'host': host, 'port': port})

    ARCHITECT.Save()
    
    print_success(
        f'Success !\n\tCreated new project "{project_name}"\n\t-> cd {root_dir}\n\t-> And then continue developing your awesome services !\n-> For more info on how to use the webezy.io CLI go to https://www.webezy.io/docs')


