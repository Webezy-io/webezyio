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
from sylk.commons import helpers, file_system, resources,pretty, protos
from sylk.builder.plugins.static import gitignore_ts,utils_errors_ts,utils_interfaces,package_json,bash_init_script_ts,bash_run_server_script_ts,protos_compile_script_ts,main_ts_config,clients_ts_configs,protos_ts_config
import inspect


@builder.hookimpl
def pre_build(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    pretty.print_info("Starting sylk build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    # TODO add postbuild validation of generated code
    pretty.print_success("Finished sylk build process %s plugin" % (__name__))
    return (__name__,'OK')


@builder.hookimpl
def init_project_structure(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    directories = [
        # Utils
        file_system.join_path(sylk_json.path, 'services', 'utils'),
        # Protos
        file_system.join_path(sylk_json.path, 'services', 'protos')]

    for dir in directories:
        file_system.mkdir(dir)
    # Utils error
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'services','utils', 'error.ts'), utils_errors_ts)
    # Utils Interfaces
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'services','utils', 'interfaces.ts'), utils_interfaces)
    # package.json
    file_system.wFile(file_system.join_path(sylk_json.path,'package.json'),package_json.replace('REPLACEME',sylk_json.project.get('packageName')))
    
    # Bin files
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'bin', 'init-ts.sh'), bash_init_script_ts)
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'bin', 'proto.js'), protos_compile_script_ts)

    # tsconfig.json
    file_system.wFile(file_system.join_path(sylk_json.path, 'tsconfig.json'),main_ts_config)
    file_system.wFile(file_system.join_path(sylk_json.path, 'services', 'protos', 'tsconfig.json'),protos_ts_config)
    
    if sylk_json.get_server_language() == 'typescript':
        file_system.wFile(file_system.join_path(
            sylk_json.path, 'bin', 'run-server.sh'), bash_run_server_script_ts)
    
    # file_system.wFile(file_system.join_path(sylk_json.path,'.webezy','contxt.json'),'{"files":[]}')
    
    # .gitignore
    file_system.wFile(file_system.join_path(sylk_json.path,'.gitignore'),gitignore_ts)

    return [directories]


