# Copyright (c) 2023 sylk.build

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
import sylk.builder as builder
from sylk.commons import helpers, file_system, resources, pretty
from sylk.builder.plugins.static import gitignore_go,package_json,bash_init_script_go,sylk_go_utils_channel


@builder.hookimpl
def pre_build(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    pretty.print_info("Starting sylk.build build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    if file_system.check_if_file_exists(file_system.join_path(sylk_json.path,'go.mod')):
        pretty.print_info('Run the following commands :\n\t-> $ go test\n\t-> $ go mod tidy')

    else:
        pretty.print_info('Run the following command :\n\t-> $ go mod init {}'.format(_format_go_package_name(sylk_json.project.get('goPackage'))))
    pretty.print_success("Finished sylk.build build process %s plugin" % (__name__))
    return (__name__,'OK')


@builder.hookimpl
def init_project_structure(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    directories = [
        # Clients
        file_system.join_path(sylk_json.path, 'clients', 'go'),
        file_system.join_path(sylk_json.path, 'clients', 'go','protos'),
        file_system.join_path(sylk_json.path, 'clients', 'go','utils'),

        # Protos
        file_system.join_path(sylk_json.path, 'services', 'protos')]

    for dir in directories:
        file_system.mkdir(dir)
    
    # Bin files
    services_protoc = []
    packages_protoc = []
    if sylk_json.services is not None:
        for s in sylk_json.services:
            services_protoc.append(s)
            if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path, 'services', 'protos', s)) == False:
                file_system.mkdir(file_system.join_path(sylk_json.path, 'services', 'protos',s))
    if sylk_json.packages is not None:
        for p in sylk_json.packages:
            packages_protoc.append(sylk_json.packages[p].get('name'))
            if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path, 'services', 'protos', sylk_json.packages[p].get('name'))) == False:
                file_system.mkdir(file_system.join_path(sylk_json.path, 'services', 'protos', sylk_json.packages[p].get('name')))

    file_system.wFile(file_system.join_path(
        sylk_json.path, 'clients','go','utils', 'channel.go'), sylk_go_utils_channel)
    # file_system.wFile(file_system.join_path(
        # sylk_json.path, 'bin', 'proto.js'), protos_compile_script_ts)

    # tsconfig.json
    # if sylk_json.get_server_language() != 'typescript':
        # file_system.wFile(file_system.join_path(sylk_json.path, 'tsconfig.json'),main_ts_config_client_only)
        # file_system.wFile(file_system.join_path(sylk_json.path, 'services', 'protos', 'tsconfig.json'),protos_ts_config_client_only)
    
    # file_system.wFile(file_system.join_path(sylk_json.path,'.sylk','contxt.json'),'{"files":[]}')
    
    # .gitignore
    # gitignore_path = file_system.join_path(sylk_json.path,'.gitignore')
    # if file_system.check_if_file_exists(gitignore_path):
    #     gitignore_file = ''.join(file_system.rFile(gitignore_path))
    #     gitignore_file += gitignore_go
    #     file_system.wFile(file_system.join_path(sylk_json.path,'.gitignore'),gitignore_file,True)
    file_system.wFile(file_system.join_path(sylk_json.path,'.gitignore'),gitignore_go)

    return [directories]

@builder.hookimpl
def compile_protos(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    services_protoc = []
    packages_protoc = []
    if sylk_json.services is not None:
        for s in sylk_json.services:
            services_protoc.append(s)
    if sylk_json.packages is not None:
        for p in sylk_json.packages:
            packages_protoc.append(sylk_json.packages[p].get('name'))
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'bin', 'init-go.sh'), bash_init_script_go(sylk_json.project.get('packageName'),services_protoc,packages_protoc),True)
    # Running ./bin/init-go.sh script for compiling protos
    if sylk_json.get_server_language() != 'go':
        logging.info("Running ./bin/init-go.sh script for 'protoc' compiler")
        subprocess.run(['bash', file_system.join_path(
            sylk_json.path, 'bin', 'init-go.sh')])

@builder.hookimpl
def write_clients(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path,'clients','go')):
        file_system.mkdir(file_system.join_path(sylk_json.path,'clients','go','protos'))
    else:
        file_system.mkdir(file_system.join_path(sylk_json.path,'clients','go'))
        file_system.mkdir(file_system.join_path(sylk_json.path,'clients','go','protos'))
    
    if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path, 'services','protos')):
        for f in file_system.walkFiles(file_system.join_path(sylk_json.path, 'services','protos')):
            if '.go' in f:
                file_name = f.split('.')[0] if '_grpc' not in f else f.split('_grpc.')[0]
                go_proto_package_dir = file_system.join_path(sylk_json.path,'services', 'protos', file_name)
                if file_system.check_if_dir_exists(go_proto_package_dir) == False:
                    file_system.mkdir(go_proto_package_dir)
                file_system.mv(file_system.join_path(sylk_json.path,'services', 'protos', f), file_system.join_path(go_proto_package_dir,f))
        
        # if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path, 'services','protos','google')):
            # file_system.cpDir(file_system.join_path(sylk_json.path, 'services','protos','google'),file_system.join_path(sylk_json.path, 'clients','go','protos','google'))

    client = helpers.SylkClientGo(sylk_json.project.get(
        'packageName'), sylk_json.services, sylk_json.packages, sylk_context, sylk_json=sylk_json)
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'clients','go', 'main.go'), client.__str__(), overwrite=True)

def _format_go_package_name(go_package):
    return '{}'.format(go_package)