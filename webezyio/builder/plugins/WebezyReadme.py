from webezyio import builder
from webezyio.commons import helpers,file_system
import logging

@builder.hookimpl
def pre_build(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Starting webezyio build process %s plugin" % (__name__))

@builder.hookimpl
def post_build(wz_json:helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Finished webezyio build process %s plugin" % (__name__))

@builder.hookimpl
def write_readme(wz_json: helpers.WZJson):
    file_system.wFile(file_system.join_path(wz_json.path,'README.md'),get_readme(wz_json),overwrite=True)


def get_readme(wz_json:helpers.WZJson):
    project_name = wz_json.project.get('name')
    readme_file = f'# {project_name}\n\nThis project has been generated thanks to [```Webezy.io```](https://www.webezy.io) !\n\n# Installation\n\n# Usage'
    return readme_file