@builder.hookimpl
def write_services(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    for svc in sylk_json.services:
        if file_system.check_if_file_exists(file_system.join_path(
            sylk_json.path, 'services', f'{svc}.ts')) == False:
            service_code = helpers.SylkServiceTs(sylk_json.project.get('packageName'), svc, sylk_json.services[svc].get(
                'dependencies'), sylk_json.services[svc], context=sylk_context,sylk_json=sylk_json).to_str()
            file_system.wFile(file_system.join_path(
                sylk_json.path, 'services', f'{svc}.ts'), service_code, overwrite=True)
        else:
            pretty.print_info("Make sure you are editing the {0} file\n - See how to edit service written in Typescript".format(file_system.join_path(
                sylk_json.path, 'services', f'{svc}.ts')))

@builder.hookimpl
def compile_protos(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    # Running ./bin/init.sh script for compiling protos
    pretty.print_note("Running ./bin/init-ts.sh script for 'protoc' compiler")
    proc = subprocess.run(['bash', file_system.join_path(
        sylk_json.path, 'bin', 'init-ts.sh')])
    pretty.print_note(proc,True)
    if int(proc.returncode) != 0:
        pretty.print_error("ERROR occured during building process some more info on specific error can be found above")
        exit(proc.returncode)
    pretty.print_success("Compiled protos %s" % (__name__))
    


def parse_proto_type_to_ts(type, label, messageType=None, enumType=None):
    temp_type = 'None'
    if 'int' in type or type == 'float' or type == 'double':
        temp_type = 'number'
    elif type == 'string':
        temp_type = 'string'
    elif type == 'message' or type == 'enum':
        temp_type = '{0}__pb2.{1}'.format(
            messageType.split('.')[1], messageType.split('.')[-1])
    elif type == 'enum':
        temp_type = '{0}__pb2.{1}'.format(
            enumType.split('.')[1], enumType.split('.')[-1])
    elif type == 'bool':
        temp_type = 'boolean'
    if label == 'repeated':
        temp_type = f'{temp_type}[]'
    return temp_type


_OPEN_BRCK = '{'
_CLOSING_BRCK = '}'

# @builder.hookimpl
# def init_context(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
#     files = []
#     pretty.print_error("Initialize sylk.context file")

#     path = sylk_json.project.get('uri')
#     if sylk_json.services is not None:
#         for svc in sylk_json.services:
#             methods = []
#             if sylk_json.services[svc].get('methods') is not None and len(sylk_json.services[svc].get('methods')) > 0 :
#                 for rpc in sylk_json.services[svc].get('methods'):
#                     rpc_name = rpc.get('name')
#                     rpc_type_out = rpc.get('serverStreaming')
#                     rpc_out_name = rpc.get('inputType').split('.')[-1]
#                     rpc_out_pkg = rpc.get('outputType').split('.')[1]
#                     rpc_output = rpc.get('outputType')
#                     msg = sylk_json.get_message(rpc_output)
#                     fields = []
#                     for f in msg.get('fields'):
#                         F_VALUE = 'null'
#                         if f.get('fieldType') == 'TYPE_STRING':
#                             F_VALUE = '"SomeString"'
#                         elif f.get('fieldType') == 'TYPE_BOOL':
#                             F_VALUE = 'false'
#                         elif f.get('fieldType') == 'TYPE_INT32' or f.get('fieldType') ==  'TYPE_INT64':
#                             F_VALUE = '1'
#                         elif f.get('fieldType') == 'TYPE_FLOAT' or f.get('fieldType') == 'TYPE_DOUBLE':
#                             F_VALUE = '1.0'

#                         fields.append('{0}: {1}'.format(f.get('name'), F_VALUE))
#                     fields = ','.join(fields)
#                     if rpc_type_out:
#                         out_prototype = f'\t\tcall.destroy(new ServiceError(status.UNIMPLEMENTED,"Method is not yet implemented"))'
#                     else:
#                         out_prototype = f'\t\t// let response:{rpc_out_pkg}.{rpc_out_name} = {_OPEN_BRCK} {fields} {_CLOSING_BRCK};\n\t\t// callback(null,response);\n\t\tcallback(new ServiceError(status.UNIMPLEMENTED,"Method is not yet implemented"))'
#                     code = f'{out_prototype}\n'
#                     methods.append(protos.WebezyMethodContext(
#                         name=rpc_name, code=code, type='rpc'))
#                 files.append(protos.WebezyFileContext(
#                     file=f'./services/{svc}.ts', methods=methods))
#             else:
#                 pretty.print_warning("No available RPC's for -> {}".format(svc))
#     context = resources.proto_to_dict(protos.WebezyContext(files=files))
#     logging.debug("Writing new context")
#     file_system.mkdir(file_system.join_path(path, '.webezy'))
#     file_system.wFile(file_system.join_path(
#         path, '.webezy', 'context.json'), context, json=True, overwrite=True)
#     sylk_json = helpers.SylkContext(context)
#     return context

@builder.hookimpl
def rebuild_context(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    pretty.print_note("Re-Building sylk.context")
    if sylk_json.services is not None:
        for svc in sylk_json.services:
            try:
                svcFile = file_system.rFile(file_system.join_path(
                    sylk_json.path, 'services', f'{svc}.ts'))
                is_init = False
                for l in svcFile:
                    if '__init__' in l:
                        is_init = True
                        break
                # Non RPC functions should have # @skip line above func name
                function_code_inlines = helpers.parse_code_file(svcFile, '@skip')
                # Parse all rpc's in file by default # @rpc seperator
                rpc_code_inlines = helpers.parse_code_file(svcFile)
                for f in sylk_context.files:

                    if svc in f.get('file'):
                        # Iterating all regular functions
                        for func in function_code_inlines:
                            func_code = []
                            for l in func:
                                if '@rpc @@sylk' in l:
                                    break

                                func_code.append(l)
                            func_name = func_code[0].split(
                            '(')[0].split('private')
                            if len(func_name) > 1:
                                func_name = func_name[1].strip()
                            else:
                                func_name = func_name[0].strip()
                            sylk_context.set_method_code(svc, func_name, ''.join(func_code))
                        methods_i = 0
                        for r in sylk_json.services[svc]['methods']:
                            if next((m for m in f.get('methods') if m['name'] == r['name']),None) is None:
                                pretty.print_note(f"Starting new RPC at sylk.context [{r.get('name')}]")
                                new_rpc_context = {'name': r.get('name'), 'type': 'rpc', 'code': '\t\tbreak;'}
                                sylk_context.new_rpc(svc, new_rpc_context, suffix='ts')
                        # Iterating all RPC's functions
                        for m in f.get('methods'):
                            if m['type'] == 'rpc':
                                # Checking if edit to method has happened - meaning canot find in sylk.json all context methods
                                if next((r for r in sylk_json.services[svc]['methods'] if r['name'] == m['name']), None) == None:
                                    # Getting method details from sylk.json
                                    new_method = sylk_json.services[svc]['methods'][methods_i]
                                    # Building new context with old func code
                                    new_rpc_context = {'name': new_method.get(
                                        'name'), 'type': 'rpc', 'code': ''.join(rpc_code_inlines[methods_i][1:])}
                                    # Editing inplace the RPC context
                                    sylk_context.edit_rpc(
                                        svc, m.get('name'), new_rpc_context)
                                else:
                                    # Setting new context
                                    temp_lines = []
                                    num_lines = 4
                                    for l in rpc_code_inlines[methods_i]:
                                        if 'ServerWritableStream<' in l:
                                            num_lines = 3
                                            break
                                    for line in rpc_code_inlines[methods_i][num_lines:]:
                                        
                                        if '\t}\n' == line:
                                            if '\n' == temp_lines[-1]:
                                                break

                                        if 'export {' in line:
                                            break

                                        temp_lines.append(line)
                                    # pretty.print_info(f"Setting RPC -> {m.get('name')}\n-> {temp_lines}")
                                    sylk_context.set_rpc_code(svc, m.get('name'), ''.join(
                                        temp_lines))

                                methods_i += 1

            except Exception as e:
                pretty.print_error(e)

    # pretty.print_note(sylk_context.dump(),True)
    file_system.wFile(file_system.join_path(
        sylk_json.path, '.sylk', 'context.json'), sylk_context.dump(), True, True)

@builder.hookimpl
def write_server(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext,pre_data):
    
    imports = ['import { Server, ServerCredentials } from \'@grpc/grpc-js\';']
    services_init_impl = []
    services_bindings = []
    overwrite = False
    server_options = [
        ('grpc.max_receive_message_length',-1),
        ('grpc.max_send_message_length',-1)
    ]
    before_init = ''
    injects_service = {}
    startup_promises =[]
    after_startup = ''
    """Parse pre data"""
    if pre_data:
        _hook_name = inspect.stack()[0][3]
        for mini_hooks in pre_data:
            for hook in mini_hooks:
                if __name__ == hook.split(':')[0]:

                    if hook.split(':')[2] is not None and _hook_name == hook.split(':')[1].replace('()',''):

                        # Pre consume imports
                        if 'append_imports' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for imp in mini_hooks[hook]:
                                    imports.append(imp)
                        
                        # Pre consume services bindings
                        elif 'append_services_bindings' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None and len(mini_hooks[hook]) > 1:
                                for imp in mini_hooks[hook]:
                                    imports.append(imp)
                        
                        # Force rewriting of server each build
                        elif 'overwrite' in hook.split(':')[2]:
                            if mini_hooks[hook] == True:
                                overwrite = True

                        elif 'append_server_options' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for k,v in mini_hooks[hook]:
                                    old_value = next((i for i in server_options if i[0] == k),(None,None))[1]
                                    if k not in list(map(lambda x: x[0], server_options)):
                                        server_options.append((k,v))
                                    elif v != old_value:
                                        server_options.remove((k,old_value))
                                        server_options.append((k,v))

                        # Add code before server init
                        elif 'add_before_init' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                before_init = mini_hooks[hook]
                        
                        # Inject the service classes with additional objects
                        elif 'inject_service' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for svc in mini_hooks[hook]:
                                    injects_service[svc] = mini_hooks[hook][svc]
                        
                        # Inject the service classes with additional objects
                        elif 'wrap_service' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for svc in mini_hooks[hook]:
                                    injects_service[svc] = mini_hooks[hook][svc]
                        
                        # Inject the service classes with additional objects
                        elif 'append_startup_promise' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                for promise in mini_hooks[hook]:
                                    startup_promises.append(promise)

                        # Append code block after startup
                        elif 'append_after_startup' in hook.split(':')[2]:
                            if mini_hooks[hook] is not None:
                                after_startup = mini_hooks[hook]


                    else:
                        pretty.print_warning(f'[{__name__}] `{hook}` missing command')

                    
    
    for svc in sylk_json.services:
        imports.append(f'import {_OPEN_BRCK} {svc}, {svc}Service {_CLOSING_BRCK} from \'./services/{svc}\';')
        injects = []
        if svc in injects_service:
            injects.append(injects_service[svc])
        
        injects = ', '.join(injects)
        services_init_impl.append(f'const {svc}Impl = new {svc}({injects})')

        services_bindings.append(
            f'server.addService({svc}Service, {svc}Impl);')
    services_bindings = '\n\t'.join(services_bindings)
    services_init_impl = '\n\t'.join(services_init_impl)
    imports = '\n'.join(imports)
    startup_promises = ',\n\t'.join(startup_promises)
    server_options = '\n\t'.join(list(map(lambda opt: '"{}": {},'.format(opt[0],opt[1]),server_options)))
    server_code = f'// sylk.build Generated Server Code\n\
{imports}\n\n\
let _PORT:number = 50051;\n\
let _HOST:string = \'0.0.0.0\';\n\
let _ADDR = `${_OPEN_BRCK}_HOST{_CLOSING_BRCK}:${_OPEN_BRCK}_PORT{_CLOSING_BRCK}`\n\
{before_init}\n\
const server = new Server({_OPEN_BRCK}\n\
\t{server_options}\n\
{_CLOSING_BRCK});\n\n\
async function startServer() {_OPEN_BRCK}\n\
\tconst promises: Promise<number>[] = [\n\
\t{startup_promises}\n\
\t];\n\
\tconst results = await Promise.all(promises);\n\
\tconsole.log(results);\n\n\
\t{after_startup}\n\n\
\t{services_init_impl}\n\
\t{services_bindings}\n\n\
\tserver.bindAsync(_ADDR, ServerCredentials.createInsecure(), (err: Error | null, bindPort: number) => {_OPEN_BRCK}\n\tif (err) {_OPEN_BRCK}\n\t\tthrow err;\n\t{_CLOSING_BRCK}\n\n\tconsole.log(`[sylk.build] Starting gRPC:server:${_OPEN_BRCK}bindPort{_CLOSING_BRCK}`,`at -> ${_OPEN_BRCK}new Date().toLocaleString(){_CLOSING_BRCK})`);\n\tserver.start();\n\t{_CLOSING_BRCK});\n{_CLOSING_BRCK}\n\nstartServer().then(res => console.log("Service Start Up...")).catch(err => console.log(err));'
   
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'server.ts'), server_code,overwrite=overwrite)
    pretty.print_warning("Make sure you make desired changes on server.ts file !")
