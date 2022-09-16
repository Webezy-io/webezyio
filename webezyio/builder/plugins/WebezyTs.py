import logging
import webezyio.builder as builder
from webezyio.commons import helpers

@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson):
    print(wz_json,"ts")
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