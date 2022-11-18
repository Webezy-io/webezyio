import pluggy

from webezyio.commons.helpers import WZContext, WZJson
from webezyio.commons.protos.webezy_pb2 import WzResourceWrapper

hookspec = pluggy.HookspecMarker("builder")

@hookspec
def get_webezy_json(wz_json_path):
    """"""

@hookspec
def pre_build(wz_json: WZJson, wz_context: WZContext):
    """Run before build process"""

@hookspec
def init_project_structure(wz_json: WZJson, wz_context: WZContext):
    """The first method that the WebezyBuilder is calling"""

@hookspec
def write_services(wz_json: WZJson, wz_context: WZContext):
    """Write services"""

@hookspec
def write_protos(wz_json: WZJson, wz_context: WZContext):
    """Write proto files"""

@hookspec
def compile_protos(wz_json: WZJson, wz_context: WZContext):
    """compile proto files"""

@hookspec
def write_clients(wz_json: WZJson, wz_context: WZContext):
    """Write clients"""

@hookspec
def write_server(wz_json: WZJson, wz_context: WZContext):
    """Write clients"""

@hookspec
def write_readme(wz_json: WZJson, wz_context: WZContext):
    """Write README.md file"""

@hookspec
def rebuild_context(wz_json: WZJson, wz_context: WZContext):
    """Rebuild context from code files and by changes from webezy json"""

@hookspec
def override_generated_classes(wz_json: WZJson, wz_context: WZContext):
    """Override generated protobug classes"""

@hookspec
def post_build(wz_json: WZJson, wz_context: WZContext):
    """Run after complete build process"""


@hookspec
def init_context(wz_json:WZJson, wz_context: WZContext):
    """Init context object"""

@hookspec
def parse_protos_to_resource(protos_dir,project_name,server_language,clients,domain):
    """Parse .proto files into :class:`webezyio.commons.helpers.WZJson` object"""

@hookspec
def package_project(wz_json:WZJson, wz_context: WZContext):
    """Provide a packaging project methods / files / scripts"""