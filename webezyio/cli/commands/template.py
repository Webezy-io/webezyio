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

import os
import subprocess
from webezyio.architect import WebezyArchitect
from webezyio.cli import theme
from webezyio.commons import file_system
from webezyio.commons.helpers import WZJson,MessageToDict
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success
import zlib

from webezyio.commons.protos.WebezyConfig_pb2 import WebezyConfig

_OPEN_BRCK = '{'
_CLOSING_BRCK = '}'

def parse_wz_json():
    pass

def create_webezy_template_py(wz_json:WZJson,include_code:bool,prj_configs:WebezyConfig):
    
    opt_template = prj_configs.template
    opts = None
    if opt_template is None or opt_template.name =='':
        print_warning("Couldnt find any 'WebezyTemplate.TemplateConfig' object at: webezy.json | config.py files")
    else:
        # opts = ',\n\t- '.join(str((k,opt_template[k])) for k in opt_template)
        opts = prj_configs.template
    host = prj_configs.host
    port = prj_configs.port
    project_pkg_name = wz_json.project['packageName'] if prj_configs.template is None else  prj_configs.template.name
    project_name = wz_json.project['name'] if prj_configs.template is None else  prj_configs.template.name
    clients = wz_json.project.get('clients')
    description = prj_configs.template.description if prj_configs.template is not None else ''
    messages = []
    enums = []
    includes = None
    excludes = None
    root_path = wz_json.path.split('webezy.json')[0]
    author = prj_configs.template.author if  prj_configs.template is not None else 'Unknown'
    if include_code:
        includes = [] if prj_configs.template is None or prj_configs.template.include is None else prj_configs.template.include
        excludes = [] if prj_configs.template is None or prj_configs.template.exclude is None else prj_configs.template.exclude
    for pkg in wz_json.packages:
        p = wz_json.packages[pkg]
        for m in p.get('messages'):
            messages.append(m)
        if p.get('enums') is not None:
            for e in p.get('enums'):
                enums.append(e)
    print_info("Generating template from [{0}] project:\n\t- {1}".format(wz_json.project.get('name'),opts))
    return f'{create_init(project_pkg_name,description,author)}{create_constants(host=host,port=port,project_name=project_name,domain=wz_json.domain,server_language=wz_json.get_server_language())}{create_clients(clients)}{add_project()}{create_enums_values(enums)}{create_enums(enums)}{create_fields(messages)}{create_msgs(messages)}{create_pckgs(wz_json.packages)}{add_packgs(wz_json.packages)}{add_msgs(wz_json.packages)}{add_enums(wz_json.packages)}{create_rpcs(wz_json.services)}{create_services(wz_json.services)}{add_services(wz_json.services)}{add_rpcs(wz_json.services)}{create_file_context(root_path,include=includes,exclude=excludes) if include_code else ""}{save_architect()}'

def create_init(project_name:str='webezy.io',description=None,author=None):
    return """
\"\"\"Init script for webezy.io template {0}
Generated thanks to -
{1}
{2}

Author: {3}
\"\"\"
# Main webezyio class to create gRPC services programmatically
# (Same inteface that webezyio cli is built as wrapper for
# WebezyArchitect whenever you generate new resource / create new project)
from webezyio.architect import WebezyArchitect

# Some common utils modules to help us build the services faster
# and adds an validations to object before they created
from webezyio.commons import helpers, file_system

# Webezy proto modules also helps us here to construct our services
# gRPC used to create another gRPC ! :)
from webezyio.commons.protos import WebezyLanguage, WebezyContext, WebezyFileContext

# Default system imports
import os
import sys
import argparse
import zlib

    """.format(project_name,theme.logo_ascii_art,description if description is not None else '',author)

def create_constants(domain, project_name, server_language:str='python', host:str = 'localhost', port:int = 50051):
    return f"""
\"\"\"Initialize constants and WebezyArchitect class\"\"\"
parser = argparse.ArgumentParser(
                    prog = '{project_name}',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')
parser.add_argument('--domain',default='{domain}')           # optional argument
parser.add_argument('--project-name',default='{project_name}')           # optional argument

args = parser.parse_args()

# Constants
_PATH = file_system.join_path(os.getcwd(), 'webezy.json') 
_DOMAIN = args.domain
_PROJECT_NAME = args.project_name
_SERVER_LANGUAGE = WebezyLanguage.Name(WebezyLanguage.{server_language})
_HOST = '{host}'
_PORT = {port}

# Initializing WebezyArchitect class which we going to interact with
# It is used to create all of our 'webezyio' resources
_architect = WebezyArchitect(path=_PATH,
                             domain=_DOMAIN,
                             project_name=_PROJECT_NAME)
_architect.SetConfig({_OPEN_BRCK}'host': _HOST, 'port': _PORT{_CLOSING_BRCK})
_architect.SetDomain(_DOMAIN)
    
\"\"\"Project specific configurations\"\"\"
    """

