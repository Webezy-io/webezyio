import pluggy

from webezyio.commons.helpers import WZContext, WZJson

"""Core builder plugins hookspec"""
hookspec = pluggy.HookspecMarker("webezyio")

"""Custom plugins hook specs"""
plugin_hookspecs = pluggy.HookspecMarker("plugins")

@hookspec
def get_webezy_json(wz_json_path):
    """"""

@hookspec
def pre_build(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Run before build process"""

@hookspec
def post_build(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Run after complete build process"""

# ============================================================
#                       Setup hooks
# ============================================================

@hookspec
def init_project_structure(wz_json: WZJson, wz_context: WZContext,pre_data):
    """The first method that the WebezyBuilder is calling"""

# ============================================================
#                       Services hooks
# ============================================================

@hookspec
def pre_build_services(wz_json: WZJson, wz_context: WZContext):
    """"""

@hookspec
def write_services(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Write services"""

@hookspec
def post_build_services(wz_json: WZJson, wz_context: WZContext):
    """"""

# ============================================================
#                       Protos hooks
# ============================================================

@hookspec
def write_protos(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Write proto files"""

@hookspec
def compile_protos(wz_json: WZJson, wz_context: WZContext,pre_data):
    """compile proto files"""

# ============================================================
#                       Clients hooks
# ============================================================

@hookspec
def pre_build_clients(wz_json: WZJson, wz_context: WZContext):
    """Pre build hook for Write clients"""

@hookspec
def write_clients(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Write clients"""

@hookspec
def post_build_clients(wz_json: WZJson, wz_context: WZContext):
    """Post build hook for Write clients"""

# ============================================================
#                       Server hooks
# ============================================================

@hookspec
def pre_build_server(wz_json: WZJson, wz_context: WZContext):
    """Pre build hook for server generated code"""

@hookspec
def write_server(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Write clients"""

@hookspec
def post_build_server(wz_json: WZJson, wz_context: WZContext):
    """Post build hook of server generated code"""

# ============================================================
#                       Docs hooks
# ============================================================

@hookspec
def write_readme(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Write README.md file"""

# ============================================================
#                       Deprecated? hooks
# ============================================================

@hookspec
def rebuild_context(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Rebuild context from code files and by changes from webezy json"""

@hookspec
def init_context(wz_json:WZJson, wz_context: WZContext,pre_data):
    """Init context object"""

# ============================================================
#                       Workaround hooks
# ============================================================

@hookspec
def override_generated_classes(wz_json: WZJson, wz_context: WZContext,pre_data):
    """Override generated protobug classes"""

@hookspec
def parse_protos_to_resource(protos_dir,project_name,server_language,clients,domain):
    """Parse .proto files into :class:`webezyio.commons.helpers.WZJson` object"""

# ============================================================
#                       Packages hooks
# ============================================================

@hookspec
def package_project(wz_json:WZJson, wz_context: WZContext,pre_data):
    """Provide a packaging project methods / files / scripts"""


@hookspec
def process_plugin(wz_json:WZJson, wz_context:WZContext,pre_data):
    """Process any plugin model impl."""

@plugin_hookspecs
def init_packages(wz_json:WZJson, wz_context:WZContext,pre_data):
    """implement the initialization of webezy.io packages into webezy.json file"""

