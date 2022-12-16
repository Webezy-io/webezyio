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
from webezyio.builder.plugins.static import gitignore_ts,package_json_webpack,bash_init_script_webpack


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    if file_system.check_if_file_exists(file_system.join_path(wz_json.path,'package.json')):
        pretty.print_info('Run the following commands :\n\t-> $ npm install grpc-web')
    else:
        if wz_json.get_server_language() != 'typescript':
            pretty.print_info('Writing package.json file for webpack plugin')
            file_system.wFile(file_system.join_path(wz_json.path,'package.json'),package_json_webpack.replace('REPLACEME',wz_json.project.get('packageName')))
    subprocess.run(['npm', 'install'])
    # subprocess.run(['go mod init',_format_go_package_name(wz_json.project.get('goPackage'))])
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    directories = [
        # Clients
        file_system.join_path(wz_json.path, 'clients', 'webpack')]

    for dir in directories:
        file_system.mkdir(dir)
    
   # Bin files
    file_system.wFile(file_system.join_path(
        wz_json.path, 'bin', 'init-webpack.sh'), bash_init_script_webpack)

    return [directories]

@builder.hookimpl
def compile_protos(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # Running ./bin/init-webpack.sh script for compiling protos
    logging.info("Running ./bin/init-webpack.sh script for 'protoc' compiler")
    subprocess.run(['bash', file_system.join_path(
        wz_json.path, 'bin', 'init-webpack.sh')])