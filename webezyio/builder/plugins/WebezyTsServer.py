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
from webezyio.commons import helpers, file_system, resources,pretty, protos
from webezyio.builder.plugins.static import gitignore_ts,utils_errors_ts,utils_interfaces,package_json,bash_init_script_ts,bash_run_server_script_ts,protos_compile_script_ts,main_ts_config,clients_ts_configs,protos_ts_config


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # TODO add postbuild validation of generated code
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    directories = [
        # Utils
        file_system.join_path(wz_json.path, 'services', 'utils'),
        # Protos
        file_system.join_path(wz_json.path, 'services', 'protos')]

    for dir in directories:
        file_system.mkdir(dir)
    # Utils error
    file_system.wFile(file_system.join_path(
        wz_json.path, 'services','utils', 'error.ts'), utils_errors_ts)
    # Utils Interfaces
    file_system.wFile(file_system.join_path(
        wz_json.path, 'services','utils', 'interfaces.ts'), utils_interfaces)
    # package.json
    file_system.wFile(file_system.join_path(wz_json.path,'package.json'),package_json.replace('REPLACEME',wz_json.project.get('packageName')))
    
    # Bin files
    file_system.wFile(file_system.join_path(
        wz_json.path, 'bin', 'init-ts.sh'), bash_init_script_ts)
    file_system.wFile(file_system.join_path(
        wz_json.path, 'bin', 'proto.js'), protos_compile_script_ts)

    # tsconfig.json
    file_system.wFile(file_system.join_path(wz_json.path, 'tsconfig.json'),main_ts_config)
    file_system.wFile(file_system.join_path(wz_json.path, 'services', 'protos', 'tsconfig.json'),protos_ts_config)
    
    if wz_json.get_server_language() == 'typescript':
        file_system.wFile(file_system.join_path(
            wz_json.path, 'bin', 'run-server.sh'), bash_run_server_script_ts)
    
    # file_system.wFile(file_system.join_path(wz_json.path,'.webezy','contxt.json'),'{"files":[]}')
    
    # .gitignore
    file_system.wFile(file_system.join_path(wz_json.path,'.gitignore'),gitignore_ts)

    return [directories]


