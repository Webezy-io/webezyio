import pluggy

from webezyio.commons.helpers import WZContext, WZJson

hookspec = pluggy.HookspecMarker("builder")

@hookspec
def init_project_structure(wz_json: WZJson):
    """The first method that the WebezyBuilder is calling"""

@hookspec
def write_services(wz_json: WZJson, wz_context: WZContext):
    """Write services"""

@hookspec
def write_protos(wz_json: WZJson):
    """Write proto files"""

@hookspec
def compile_protos(wz_json: WZJson):
    """compile proto files"""

@hookspec
def write_clients(wz_json: WZJson):
    """Write clients"""

@hookspec
def write_server(wz_json: WZJson):
    """Write clients"""

@hookspec
def write_readme(wz_json: WZJson):
    """Write README.md file"""

@hookspec
def rebuild_context(wz_json: WZJson, wz_context: WZContext):
    """Rebuild context from code files and by changes from webezy json"""

@hookspec
def override_generated_classes(wz_json: WZJson):
    """Override generated protobug classes"""