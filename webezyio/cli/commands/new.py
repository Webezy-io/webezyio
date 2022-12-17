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

import logging
import subprocess
from typing import List, Literal
from webezyio.cli.prompter import QCheckbox,QConfirm,QList,QText,ask_user_question
from webezyio.cli.theme import WebezyTheme
from webezyio.commons import file_system,protos
from webezyio.commons.helpers import WZEnumValue, WZField,_BUILTINS_TEMPLATES
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success
from webezyio.commons.file_system import join_path,mkdir
from webezyio.architect import WebezyArchitect
import os
import inquirer
from inquirer import errors

_TEMPLATES = _BUILTINS_TEMPLATES

def validate_client(answers, current):
    if len(current) ==0:
        raise errors.ValidationError(current,"Must chose at least 1 client !")
    return True

def validate_domain(answers, current):
    if '.' in current:
        raise errors.ValidationError(current,"Domain name MUST not include suffix like '.com' / '.io' and so on.")
    return True

wz_new_q = [
    QList(name="server", message="Choose server language", choices=[
                  ('Python', protos.python), ('Typescript', protos.typescript), ('Go', protos.go)], default=protos.python),
    QCheckbox(name="clients", message="Choose clients languages (Use arrows keys to enable disable a language)", choices=[
                      ('Python', protos.python), ('Typescript', protos.typescript), ('Go',protos.go), ('Webpack-js',protos.webpack)], default=[protos.python],validate=validate_client),
    QText(name="domain", message="Enter domain name", default='domain',validate=validate_domain),
]

def create_new_project(project_name:str,path:str=None,host:str=None,port:int=None,server_language:str=None,clients=[],domain:str=None,template:_TEMPLATES='@webezyio/Blank'):

    domain_name = 'domain'

    if server_language is None and clients == None and domain is None:
        results = ask_user_question(questions=wz_new_q)
    
        if results is None:
            print_warning("Must answer project creation questions")
            exit(1)
    else:
        results = {}
        results['server'] = server_language
        results['clients'] = clients
        results['domain'] = domain

    if path is None:
        try:
            root = os.getcwd()
            result_path = inquirer.prompt([inquirer.Path('root_dir', default=join_path(
                root, project_name), message="Enter a root dir path", exists=False)], theme=WebezyTheme())
            if result_path is not None:
                result_path = result_path['root_dir']
        except Exception:
            print_error(
                f"Error root dir exists\n[{join_path(root,project_name)}]")
            exit(1)
    else:
        result_path = join_path(path, project_name)

    clients = []
    for k in results:
        if k == 'server':
            if type(results[k]) == str:
                server_langugae = results[k]
            else:
                server_langugae = protos.WebezyLanguage.Name(results[k])
            print_info(f'Server language: {server_langugae}')
        if k == 'clients':
            for c in results[k]:
                if type(c) == str:
                    client_lang = c
                else:
                    client_lang = protos.WebezyLanguage.Name(c)
                out_dir = join_path(
                    result_path, 'clients', client_lang)
                print_info(f'Adding client: {client_lang}\n\t-> {out_dir}')
                clients.append(
                    {'out_dir': out_dir, 'language': client_lang})
        if k == 'domain':
            domain_name = results[k]

    out_dir = join_path(
                    result_path, 'clients',results['server'] if type(results['server']) == str else protos.WebezyLanguage.Name(results['server']))
    if next((c for c in clients if c.get('language') == (results['server'] if type(results['server']) == str else protos.WebezyLanguage.Name(results['server'])) ),None) is None:
        print_warning('Auto-Adding client {} - Any project by default is assigned with client in the server specified language !'.format(protos.WebezyLanguage.Name(results['server']) if type(results['server']) != str else results['server'] ))
        clients.append({'out_dir': out_dir, 'language': protos.WebezyLanguage.Name(results['server']) if type(results['server']) != str else results['server'] })
    root_dir = result_path
    webezy_json_path = join_path(root_dir, 'webezy.json')
    mkdir(result_path)

    ARCHITECT = WebezyArchitect(
        path=webezy_json_path, domain=domain_name, project_name=project_name)
    if template != '@webezyio/Blank':
        print_info(webezy_json_path)
        print_info(f'Creating new webezy project "{project_name}" [{template}]')
        attach_template(ARCHITECT,template)
        print_success(
        f'Success !\n\tCreated new project "{project_name}" from [{template}] template\n\t-> cd {root_dir}\n\t-> And then continue developing your awesome services !\n\t-> For more info on how to use the webezy.io CLI go to https://www.webezy.io/docs')
        # ARCHITECT = WebezyArchitect(
            # path=webezy_json_path, domain=domain_name, project_name=project_name)
        # ARCHITECT.AddProject(server_language=server_langugae, clients=clients)
        # ARCHITECT.AddProject(server_language=server_langugae, clients=clients)
        # ARCHITECT.SetDomain(domain_name)
        exit(1)

    ARCHITECT.AddProject(server_language=server_langugae, clients=clients)
    ARCHITECT.SetDomain(domain_name)
    ARCHITECT.SetConfig({'host': host, 'port': int(port), 'deployment': protos.DeploymentType.Name(protos.LOCAL) })

    ARCHITECT.Save()
    
    print_success(
        f'Success !\n\tCreated new project "{project_name}"\n\t-> cd {root_dir}\n\t-> And then continue developing your awesome services !\n\t-> For more info on how to use the webezy.io CLI go to https://www.webezy.io/docs')