@builder.hookimpl
def write_services(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    for svc in wz_json.services:
        if file_system.check_if_file_exists(file_system.join_path(
            wz_json.path, 'services', f'{svc}.ts')) == False:
            service_code = helpers.WZServiceTs(wz_json.project.get('packageName'), svc, wz_json.services[svc].get(
                'dependencies'), wz_json.services[svc], context=wz_context,wz_json=wz_json).to_str()
            file_system.wFile(file_system.join_path(
                wz_json.path, 'services', f'{svc}.ts'), service_code, overwrite=True)
        else:
            pretty.print_info("Make sure you are editing the {0} file\n - See how to edit service written in Typescript".format(file_system.join_path(
                wz_json.path, 'services', f'{svc}.ts')))

@builder.hookimpl
def compile_protos(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # Running ./bin/init.sh script for compiling protos
    pretty.print_note("Running ./bin/init-ts.sh script for 'protoc' compiler")
    proc = subprocess.run(['bash', file_system.join_path(
        wz_json.path, 'bin', 'init-ts.sh')])
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

@builder.hookimpl
def init_context(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    files = []
    pretty.print_error("Initialize webezy.context file")

    path = wz_json.project.get('uri')
    if wz_json.services is not None:
        for svc in wz_json.services:
            methods = []
            for rpc in wz_json.services[svc].get('methods'):
                rpc_name = rpc.get('name')
                rpc_type_out = rpc.get('serverStreaming')
                rpc_out_name = rpc.get('inputType').split('.')[-1]
                rpc_out_pkg = rpc.get('outputType').split('.')[1]
                rpc_output = rpc.get('outputType')
                msg = wz_json.get_message(rpc_output)
                fields = []
                for f in msg.get('fields'):
                    F_VALUE = 'null'
                    if f.get('fieldType') == 'TYPE_STRING':
                        F_VALUE = '"SomeString"'
                    elif f.get('fieldType') == 'TYPE_BOOL':
                        F_VALUE = 'false'
                    elif f.get('fieldType') == 'TYPE_INT32' or f.get('fieldType') ==  'TYPE_INT64':
                        F_VALUE = '1'
                    elif f.get('fieldType') == 'TYPE_FLOAT' or f.get('fieldType') == 'TYPE_DOUBLE':
                        F_VALUE = '1.0'

                    fields.append('{0}: {1}'.format(f.get('name'), F_VALUE))
                fields = ','.join(fields)
                if rpc_type_out:
                    out_prototype = f'\t\tcall.destroy(new ServiceError(status.UNIMPLEMENTED,"Method is not yet implemented"))'
                else:
                    out_prototype = f'\t\t// let response:{rpc_out_pkg}.{rpc_out_name} = {_OPEN_BRCK} {fields} {_CLOSING_BRCK};\n\t\t// callback(null,response);\n\t\tcallback(new ServiceError(status.UNIMPLEMENTED,"Method is not yet implemented"))'
                code = f'{out_prototype}\n'
                methods.append(protos.WebezyMethodContext(
                    name=rpc_name, code=code, type='rpc'))
            files.append(protos.WebezyFileContext(
                file=f'./services/{svc}.ts', methods=methods))
    context = resources.proto_to_dict(protos.WebezyContext(files=files))
    logging.debug("Writing new context")
    file_system.mkdir(file_system.join_path(path, '.webezy'))
    file_system.wFile(file_system.join_path(
        path, '.webezy', 'context.json'), context, json=True, overwrite=True)
    wz_json = helpers.WZContext(context)
    return context

@builder.hookimpl
def rebuild_context(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_note("Re-Building webezy.context")
    if wz_json.services is not None:
        for svc in wz_json.services:
            try:
                svcFile = file_system.rFile(file_system.join_path(
                    wz_json.path, 'services', f'{svc}.ts'))
                is_init = False
                for l in svcFile:
                    if '__init__' in l:
                        is_init = True
                        break
                # Non RPC functions should have # @skip line above func name
                function_code_inlines = helpers.parse_code_file(svcFile, '@skip')
                # Parse all rpc's in file by default # @rpc seperator
                rpc_code_inlines = helpers.parse_code_file(svcFile)
                for f in wz_context.files:

                    if svc in f.get('file'):
                        # Iterating all regular functions
                        for func in function_code_inlines:
                            func_code = []
                            for l in func:
                                if '@rpc @@webezyio' in l:
                                    break

                                func_code.append(l)
                            func_name = func_code[0].split(
                            '(')[0].split('private')
                            if len(func_name) > 1:
                                func_name = func_name[1].strip()
                            else:
                                func_name = func_name[0].strip()
                            wz_context.set_method_code(svc, func_name, ''.join(func_code))
                        methods_i = 0
                        for r in wz_json.services[svc]['methods']:
                            if next((m for m in f.get('methods') if m['name'] == r['name']),None) is None:
                                pretty.print_note(f"Starting new RPC at webezy,context [{r.get('name')}]")
                                new_rpc_context = {'name': r.get('name'), 'type': 'rpc', 'code': '\t\tbreak;'}
                                wz_context.new_rpc(svc, new_rpc_context, suffix='ts')
                        # Iterating all RPC's functions
                        for m in f.get('methods'):
                            if m['type'] == 'rpc':
                                # Checking if edit to method has happened - meaning canot find in webezy.json all context methods
                                if next((r for r in wz_json.services[svc]['methods'] if r['name'] == m['name']), None) == None:
                                    # Getting method details from webezy.json
                                    new_method = wz_json.services[svc]['methods'][methods_i]
                                    # Building new context with old func code
                                    new_rpc_context = {'name': new_method.get(
                                        'name'), 'type': 'rpc', 'code': ''.join(rpc_code_inlines[methods_i][1:])}
                                    # Editing inplace the RPC context
                                    wz_context.edit_rpc(
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
                                    wz_context.set_rpc_code(svc, m.get('name'), ''.join(
                                        temp_lines))

                                methods_i += 1

            except Exception as e:
                pretty.print_error(e)

    # pretty.print_note(wz_context.dump(),True)
    file_system.wFile(file_system.join_path(
        wz_json.path, '.webezy', 'context.json'), wz_context.dump(), True, True)

@builder.hookimpl
def write_server(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    imports = ['import { Server, ServerCredentials } from \'@grpc/grpc-js\';']
    services_bindings = []
    svcs = []
    for svc in wz_json.services:
        svcs.append(svc)
        imports.append(f'import {_OPEN_BRCK} {svc}, {svc}Service {_CLOSING_BRCK} from \'./services/{svc}\';')
        services_bindings.append(
            f'server.addService({svc}Service, new {svc}());')
    services_bindings = '\n\t'.join(services_bindings)
    imports = '\n'.join(imports)
    server_code = f'// Webezy.io Generated Server Code\n\
{imports}\n\n\
let _PORT:number = 50051;\n\
let _HOST:string = \'0.0.0.0\';\n\
let _ADDR = `${_OPEN_BRCK}_HOST{_CLOSING_BRCK}:${_OPEN_BRCK}_PORT{_CLOSING_BRCK}`\n\
const server = new Server({_OPEN_BRCK}\n\
	"grpc.max_receive_message_length": -1,\n\
	"grpc.max_send_message_length": -1,\n\
{_CLOSING_BRCK});\n\n\
{services_bindings}\n\n\
server.bindAsync(_ADDR, ServerCredentials.createInsecure(), (err: Error | null, bindPort: number) => {_OPEN_BRCK}\n\tif (err) {_OPEN_BRCK}\n\t\tthrow err;\n\t{_CLOSING_BRCK}\n\n\tconsole.log(`[webezy] Starting gRPC:server:${_OPEN_BRCK}bindPort{_CLOSING_BRCK}`,`at -> ${_OPEN_BRCK}new Date().toLocaleString(){_CLOSING_BRCK})`);\n\tserver.start();\n{_CLOSING_BRCK});'
   
    if file_system.check_if_file_exists(file_system.join_path(
            wz_json.path, 'server.ts')) == False:
        file_system.wFile(file_system.join_path(
            wz_json.path, 'server.ts'), server_code, overwrite=True)
    else:
        pretty.print_warning("Make sure you make desired changes on server.ts file !")
