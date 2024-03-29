# Copyright (c) 2022 sylk.build.

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
from sylk.builder.plugins.static import gitignore_go,bash_init_script_go,bash_run_server_script_go,utils_go


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
    # Utils
    file_system.wFile(file_system.join_path(
        sylk_json.path, 'services','utils', 'utils.go'), utils_go)
    # Utils Interfaces
    # file_system.wFile(file_system.join_path(
        # sylk_json.path, 'services','utils', 'interfaces.ts'), utils_interfaces)
    # package.json
    # file_system.wFile(file_system.join_path(sylk_json.path,'package.json'),package_json.replace('REPLACEME',sylk_json.project.get('packageName')))
    # Bin files
    services_protoc = []
    packages_protoc = []
    if sylk_json.services is not None:
        for s in sylk_json.services:
            services_protoc.append(s)
            if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path, 'services', 'protos', s)) == False:
                file_system.mkdir(file_system.join_path(sylk_json.path, 'services', 'protos',s))
            if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path, 'services', s)) == False:
                file_system.mkdir(file_system.join_path(sylk_json.path, 'services',s))
    if sylk_json.packages is not None:
        for p in sylk_json.packages:
            packages_protoc.append(sylk_json.packages[p].get('name'))
            if file_system.check_if_dir_exists(file_system.join_path(sylk_json.path, 'services', 'protos', sylk_json.packages[p].get('name'))) == False:
                file_system.mkdir(file_system.join_path(sylk_json.path, 'services', 'protos', sylk_json.packages[p].get('name')))

    # Bin files
    # file_system.wFile(file_system.join_path(
        # sylk_json.path, 'bin', 'init-go.sh'), bash_init_script_ts)
    # file_system.wFile(file_system.join_path(
        # sylk_json.path, 'bin', 'proto.js'), protos_compile_script_ts)

    # tsconfig.json
    # file_system.wFile(file_system.join_path(sylk_json.path, 'tsconfig.json'),main_ts_config)
    # file_system.wFile(file_system.join_path(sylk_json.path, 'services', 'protos', 'tsconfig.json'),protos_ts_config)
    
    if sylk_json.get_server_language() == 'go':
        file_system.wFile(file_system.join_path(
            sylk_json.path, 'bin', 'run-server.sh'), bash_run_server_script_go)
    
    # file_system.wFile(file_system.join_path(sylk_json.path,'.webezy','contxt.json'),'{"files":[]}')
    
    # .gitignore
    file_system.wFile(file_system.join_path(sylk_json.path,'.gitignore'),gitignore_go)

    return [directories]


@builder.hookimpl
def write_services(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    for svc in sylk_json.services:
        if file_system.check_if_file_exists(file_system.join_path(
            sylk_json.path, 'services',svc, f'{svc}.go')) == False:
            service_code = helpers.SylkServiceGo(sylk_json.project.get('packageName'), svc, sylk_json.services[svc].get(
                'dependencies'), sylk_json.services[svc], context=sylk_context,sylk_json=sylk_json).to_str()
            file_system.wFile(file_system.join_path(
                sylk_json.path, 'services',svc, f'{svc}.go'), service_code, overwrite=True)
        else:
            pretty.print_info("Make sure you are editing the {0} file\n - See how to edit service written in Go".format(file_system.join_path(
                sylk_json.path, 'services',svc, f'{svc}.go')))

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
    logging.info("Running ./bin/init-go.sh script for 'protoc' compiler")
    subprocess.run(['bash', file_system.join_path(
        sylk_json.path, 'bin', 'init-go.sh')])


_OPEN_BRCK = '{'
_CLOSING_BRCK = '}'


@builder.hookimpl
def write_server(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext,pre_data):
    pretty.print_error(pre_data,True,'pre_data')
    go_package_name = sylk_json.project.get('goPackage')
    imports = ['"log"','"fmt"','"flag"','"net"','"google.golang.org/grpc"']
    services_bindings = []
    for svc in sylk_json.services:
        imports.append(f'{svc}Servicer "{go_package_name}/services/protos/{svc}"')
        imports.append(f'{svc} "{go_package_name}/services/{svc}"')
        temp_svc_name = svc[0].capitalize() + svc[1:]
        services_bindings.append(
            f'{svc}Servicer.Register{temp_svc_name}Server(grpcServer, new({svc}.{temp_svc_name}));')
    services_bindings = '\n\t'.join(services_bindings)
    imports = '\n\t'.join(imports)
    server_code = f'// sylk.build Generated Server Code\n\
package main\n\n\
import (\n\t{imports}\n)\n\
var (\n\
	port = flag.Int("port", 50051, "The server port")\n\
)\n\n\
func main() {_OPEN_BRCK}\n\
\tflag.Parse()\n\
\tlis, err := net.Listen("tcp", fmt.Sprintf("localhost:%d", *port))\n\
\tif err != nil {_OPEN_BRCK}\n\
\t\tlog.Fatalf("Failed to listen: %v", err)\n\
\t{_CLOSING_BRCK}\n\
\tvar opts []grpc.ServerOption\n\
\tgrpcServer := grpc.NewServer(opts...)\n\
\t{services_bindings}\n\
\tlog.Printf("[sylk.build] Starting server (Go) at -> %d",*port)\n\
\tgrpcServer.Serve(lis)\n\
{_CLOSING_BRCK}'
   
    if file_system.check_if_file_exists(file_system.join_path(
            sylk_json.path,'server', 'server.go')) == False:
        file_system.wFile(file_system.join_path(
            sylk_json.path, 'server', 'server.go'), server_code, overwrite=True)
    else:
        pretty.print_warning("Make sure you make desired changes on server/server.go file !")
