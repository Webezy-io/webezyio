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

import subprocess
import webezyio.builder as builder
from webezyio.commons import helpers, file_system, resources,pretty
from webezyio.builder.plugins.static import gitignore_py


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # Bin files
    file_system.wFile(file_system.join_path(
        wz_json.path, 'Dockerfile'), get_dockerfile_content(wz_json))
    file_system.wFile(file_system.join_path(
        wz_json.path, 'docker-compose.yml'), get_dockercompose_content(wz_json))

@builder.hookimpl
def package_project(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Running docker build")


def get_dockerfile_content(wz_json: helpers.WZJson):
    sevrer_language = wz_json.project.get('server').get('language')
    if sevrer_language == 'python':
        return PYTHON_DOCKERFILE
    elif sevrer_language == 'typescript':
        return TYPESCRIPT_DOCKERFILE


def get_dockercompose_content(wz_json: helpers.WZJson):
    return PYTHON_DOCKERCOMPOSE.format(project=wz_json.project.get('packageName'))

TYPESCRIPT_DOCKERFILE = 'FROM node:16.3-alpine3.12\n\
WORKDIR / \n\
ADD . / \n\
RUN pwd\n\
RUN apk add --no-cache tini && npm i --target_arch=x64 --target_platform=linux\n\
CMD ["tini", "--", "./node_modules/.bin/ts-node", "server.ts"]'

PYTHON_DOCKERFILE = 'FROM python:3.9.12-slim\n\
RUN apt-get update && apt-get install python3 python3-pip -y libpq-dev gcc\n\
WORKDIR / \n\
ADD . / \n\
RUN pip3 install -r requirements.txt --no-cache-dir\n\
CMD ["bash","bin/run-server.sh"]'

PYTHON_DOCKERCOMPOSE = 'version: "3"\n\
services:\n\n\
  {project}-app:\n\
    build: ./'

