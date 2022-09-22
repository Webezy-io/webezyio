import logging
import webezyio.builder as builder
from webezyio.commons import helpers,file_system,pretty


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


@builder.hookimpl
def post_build(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def get_webezy_json():
    pass