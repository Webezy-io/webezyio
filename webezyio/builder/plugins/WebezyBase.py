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
from webezyio.commons import helpers,file_system,pretty
from webezyio.commons.errors import WebezyValidationError


@builder.hookimpl
def pre_build(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))

    directories = [
        # Clients
        file_system.join_path(wz_json.path,'clients'),
        file_system.join_path(wz_json.path,'services'),
        file_system.join_path(wz_json.path,'protos'),
        file_system.join_path(wz_json.path,'bin'),
        file_system.join_path(wz_json.path,'.webezy'),
        file_system.join_path(wz_json.path,'server'),
    ]
    for d in directories:
        file_system.mkdir(d)


@builder.hookimpl(hookwrapper=True)
def post_build(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))
    # all corresponding hookimpls are invoked here
    outcome = yield
    results = outcome.get_result()
    if results != []:
        pretty.print_info(results,True,'post_build')

@builder.hookimpl(hookwrapper=True)
def pre_build_server(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    # all corresponding hookimpls are invoked here
    outcome = yield
    # outcome.force_result([{'test':'test'}])
    results = outcome.get_result()

    inject_base_dependencies = None
    for s in wz_json.services:
        svc = wz_json.services[s]
        if svc.get('dependencies') is not None and len(svc.get('dependencies')) > 0:
            for d in svc.get('dependencies') :
                dependentSvc = wz_json.get_service(d.split('.')[1])
                if dependentSvc is not None:
                    if inject_base_dependencies is None:
                        inject_base_dependencies = {}
                    inject_base_dependencies[s] = d.split('.')[1]+'Impl'
    if inject_base_dependencies is not None:
        results.append({
            'webezyio.builder.plugins.WebezyTsServer:write_server():inject_service': inject_base_dependencies
        })
    if results != []:
        for impl in results:
            for mini_hook in impl:
                pretty.print_info(f'[pre_build_server] Found MiniHook: {mini_hook}')

@builder.hookimpl(hookwrapper=True)
def post_build_server(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    # all corresponding hookimpls are invoked here
    outcome = yield
    results = outcome.get_result()
    if results != []:
        for impl in results:
            for mini_hook in impl:
                pretty.print_info(f'[post_build_server] Found MiniHook: {mini_hook}')


@builder.hookimpl(hookwrapper=True)
def pre_build_clients(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    # all corresponding hookimpls are invoked here
    outcome = yield
    results = outcome.get_result()
    if results != []:
        for impl in results:
            for mini_hook in impl:
                pretty.print_info(f'[pre_build_clients] Found MiniHook: {mini_hook}')


@builder.hookimpl(hookwrapper=True)
def post_build_clients(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    # all corresponding hookimpls are invoked here
    outcome = yield
    results = outcome.get_result()
    if results != []:
        for impl in results:
            for mini_hook in impl:
                pretty.print_info(f'[post_build_clients] Found MiniHook: {mini_hook}')





@builder.hookimpl
def get_webezy_json():
    pass