def create_clients(clients):
    temp_clients = []
    langauges = []
    for c in clients:
        temp_clients.append({'language':c['language'],'out_dir':'file_system.join_path(_PATH, \'clients\', WebezyLanguage.Name(WebezyLanguage.{0}))'.format(c['language'])})
        langauges.append(c['language'])
    return """
# Init all the client to be used with your services
# Here we configured a {1} clients to be created with our services    
_clients = {0}
    """.format(temp_clients,' + '.join(langauges)).replace('"','')


def add_project():
    return """
# Adding the base project data
_project = _architect.AddProject(server_language=_SERVER_LANGUAGE,
                                 clients=_clients)

# NOTE - that every call to WebezyArchitect executions
# it will return the proto generated class of that object
# which can be used to enrich the webezy base structure
# or debug easly whats going on beneath the surface
# print(type(_project))
# <class 'webezy_pb2.Project'>

    """

def create_enums_values(enums):
    if enums is not None:
        code = ''
        for e in enums:
            temp_enum_values = []
            for ev in e.get('values'):
                temp_enum_values.append('helpers.WZEnumValue(\'{0}\',{1},description=\'{2}\')'.format(ev.get('name'),ev.get('number') if ev.get('number') is not None else 0,ev.get('description')))
            code += '\n# Instantiating all enum values for [{0}]\n_enum_values_{0} = [{1}]'.format(e.get('fullName').replace('.','_'),',\n\t'.join(temp_enum_values))
    
        return """
# Creating enums values
{0}
        """.format(code)
    else:
        return "\n"

def create_enums(enums):
    if enums is not None:
        code = ''
        for e in enums:
            code += '\n# Constructing enum [{0}]\n_enum_{0} = helpers.WZEnum(\'{1}\',enum_values=_enum_values_{0})'.format(e.get('fullName').replace('.','_'),e.get('name')) 
        return """
# Creating enums   
{0} 
        """.format(code)
    else:
        return "\n"

def create_fields(messages):
    fields = {}
    for m in messages:
        
        fields[m.get('fullName')] = []
        for f in  m.get('fields'):
            temp_msg_type = f.get('messageType')
            if temp_msg_type is not None:
                if 'google' not in temp_msg_type:
                    temp_msg_type = '_DOMAIN + \'.{}\''.format('.'.join(temp_msg_type.split('.')[1:]))
                else:
                    temp_msg_type = '\'{}\''.format(temp_msg_type)
            field = '\n# Constructing a field for [{4}]\n_field_{4} = helpers.WZField(name=\'{0}\',\n\
                              description=\'{1}\',\n\
                              label=\'{2}\',\n\
                              type=\'{3}\',\n\
                              message_type={6},\n\
                              enum_type={5},\n\
                              key_type={7},\n\
                              value_type={8},\n\
                              oneof_fields=None, # Not supporting templating with oneof_fields !\n\
                              extensions={9})\n'.format(
                                  f.get('name'),
                                  str(f.get('description')).replace("'",'"'),
                                  f.get('label'),
                                  f.get('fieldType'),
                                  f.get('fullName').replace('.','_'),
                                  '_DOMAIN+\'.{}\''.format('.'.join(f.get('enumType').split('.')[1:])) if f.get('enumType') is not None else None,
                                  '{}'.format(temp_msg_type),
                                  '\'{0}\''.format(f.get('keyType')) if f.get('keyType') is not None else None,
                                  '\'{0}\''.format(f.get('valueType')) if f.get('valueType') is not None else None,
                                  f.get('extensions'))
            fields[m.get('fullName')].append((f.get('fullName').replace('.','_'),field))

    code = ''

    for k in fields:
        msg = k
        msg_fields = []
        for f in fields[msg]:
            msg_fields.append(f[1])
        code += ''.join(msg_fields)
    for m in messages:
        temp_fields = []
        for f in m.get('fields'):
            temp_fields.append('_field_{0}'.format(f.get('fullName').replace('.','_')))
        code += '\n# Packing all fields for [{0}]\n_msg_fields_{0} = [{1}]'.format(m.get('fullName').replace('.','_'),','.join(temp_fields))
        
    return """
\"\"\"Packages and thier resources\"\"\"
# Construct fields    
{0}
    """.format(code)

