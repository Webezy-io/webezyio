import webezyio.builder as builder
from webezyio.commons import helpers

import logging


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson):
    return ["ts"]


@builder.hookimpl
def write_services(wz_json: helpers.WZJson):
    pass


@builder.hookimpl
def write_protos(wz_json: helpers.WZJson):
    pass


@builder.hookimpl
def compile_protos(wz_json: helpers.WZJson):
    pass


@builder.hookimpl
def write_clients(wz_json: helpers.WZJson):
    pass
