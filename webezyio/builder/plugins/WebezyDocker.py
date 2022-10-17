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