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
from webezyio.commons.config import parse_project_config


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # Bin files
    # file_system.wFile(file_system.join_path(
    #     wz_json.path, 'Dockerfile'), get_dockerfile_content(wz_json))
    # file_system.wFile(file_system.join_path(
    #     wz_json.path, 'docker-compose.yml'), get_dockercompose_content(wz_json))

    print(get_dockercompose_content(wz_json))

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

    prj_configs = parse_project_config(wz_json.path)
    pretty.print_info(prj_configs,True)
    envoy_yaml_path = prj_configs.get('proxyPath') if  prj_configs.get('proxyPath') is not None else './proxy/envoy.yaml'
    envoy_proxy = PROXY_DOCKER_SERVICE.format(project=wz_json.project.get('packageName'),envoy_yaml=envoy_yaml_path)
    if prj_configs.get('monitor'):
        grafana_root_dir = prj_configs.get('grafanaPath') if  prj_configs.get('grafanaPath') is not None else './grafana'
        grafana = GRAFANA_DOCKER_SERVICE.format(grafana=grafana_root_dir)
        prom_config_yaml =  prj_configs.get('prometheusPath') if  prj_configs.get('prometheusPath') is not None else './prometheus/config.yaml'
        prom = PROMETHEUS_DOCKER_SERVICE.format(prom_yaml=prom_config_yaml)
        statsd = STATSD_EXPORTER_DOCKER_SERVICE.format(project=wz_json.project.get('packageName'))
    else:
        grafana = ''
        prom = ''
        statsd = ''

    docker_compose_file = DOCKER_COMPOSE+APP_DOCKER_SERVICE.format(project=wz_json.project.get('packageName'),port=prj_configs.get('port'))+envoy_proxy+grafana+prom+statsd
    return docker_compose_file

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

DOCKER_COMPOSE = 'version: "3"\n\
services:\n\n'

APP_DOCKER_SERVICE = '\t{project}-app:\n\
\t\trestart: always\n\
\t\tcontainer_name: {project}-app\n\
\t\tbuild: ./\n\
\t\tports:\n\
\t\t\t- {port}:{port}\n\
\t\tvolumes:\n\
\t\t\t- ./:/app\n\n'

PROXY_DOCKER_SERVICE = '\tproxy:\n\
\t\tcontainer_name: proxy\n\
\t\timage: envoyproxy/envoy-alpine:v1.21-latest\n\
\t\tvolumes:\n\
\t\t\t- {envoy_yaml}:/etc/envoy/envoy.yaml\n\
\t\tcommand: /usr/local/bin/envoy -c /etc/envoy/envoy.yaml --service-cluster {project}_service --service-node {project}_service\n\
\t\tports:\n\
\t\t\t- "9000:9000"\n\
\t\t\t- "9900:9900"\n\n'

GRAFANA_DOCKER_SERVICE = '\tgrafana:\n\
\t\tcontainer_name: grafana\n\
\t\timage: grafana/grafana\n\
\t\tenvironment:\n\
\t\t\t- GF_SECURITY_ADMIN_USER=admin\n\
\t\t\t- GF_SECURITY_ADMIN_PASSWORD=admin\n\
\t\tuser: \'104\'\n\
\t\tports:\n\
\t\t\t- "3000:3000"\n\
\t\tvolumes:\n\
\t\t\t- {grafana}:/var/lib/grafana\n\
\t\t\t- {grafana}/provisioning:/etc/grafana/provisioning\n\n'

PROMETHEUS_DOCKER_SERVICE = '\tprometheus:\n\
\t\tcontainer_name: prometheus\n\
\t\timage: prom/prometheus\n\
\t\tvolumes:\n\
\t\t\t- {prom_yaml}:/etc/prometheus.yaml\n\
\t\tports:\n\
\t\t\t- "9090:9090"\n\
\t\tcommand: "--config.file=/etc/prometheus.yaml"\n\n'

STATSD_EXPORTER_DOCKER_SERVICE = '\tstatsd_exporter_{project}:\n\
\t\tcontainer_name: statsd-exporter\n\
\t\timage: prom/statsd-exporter:latest\n\
\t\tcommand: ["--statsd.listen-tcp=:9125","--web.listen-address=:9102"]\n\
\t\tports:\n\
\t\t\t- "9125:9125"\n\
\t\t\t- "9102:9102"\n\n'