def attach_template(ARCHITECT:WebezyArchitect,template:_TEMPLATES):
    if template != '@webezyio/Blank':
        file_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        template_domain_name = template.split('/')[0].split('@')[-1]
        template_name = template.split('/')[-1]
        print(file_dir + '/commons/templates/{0}/{1}.template.py'.format(template_domain_name,template_name))
        print(file_system.get_current_location())
        os.chdir(ARCHITECT._path.split('webezy.json')[0])
        print(file_system.get_current_location())

        subprocess.run(['python',file_dir + '/commons/templates/{0}/{1}.template.py'.format(template_domain_name,template_name),'--project-name',ARCHITECT._project_name])
    # if template == '@webezyio/Sample':

    #     pkg = ARCHITECT.AddPackage('SamplePackage',[],[],'This is a sample package to be used in "SampleService"')

    #     _SAMPLE_MSG_FIELDS = [
    #         WZField('SampleString','TYPE_STRING','LABEL_OPTIONAL',None,None,None,'This is a sample field under "SampleMessage" which expect string value').to_dict(),
    #         WZField('SampleBool','TYPE_BOOL','LABEL_OPTIONAL',None,None,None,'This is a sample field under "SampleMessage" which expect boolean value').to_dict(),
    #         WZField('SampleInt','TYPE_INT32','LABEL_OPTIONAL',None,None,None,'This is a sample field under "SampleMessage" which expect int32 value').to_dict(),
    #         WZField('SampleFloat','TYPE_FLOAT','LABEL_OPTIONAL',None,None,None,'This is a sample field under "SampleMessage" which expect float value').to_dict(),
    #         WZField('StringArray','TYPE_STRING','LABEL_REPEATED',None,None,None,'This is a list/array field under "SampleMessage" which expect strings values').to_dict()
    #     ]
    #     msg = ARCHITECT.AddMessage(pkg,'SampleMessage',_SAMPLE_MSG_FIELDS,'This is a sample message')

    #     _ENUM_VALUES = [
    #         WZEnumValue(name='UNKNOWN',number=0,description='This is the default enum value which should be ignored when passed to server / client').to_dict(),
    #         WZEnumValue(name='SOME_VALUE',number=1).to_dict(),
    #         WZEnumValue(name='OTHER_VALUE',number=2).to_dict()
    #     ]
        
    #     enm = ARCHITECT.AddEnum(pkg,'SampleEnum',_ENUM_VALUES,'This is Enum type to be used as field type')
        
    #     _SAMPLE_MSG_FIELDS = [
    #         WZField('NestedMessage','TYPE_MESSAGE','LABEL_OPTIONAL',msg.full_name,None,None,'This is a nested message field which expect "{0}" value'.format(msg.full_name)).to_dict(),
    #         WZField('SampleEnum','TYPE_ENUM','LABEL_OPTIONAL',None,enm.full_name,None,'This is a enum field which expect "{0}" value'.format(enm.full_name)).to_dict(),
    #     ]

    #     msg_1 = ARCHITECT.AddMessage(pkg,'ComplexMessage',_SAMPLE_MSG_FIELDS,'This is a more complex message structure including nested fields and enums')

    #     svc = ARCHITECT.AddService(name='SampleService',methods=[],description='This is a sample service',dependencies=[pkg.package])
    #     ARCHITECT.AddRPC(svc, 'SampleUnary', [
    #                     (False, msg.full_name), (False, msg_1.full_name)], 'This is a sample unary RPC call')
    #     ARCHITECT.AddRPC(svc, 'SampleClientStream', [
    #                     (True, msg.full_name), (False, msg_1.full_name)], 'This is a sample client stream RPC call')
    #     ARCHITECT.AddRPC(svc, 'SampleServerStream', [
    #                     (False, msg.full_name), (True, msg_1.full_name)], 'This is a sample server stream RPC call')
    #     ARCHITECT.AddRPC(svc, 'SampleBidiStream', [
    #                     (True, msg.full_name), (True, msg_1.full_name)], 'This is a sample bidi-stream RPC call')
