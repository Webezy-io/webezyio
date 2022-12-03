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
import webezyio.builder as builder
from webezyio.commons import helpers, file_system
from webezyio.commons.pretty import print_error, print_info


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'protos')):
        print_info("Starting webezyio build process %s plugin" % (__name__))
    else:
        file_system.mkdir(file_system.join_path(wz_json.path, 'protos'))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def write_protos(wz_json: helpers.WZJson):
    if wz_json.services is None:
        print_error("Not supporting building project without any services",True,'Build process error')
        exit(1)

    if wz_json.packages is None:
        print_error("Not supporting building project without any packages",True,'Build process error')
        exit(1)

    for svc in wz_json.services:
        if wz_json.services[svc].get('methods') is None:
            print_error(f"Cannot build service [{svc}] proto file with 0 RPC !")
            exit(1)

        svc_def = helpers.WZProto(svc, wz_json.services[svc].get(
            'dependencies'), wz_json.services[svc], description=wz_json.services[svc].get('description'),extensions=wz_json.services[svc].get('extensions'),wz_json=wz_json)
        logging.debug(f"Writing proto file for service: {svc}")
        file_system.wFile(file_system.join_path(
            wz_json.path, 'protos', f'{svc}.proto'), svc_def.__str__(), True)

    for pkg in wz_json.packages:
        pkg_name = wz_json.packages[pkg].get('name')
        pkg_full_name = package = wz_json.packages[pkg].get('package')
        if wz_json.packages[pkg].get('messages') is None:
            print_error(f"Cannot build package [{wz_json.packages[pkg].get('package')}] proto file with 0 Messages !")
            exit(1)
        pkg_def = helpers.WZProto(pkg_name,
                                  wz_json.packages[pkg].get('dependencies'),
                                  package=pkg_full_name,
                                  messages=wz_json.packages[pkg].get(
                                      'messages'),
                                  enums=wz_json.packages[pkg].get('enums'),
                                  extensions=wz_json.packages[pkg].get('extensions'),
                                  wz_json=wz_json)
        logging.debug(f"Writing proto file for package: {pkg_name}")
        file_system.wFile(file_system.join_path(
            wz_json.path, 'protos', f'{pkg_name}.proto'), pkg_def.__str__(), True)
