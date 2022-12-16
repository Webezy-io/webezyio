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
import webezyio.builder as builder
from webezyio.commons import helpers, file_system, resources, pretty
from webezyio.builder.plugins.static import gitignore_go,package_json,bash_init_script_go


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    if file_system.check_if_file_exists(file_system.join_path(wz_json.path,'go.mod')):
        pretty.print_info('Run the following commands :\n\t-> $ go test\n\t-> $ go mod tidy')

    else:
        pretty.print_info('Run the following command :\n\t-> $ go mod init {}'.format(_format_go_package_name(wz_json.project.get('goPackage'))))
        # subprocess.run(['go mod init',_format_go_package_name(wz_json.project.get('goPackage'))])
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    directories = [
        # Clients
        file_system.join_path(wz_json.path, 'clients', 'go'),
        file_system.join_path(wz_json.path, 'clients', 'go','protos'),
        # Protos
        file_system.join_path(wz_json.path, 'services', 'protos')]

    for dir in directories:
        file_system.mkdir(dir)
    
    # Bin files
    services_protoc = []
    packages_protoc = []
    if wz_json.services is not None:
        for s in wz_json.services:
            services_protoc.append(s)
            if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'services', 'protos', s)) == False:
                file_system.mkdir(file_system.join_path(wz_json.path, 'services', 'protos',s))
    if wz_json.packages is not None:
        for p in wz_json.packages:
            packages_protoc.append(wz_json.packages[p].get('name'))
            if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'services', 'protos', wz_json.packages[p].get('name'))) == False:
                file_system.mkdir(file_system.join_path(wz_json.path, 'services', 'protos', wz_json.packages[p].get('name')))

    # file_system.wFile(file_system.join_path(
        # wz_json.path, 'bin', 'init-go.sh'), bash_init_script_go(wz_json.project.get('packageName'),services_protoc,packages_protoc))
    # file_system.wFile(file_system.join_path(
        # wz_json.path, 'bin', 'proto.js'), protos_compile_script_ts)

    # tsconfig.json
    # if wz_json.get_server_language() != 'typescript':
        # file_system.wFile(file_system.join_path(wz_json.path, 'tsconfig.json'),main_ts_config_client_only)
        # file_system.wFile(file_system.join_path(wz_json.path, 'services', 'protos', 'tsconfig.json'),protos_ts_config_client_only)
    
    # file_system.wFile(file_system.join_path(wz_json.path,'.webezy','contxt.json'),'{"files":[]}')
    
    # .gitignore
    gitignore_path = file_system.join_path(wz_json.path,'.gitignore')
    if file_system.check_if_file_exists(gitignore_path):
        gitignore_file = ''.join(file_system.rFile(gitignore_path))
        gitignore_file += gitignore_go
        file_system.wFile(file_system.join_path(wz_json.path,'.gitignore'),gitignore_file,True)
    file_system.wFile(file_system.join_path(wz_json.path,'.gitignore'),gitignore_go)

    return [directories]

@builder.hookimpl
def compile_protos(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    services_protoc = []
    packages_protoc = []
    if wz_json.services is not None:
        for s in wz_json.services:
            services_protoc.append(s)
    if wz_json.packages is not None:
        for p in wz_json.packages:
            packages_protoc.append(wz_json.packages[p].get('name'))
    file_system.wFile(file_system.join_path(
        wz_json.path, 'bin', 'init-go.sh'), bash_init_script_go(wz_json.project.get('packageName'),services_protoc,packages_protoc),True)
    # Running ./bin/init-go.sh script for compiling protos
    if wz_json.get_server_language() != 'go':
        logging.info("Running ./bin/init-go.sh script for 'protoc' compiler")
        subprocess.run(['bash', file_system.join_path(
            wz_json.path, 'bin', 'init-go.sh')])

@builder.hookimpl
def write_clients(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    if file_system.check_if_dir_exists(file_system.join_path(wz_json.path,'clients','go')):
        file_system.mkdir(file_system.join_path(wz_json.path,'clients','go','protos'))
    else:
        file_system.mkdir(file_system.join_path(wz_json.path,'clients','go'))
        file_system.mkdir(file_system.join_path(wz_json.path,'clients','go','protos'))
    
    if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'services','protos')):
        for f in file_system.walkFiles(file_system.join_path(wz_json.path, 'services','protos')):
            if '.go' in f:
                file_name = f.split('.')[0] if '_grpc' not in f else f.split('_grpc.')[0]
                go_proto_package_dir = file_system.join_path(wz_json.path,'services', 'protos', file_name)
                if file_system.check_if_dir_exists(go_proto_package_dir) == False:
                    file_system.mkdir(go_proto_package_dir)
                file_system.mv(file_system.join_path(wz_json.path,'services', 'protos', f), file_system.join_path(go_proto_package_dir,f))
        
        # if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'services','protos','google')):
            # file_system.cpDir(file_system.join_path(wz_json.path, 'services','protos','google'),file_system.join_path(wz_json.path, 'clients','go','protos','google'))

    client = helpers.WZClientGo(wz_json.project.get(
        'packageName'), wz_json.services, wz_json.packages, wz_context, wz_json=wz_json)
    file_system.wFile(file_system.join_path(
        wz_json.path, 'clients','go', 'main.go'), client.__str__(), overwrite=True)

def _format_go_package_name(go_package):
    return '{}'.format(go_package)