def create_msgs(messages):
    code = ''
    for m in messages:
        code += '\n# Constructing message [{0}]\n_msg_{0} = helpers.WZMessage(name=\'{1}\',\n\
                                 description=\'{2}\',\n\
                                 fields=_msg_fields_{0},\n\
                                 extension_type={3},\n\
                                 extensions={4})\n'.format(m.get('fullName').replace('.','_'),m.get('name'),str(m.get('description')),'\'{}\''.format(m.get('extensionType')) if m.get('extensionType') is not None else None,m.get('extensions'))
    return """
# Construct messages
{0}
    """.format(code)

def create_pckgs(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        msgs = []
        enums = []
        for m in pkg.get('messages'):
            msgs.append('_msg_{0}'.format(m.get('fullName').replace('.','_')))
        if pkg.get('enums') is not None:
            for e in pkg.get('enums'):
                enums.append('_enum_{0}'.format(e.get('fullName').replace('.','_')))
        code += '\n_pkg_{0} = helpers.WZPackage(name=\'{1}\',\n\
                                                messages=[{2}],\n\
                                                enums=[{3}],\n\
                                                extensions={4})\n\
\n# Unpacking package [{0}]\n_pkg_{0}_name, _pkg_{0}_messages, _pkg_{0}_enums, _pkg_{0}_ext, _pkg_{0}_domain = _pkg_{0}.to_tuple()'.format(pkg.get('package').replace('.','_'),pkg.get('name'),','.join(msgs),','.join(enums),pkg.get('extensions'))
    return """
# Construct packages
{0}
    """.format(code)

def add_packgs(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        code += '\n# Adding package [{0}]\n_pkg_{0} = _architect.AddPackage(_pkg_{0}_name,\n\
                                                    dependencies=[],\n\
                                                    description=\'{1}\',\n\
                                                    domain=_pkg_{0}_domain,\n\
                                                    extensions=_pkg_{0}_ext)'.format(pkg.get('package').replace('.','_'),str(pkg.get('description')).replace("'",'"'))
    return """
# Add packages
{0}
    """.format(code)

def add_msgs(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        code += '\nfor m in _pkg_{0}_messages:\n\
\tmsg_name, msg_fields, msg_desc, msg_opt, msg_ext, msg_domain = m\n\
\ttemp_msg = _architect.AddMessage(package=_pkg_{0}, name=msg_name, fields=msg_fields, description=msg_desc, options=msg_opt, extensions=msg_ext, domain=msg_domain)\n\
\tmsgs_map[temp_msg.full_name] = temp_msg'.format(pkg.get('package').replace('.','_'))
    return """
msgs_map = {1}{2}

# Add packages messages
{0}
    """.format(code,_OPEN_BRCK,_CLOSING_BRCK)

def add_enums(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        code += '\nfor e in _pkg_{0}_enums:\n\
\tenum_name, enum_values, enum_desc, enum_domain = e\n\
\t_architect.AddEnum(package=_pkg_{0}, name=enum_name, enum_values=enum_values, description=enum_desc, domain=enum_domain)'.format(pkg.get('package').replace('.','_'))
    return """
# Add packages enums
{0}
    """.format(code,_OPEN_BRCK,_CLOSING_BRCK)

def create_rpcs(services):
    code = ''
    if services is not None:
        for s in services:
            svc = services.get(s)
            for rpc in svc.get('methods'):
                code += '\n_rpc_{0}_{4} = helpers.WZRPC(name=\'{4}\',client_stream={5},server_stream={6},in_type=msgs_map[_DOMAIN+\'.{1}\'].full_name, out_type=msgs_map[_DOMAIN+\'.{2}\'].full_name, description=\'{3}\')'.format(svc.get('fullName').replace('.','_'),'.'.join(rpc.get('inputType').split('.')[1:]),'.'.join(rpc.get('outputType').split('.')[1:]),str(rpc.get('description')).replace("'",'"'),rpc.get('name'),rpc.get('clientStreaming'),rpc.get('serverStreaming'))
        return """
\"\"\"Services and thier resources\"\"\"
# Construct rpc's
{0}
        """.format(code)
    else:
        return ''

def create_services(services):
    code = ''
    if services is not None:
        for s in services:
            svc = services[s]
            temp_rpcs = []
            for rpc in svc.get('methods'):
                temp_rpcs.append('_rpc_{0}_{1}'.format(svc.get('fullName').replace('.','_'),rpc.get('name'))) 

            temp_dependencies = []
            for d in svc.get('dependencies'):
                temp_dependencies.append('_pkg_{0}.package'.format(d.replace('.','_')))

            code += '\n_svc_{0} = helpers.WZService(\'{0}\',\n\
                                                methods=[{1}],\n\
                                                dependencies=[{2}],\n\
                                                description=\'{3}\',\n\
                                                extensions={4})\n\
\n_svc_{0}_name, _svc_{0}_methods, _svc_{0}_dependencies, _svc_{0}_desc, _svc_{0}_ext = _svc_{0}.to_tuple()'.format(svc.get('name'),','.join(temp_rpcs),','.join(temp_dependencies),str(svc.get('description')).replace("'",'"'),svc.get('extensions'))

        return """
# Construct services
{0}
        """.format(code)
    else:
        return ''

def add_services(services):
    code = ''
    if services is not None:
        for s in services:
            svc = services[s]
            code += '\n_svc_{0} = _architect.AddService(_svc_{0}_name,_svc_{0}_dependencies,_svc_{0}_desc,[],extensions=_svc_{0}_ext)'.format(svc.get('name'))

        return """
# Add services
{0}
        """.format(code)
    else:
        return ''

def add_rpcs(services):
    code = ''
    if services is not None:
        for s in services:
            svc = services[s]
            code += '\nfor rpc in _svc_{0}_methods:\n\
\trpc_name, rpc_in_out, rpc_desc = rpc\n\
\t_architect.AddRPC(_svc_{0}, rpc_name, rpc_in_out, rpc_desc)'.format(svc.get('name'))            
        return """
{0}
    """.format(code)
    else:
        return ''

def save_architect():
    return """
_architect.Save()
    """

def load_template(file_path:str):
    if file_system.check_if_file_exists(file_path):
        print_info('Running template script -> {0}'.format(file_path))
        subprocess.run(['python',file_path])
    else:
        print_error("File [{0}] does not exist !".format(file_path))
        exit(1)

def create_file_context(root_path,include,exclude):
    list_files = []
    if len(include) != 0:
        if '*' in include:
            for f in file_system.walkFiles(root_path):
                if f not in exclude and '.template.py' not in f and 'webezy.json' not in f:
                    code = ''.join(file_system.rFile(f))
                    code = bytes(code, 'utf-8')
                    list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(f,zlib.compress(code)))
                    print_note("Added file to template -> 'file':{0}".format(f),True)

        if '**/*' in include:
            for d in file_system.walkDirs(root_path):
                file_relative_path = d.split(file_system.get_current_location())[1]
                if file_relative_path != '':
                    if check_exclude(exclude,d,file_relative_path):
                        for f in file_system.walkFiles(d):
                            code = ''.join(file_system.rFile(file_system.join_path(d,f)))
                            code = bytes(code, 'utf-8')
                            list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(file_relative_path,f),zlib.compress(code)))
                            print_note("Added file to template -> 'path':{0},'file':{1}".format(file_relative_path,f),True)


        for inc in include:
            if '*' not in inc:
                if '.' in inc:
                    if file_system.check_if_file_exists(inc) and check_exclude(exclude,None,inc):
                        code = ''.join(file_system.rFile(inc))
                        code = bytes(code, 'utf-8')
                        list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(inc,zlib.compress(code)))
                        print_note("Added file to template -> 'file':{0}".format(inc),True)

                else:
                    if file_system.check_if_dir_exists(inc):
                        for f in file_system.walkFiles(file_system.get_current_location()+'/'+inc):
                            if check_exclude(exclude,inc,f):
                                code = ''.join(file_system.rFile(file_system.join_path(file_system.get_current_location(),inc,f)))
                                code = bytes(code, 'utf-8')
                                list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(inc,f),zlib.compress(code)))
                                print_note("Added file to template -> 'path':{0},'file':{1}".format(inc,f),True)

            else:
                if '/' in inc:
                    paths = inc.split('/')

                    if len(paths) > 2 and len(paths) <= 3:
                        relative = '/'.join(paths[:2])
                        if file_system.check_if_dir_exists(relative):
                            for f in file_system.walkFiles(file_system.get_current_location()+'/'+relative):

                                if '*.' in paths[-1] and check_exclude(exclude,relative,f):
                                    suffix = paths[-1].split('.')[1]
                                    if suffix in f:
                                        code = ''.join(file_system.rFile(file_system.join_path(relative,f)))
                                        code = bytes(code, 'utf-8')
                                        list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(relative,f),zlib.compress(code)))
                                        print_note("Added file to template -> 'path':{0},'file':{1}".format(relative,f),True)
                        else:
                            if '/**' in relative:
                                for d in file_system.walkDirs(paths[0]):
                                    for f in file_system.walkFiles(d):
                                        if check_exclude(exclude,d,f):
                                            if '*.' in paths[-1]:
                                                suffix = paths[-1].split('.')[1]
                                                if suffix in f:
                                                    code = ''.join(file_system.rFile(file_system.join_path(d,f)))
                                                    code = bytes(code, 'utf-8')
                                                    list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(d,f),zlib.compress(code)))
                                                    print_note("Added file to template -> 'path':{0},'file':{1}".format(d,f),True)
                                            elif paths[-1] == f:
                                                code = ''.join(file_system.rFile(file_system.join_path(d,f)))
                                                code = bytes(code, 'utf-8')
                                                list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(d,f),zlib.compress(code)))
                                                print_note("Added file to template -> 'path':{0},'file':{1}".format(d,f),True)

                    elif len(paths) < 2:
                        if file_system.check_if_dir_exists(paths[0]):
                            for f in file_system.walkFiles(file_system.get_current_location()+'/'+paths[0]):
                                if check_exclude(exclude,paths[0],f):
                                    if '*.' in paths[1]:
                                        suffix = paths[1].split('.')[1]
                                        if suffix in f:
                                            code = ''.join(file_system.rFile(file_system.join_path(paths[0],f)))
                                            code = bytes(code, 'utf-8')
                                            list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(paths[0],f),zlib.compress(code)))
                                            print_note("Added file to template -> 'path':{0},'file':{1}".format(paths[0],f),True)
                                    elif paths[1] == f:
                                        code = ''.join(file_system.rFile(file_system.join_path(paths[0],f)))
                                        code = bytes(code, 'utf-8')
                                        list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(paths[0],f),zlib.compress(code)))
                                        print_note("Added file to template -> 'path':{0},'file':{1}".format(paths[0],f),True)


                        elif '**' in paths[0]:
                            for d in file_system.walkDirs(root_path):
                                file_relative_path = d.split(file_system.get_current_location())[1]
                                if file_relative_path != '':
                                    if check_exclude(exclude,d,file_relative_path):
                                        for f in file_system.walkFiles(d):
                                            if '*.' in paths[1] and check_exclude(exclude,paths[0],f):
                                                suffix = paths[1].split('.')[1]
                                                if suffix in f:
                                                    code = ''.join(file_system.rFile(file_system.join_path(paths[0],f)))
                                                    code = bytes(code, 'utf-8')
                                                    list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(paths[0],f),zlib.compress(code)))
                                                    print_note("Added file to template -> 'path':{0},'file':{1}".format(paths[0],f),True)
                    else:
                        print_warning("Relative path is to deep !\n\tMax allowed recursion of directories is 2 from root directory of your project")
    else:   
        print_warning("No code files included !\n\t- We do not support template include ALL files under directory due to performance reasons\n\t  however we do plan to enrich this functionality with .wzignore file to exclude all files under directory based on the relative paths.")
        # TODO add .wzignore file which contains a ignore template relative paths / regex paths ( [*] only - for suffix and folders filter functionality)
        
        # for f in file_system.walkFiles(root_path):
        #     if f not in exclude and '.template.py' not in f and 'webezy.json' not in f:
        #         print_info({'file':f},True)

        # for d in file_system.walkDirs(root_path):
        #     file_relative_path = d.split(file_system.get_current_location())[1]
        #     if file_relative_path != '':
        #         if check_exclude(exclude,d,file_relative_path):
        #             print_info("Iterating dir code files")
        #             for f in file_system.walkFiles(d):
        #                 code = ''.join(file_system.rFile(file_system.join_path(d,f)))
        #                 code = bytes(code, 'utf-8')
        #                 list_files.append('WebezyFileContext(file=\'{0}\',code={1})'.format(file_system.join_path(file_relative_path,f),zlib.compress(code)))

    return """
# Initalize all code files 
_context = WebezyContext(files=[{0}]) 

# Creating all code files on target project
for f in _context.files:
\tfile_system.wFile(file_system.get_current_location()+'/'+f.file,zlib.decompress(f.code).decode(),force=True)

    """.format(',\n'.join(list_files))

def check_exclude(exclude,dir,file):
    # print_note(f"Checking exclude for -> {dir}/{file}")
    if len(exclude) != 0:
        is_valid = False
        for exc in exclude:
            if exc in file:
                is_valid = False
                break
            else:
                is_valid = True
        if is_valid:
            if dir is not None:
                if 'node_modules' not in dir:
                    # print_info({'directory':dir,'relative':file},True)
                    return True
            else:
                return True


    else:
        if dir is not None:
            if 'node_modules' not in dir:
                # print_info({'directory':dir,'relative':file},True)
                return True

        else:
            return True

def publish_template(template_file:str,code_context):
    pass