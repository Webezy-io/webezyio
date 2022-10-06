import logging
import webezyio.builder as builder
from webezyio.commons import helpers, file_system
from webezyio.commons.pretty import print_error


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    if file_system.check_if_dir_exists(file_system.join_path(wz_json.path, 'protos')):
        logging.debug("Starting webezyio build process %s plugin" % (__name__))
    else:
        file_system.mkdir(file_system.join_path(wz_json.path, 'protos'))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def write_protos(wz_json: helpers.WZJson):
    if wz_json.services is None:
        print_error("Cannot build project without services !")
        exit(1)

    if wz_json.packages is None:
        print_error("Cannot build project without packages !")
        exit(1)

    for svc in wz_json.services:
        if wz_json.services[svc].get('methods') is None:
            print_error(f"Cannot build service [{svc}] proto file with 0 RPC !")
            exit(1)

        svc_def = helpers.WZProto(svc, wz_json.services[svc].get(
            'dependencies'), wz_json.services[svc], description=wz_json.services[svc].get('description'))
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
                                  enums=wz_json.packages[pkg].get('enums'))
        logging.debug(f"Writing proto file for package: {pkg_name}")
        file_system.wFile(file_system.join_path(
            wz_json.path, 'protos', f'{pkg_name}.proto'), pkg_def.__str__(), True)
