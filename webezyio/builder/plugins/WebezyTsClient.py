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
from webezyio.builder.plugins.static import gitignore_ts,package_json,bash_init_script_ts,protos_compile_script_ts,main_ts_config_client_only,protos_ts_config_client_only


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    if file_system.check_if_file_exists(file_system.join_path(wz_json.path,'server', 'services','index.js')):
        file_system.mv(file_system.join_path(wz_json.path,'server','services','index.d.ts'),file_system.join_path(wz_json.path,'clients','typescript','index.d.ts'))
        file_system.mv(file_system.join_path(wz_json.path,'server','services','index.js'),file_system.join_path(wz_json.path,'clients','typescript','index.js'))
        file_system.mv(file_system.join_path(wz_json.path,'server','services','index.js.map'),file_system.join_path(wz_json.path,'clients','typescript','index.js.map'))
    else:
        subprocess.run(['tsc', '-b'])
        if file_system.check_if_file_exists(file_system.join_path(wz_json.path,'server', 'services','index.js')):
            file_system.mv(file_system.join_path(wz_json.path,'server','services','index.d.ts'),file_system.join_path(wz_json.path,'clients','typescript','index.d.ts'))
            file_system.mv(file_system.join_path(wz_json.path,'server','services','index.js'),file_system.join_path(wz_json.path,'clients','typescript','index.js'))
            file_system.mv(file_system.join_path(wz_json.path,'server','services','index.js.map'),file_system.join_path(wz_json.path,'clients','typescript','index.js.map'))
    
    # file_system.cpDir(file_system.join_path(wz_json.path,'server','services','p'),file_system.join_path(wz_json.path,'clients','typescript','index.js.map'))
    
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    directories = [
        # Clients
        file_system.join_path(wz_json.path, 'clients', 'typescript'),
        file_system.join_path(wz_json.path, 'clients', 'typescript','protos'),
        # Utils
        file_system.join_path(wz_json.path, 'services', 'utils'),
        # Protos
        file_system.join_path(wz_json.path, 'services', 'protos')]

    for dir in directories:
        file_system.mkdir(dir)
    # package.json
    if wz_json.get_server_language() != 'typescript':
        pretty.print_info('Removing rimraf server dir')
        tmp_pkg_json = package_json.replace('rimraf server &&','')
    else:
        tmp_pkg_json = package_json
    file_system.wFile(file_system.join_path(wz_json.path,'package.json'),tmp_pkg_json.replace('REPLACEME',wz_json.project.get('packageName')))
    
    # Bin files
    file_system.wFile(file_system.join_path(
        wz_json.path, 'bin', 'init-ts.sh'), bash_init_script_ts)
    file_system.wFile(file_system.join_path(
        wz_json.path, 'bin', 'proto.js'), protos_compile_script_ts)

    # tsconfig.json
    if wz_json.get_server_language() != 'typescript':
        file_system.wFile(file_system.join_path(wz_json.path, 'tsconfig.json'),main_ts_config_client_only)
        file_system.wFile(file_system.join_path(wz_json.path, 'services', 'protos', 'tsconfig.json'),protos_ts_config_client_only)
    
    # file_system.wFile(file_system.join_path(wz_json.path,'.webezy','contxt.json'),'{"files":[]}')
    
    # .gitignore
    file_system.wFile(file_system.join_path(wz_json.path,'.gitignore'),gitignore_ts)

    return [directories]

@builder.hookimpl
def compile_protos(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # Running ./bin/init-ts.sh script for compiling protos
    if wz_json.get_server_language() != 'typescript':
        logging.info("Running ./bin/init-ts.sh script for 'protoc' compiler")
        subprocess.run(['bash', file_system.join_path(
            wz_json.path, 'bin', 'init-ts.sh')])

@builder.hookimpl
def write_clients(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    if file_system.check_if_dir_exists(file_system.join_path(wz_json.path,'clients','typescript')):
        file_system.mkdir(file_system.join_path(wz_json.path,'clients','typescript','protos'))
    else:
        file_system.mkdir(file_system.join_path(wz_json.path,'clients','typescript'))
        file_system.mkdir(file_system.join_path(wz_json.path,'clients','typescript','protos'))
    
    if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'server','services','protos')):
        for f in file_system.walkFiles(file_system.join_path(wz_json.path, 'server','services','protos')):
            file_system.copyFile(file_system.join_path(wz_json.path,'server','services', 'protos', f), file_system.join_path(wz_json.path,'clients','typescript','protos',f))
        
        if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'server','services','protos','google')):
            file_system.cpDir(file_system.join_path(wz_json.path, 'server','services','protos','google'),file_system.join_path(wz_json.path, 'clients','typescript','protos','google'))

    client = helpers.WZClientTs(wz_json.project.get(
        'packageName'), wz_json.services, wz_json.packages, wz_context)
    file_system.wFile(file_system.join_path(
        wz_json.path, 'services', 'index.ts'), client.__str__(), overwrite=True)
