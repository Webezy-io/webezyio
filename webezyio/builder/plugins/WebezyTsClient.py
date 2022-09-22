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
    file_system.wFile(file_system.join_path(wz_json.path,'package.json'),package_json)
    
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
    file_system.mkdir(file_system.join_path(wz_json.path,'clients','typescript','protos'))
    for f in file_system.walkFiles(file_system.join_path(wz_json.path, 'server','services','protos')):
        file_system.copyFile(file_system.join_path(wz_json.path,'server','services', 'protos', f), file_system.join_path(wz_json.path,'clients','typescript','protos',f))
    
    client = helpers.WZClientTs(wz_json.project.get(
        'packageName'), wz_json.services, wz_json.packages, wz_context)
    file_system.wFile(file_system.join_path(
        wz_json.path, 'services', 'index.ts'), client.__str__(), overwrite=True)
