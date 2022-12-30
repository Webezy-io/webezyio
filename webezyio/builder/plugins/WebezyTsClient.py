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
import inspect

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
    
    if file_system.check_if_dir_exists(file_system.join_path(wz_json.path,'clients', 'typescript','utils')) == False:
        file_system.mkdir(file_system.join_path(wz_json.path,'clients', 'typescript','utils'))

    file_system.cpDir(file_system.join_path(wz_json.path,'server','services','utils'),file_system.join_path(wz_json.path,'clients','typescript','utils'))

    # file_system.cpDir(file_system.join_path(wz_json.path,'server','services','p'),file_system.join_path(wz_json.path,'clients','typescript','index.js.map'))
    
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))
    return (__name__,'OK')


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
def write_clients(wz_json: helpers.WZJson, wz_context: helpers.WZContext,pre_data):
    imports = []
    exports = []
    override_stubs = {}
    before_init = ''
    interceptors = []
    client_options = [
        ("grpc.keepalive_time_ms", 120000),
        ("grpc.http2.min_time_between_pings_ms",120000),
        ("grpc.keepalive_timeout_ms",20000),
        ("grpc.http2.max_pings_without_data",0),
        ("grpc.keepalive_permit_without_calls",1),
        ("interceptors","interceptorsProviders")
    ]
    """Parse pre data"""
    if pre_data:
        _hook_name = inspect.stack()[0][3]
        for mini_hooks in pre_data:
            for hook in mini_hooks:
                if __name__ == hook.split(':')[0]:
                    if hook.split(':')[2] is not None and _hook_name == hook.split(':')[1].replace('()',''):
                        
                         # Append to exports
                        if 'append_imports' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for imp in mini_hooks[hook]:
                                    imports.append(imp)

                        # Append to exports
                        elif 'append_exports' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for exp in mini_hooks[hook]:
                                    exports.append(exp)
                    
                        # Append to exports
                        elif 'override_stubs' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for stub in mini_hooks[hook]:
                                    override_stubs[stub] = mini_hooks[hook][stub]

                        elif 'append_client_options' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for k,v in mini_hooks[hook]:
                                    old_value = next((i for i in client_options if i[0] == k),(None,None))[1]
                                    if k not in list(map(lambda x: x[0], client_options)):
                                        client_options.append((k,v))
                                    elif v != old_value:
                                        client_options.remove((k,old_value))
                                        client_options.append((k,v))
                        elif 'add_before_init' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                before_init = mini_hooks[hook]

                        elif 'append_interceptors' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for intrcpt in mini_hooks[hook]:
                                    interceptors.append(intrcpt)
                    else:
                        pretty.print_warning(f'[{__name__}] `{hook}` missing command')


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
        'packageName'), wz_json.services, wz_json.packages, wz_context,pre_data={
            'imports': imports,
            'exports': exports,
            'stubs': override_stubs,
            'client_options': client_options,
            'before_init':before_init,
            'interceptors': interceptors
        })
    file_system.wFile(file_system.join_path(
        wz_json.path, 'services', 'index.ts'), client.__str__(), overwrite=True)
