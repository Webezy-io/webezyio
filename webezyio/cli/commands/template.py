from tkinter import N
from webezyio.architect import WebezyArchitect
from webezyio.cli import theme
from webezyio.commons.helpers import WZJson,MessageToDict
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success

_OPEN_BRCK = '{'
_CLOSING_BRCK = '}'

def parse_wz_json():
    pass

def create_webezy_template_py(wz_json:WZJson):
    host = wz_json._config.get('host')
    port = wz_json._config.get('port')
    project_pkg_name = wz_json.project['packageName']
    project_name = wz_json.project['name']
    clients = wz_json.project.get('clients')

    messages = []
    for pkg in wz_json.packages:
        p = wz_json.packages[pkg]
        for m in p.get('messages'):
            messages.append(m)

    return f'{create_init(project_pkg_name)}{create_constants(host=host,port=port,project_name=project_name,domain=wz_json.domain,server_language=wz_json.get_server_language())}{create_clients(clients)}{add_project()}{create_fields(messages)}{create_msgs(messages)}{create_pckgs(wz_json.packages)}{add_packgs(wz_json.packages)}{add_msgs(wz_json.packages)}{add_enums(wz_json.packages)}{create_rpcs(wz_json.services)}{create_services(wz_json.services)}{add_services(wz_json.services)}{add_rpcs(wz_json.services)}{save_architect()}'

def create_init(project_name:str='webezy.io'):
    return """
\"\"\"Init script for webezy.io template {0}
Generated thanks to -
{1}
\"\"\"
# Main webezyio class to create gRPC services programmatically
# (Same inteface that webezyio cli is built as wrapper for
# WebezyArchitect whenever you generate new resource / create new project)
from webezyio.architect import WebezyArchitect

# Some common utils modules to help us build the services faster
# and adds an validations to object before they created
from webezyio.commons import helpers, file_system

# Webezy proto modules also helps us here to construct our services
# gRPC used to create another gRPC ! :)
from webezyio.commons.protos.webezy_pb2 import Language

# Default system imports
import os
import sys

    """.format(project_name,theme.logo_ascii_art)

def create_constants(domain, project_name, server_language:str='python', host:str = 'localhost', port:int = 50051):
    return f"""
\"\"\"Initialize constants and WebezyArchitect class\"\"\"
# Constants
_PATH = file_system.join_path(os.getcwd(), 'webezy.json') 
_DOMAIN = '{domain}'
_PROJECT_NAME = '{project_name}'
_SERVER_LANGUAGE = Language.Name(Language.{server_language})
_HOST = '{host}'
_PORT = {port}

# Initializing WebezyArchitect class which we going to interact with
# It is used to create all of our 'webezyio' resources
_architect = WebezyArchitect(path=_PATH,
                             domain=_DOMAIN,
                             project_name=_PROJECT_NAME)
_architect.SetConfig({_OPEN_BRCK}'host': _HOST, 'port': _PORT{_CLOSING_BRCK})
_architect.SetDomain(_DOMAIN)
    
\"\"\"Project specific configurations\"\"\"
    """

def create_clients(clients):
    temp_clients = []
    langauges = []
    for c in clients:
        temp_clients.append({'language':c['language'],'out_dir':'file_system.join_path(_PATH, \'clients\', Language.Name(Language.{0}))'.format(c['language'])})
        langauges.append(c['language'])
    return """
# Init all the client to be used with your services
# Here we configured a {1} clients to be created with our services    
_clients = {0}
    """.format(temp_clients,' + '.join(langauges)).replace('"','')


def add_project():
    return """
# Adding the base project data
_project = _architect.AddProject(server_language=_SERVER_LANGUAGE,
                                 clients=_clients)
    """

def create_fields(messages):
    fields = {}
    for m in messages:
        
        fields[m.get('fullName')] = []
        for f in  m.get('fields'):
            field = '\n_field_{4} = helpers.WZField(name=\'{0}\',\n\
                              description=\'{1}\',\n\
                              label=\'{2}\',\n\
                              type=\'{3}\')\n'.format(f.get('name'),f.get('description'),f.get('label'),f.get('fieldType'),f.get('fullName').replace('.','_'))
            fields[m.get('fullName')].append((f.get('fullName').replace('.','_'),field))

    code = ''

    for k in fields:
        msg = k
        msg_fields = []
        for f in fields[msg]:
            msg_fields.append(f[1])
        code += ''.join(msg_fields)
    for m in messages:
        temp_fields = []
        for f in m.get('fields'):
            temp_fields.append('_field_{0}'.format(f.get('fullName').replace('.','_')))
        code += '\n_msg_fields_{0} = [{1}]'.format(m.get('fullName').replace('.','_'),','.join(temp_fields))
        
    return """
\"\"\"Packages and thier resources\"\"\"
# Construct fields    
{0}
    """.format(code)

def create_msgs(messages):
    code = ''
    for m in messages:
        code += '\n_msg_{0} = helpers.WZMessage(name=\'{1}\',\n\
                                 description=\'{2}\',\n\
                                 fields=_msg_fields_{0})\n'.format(m.get('fullName').replace('.','_'),m.get('name'),m.get('description'))
    return """
# Construct messages
{0}
    """.format(code)

def create_pckgs(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        msgs = []
        for m in pkg.get('messages'):
            msgs.append('_msg_{0}'.format(m.get('fullName').replace('.','_')))
        code += '\n_pkg_{0} = helpers.WZPackage(name=\'{1}\',\n\
                                                messages=[{2}],\n\
                                                enums=[])\n\
\n_pkg_{0}_name, _pkg_{0}_messages, _pkg_{0}_enums = _pkg_{0}.to_tuple()'.format(pkg.get('package').replace('.','_'),pkg.get('name'),','.join(msgs))
    return """
# Construct packages
{0}
    """.format(code)

def add_packgs(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        code += '\n_pkg_{0} = _architect.AddPackage(_pkg_{0}_name,\n\
                                                    dependencies=[],\n\
                                                    description=\'{1}\')'.format(pkg.get('package').replace('.','_'),pkg.get('description'))
    return """
# Add packages
{0}
    """.format(code)

def add_msgs(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        code += '\nfor m in _pkg_{0}_messages:\n\
\tmsg_name, msg_fields, msg_desc, msg_opt = m\n\
\ttemp_msg = _architect.AddMessage(_pkg_{0}, msg_name, msg_fields, msg_desc, msg_opt)\n\
\tmsgs_map[temp_msg.full_name] = temp_msg'.format(pkg.get('package').replace('.','_'))
    return """
msgs_map = {1}{2}

# Add packages messages
{0}
    """.format(code,_OPEN_BRCK,_CLOSING_BRCK)

def add_enums(packages):
    code = ''
    for p in packages:
        pkg = packages[p]
        code += '\nfor e in _pkg_{0}_enums:\n\
\tenum_name, enum_values, enum_desc = e\n\
\t_architect.AddEnum(_pkg_{0}, enum_name, enum_values, enum_desc)'.format(pkg.get('package').replace('.','_'))
    return """
# Add packages enums
{0}
    """.format(code,_OPEN_BRCK,_CLOSING_BRCK)

def create_rpcs(services):
    code = ''
    for s in services:
        svc = services.get(s)
        for rpc in svc.get('methods'):
            code += '\n_rpc_{0}_{4} = helpers.WZRPC(name=\'{4}\', in_type=msgs_map[\'{1}\'].full_name, out_type=msgs_map[\'{2}\'].full_name, description=\'{3}\')'.format(svc.get('fullName').replace('.','_'),rpc.get('inputType'),rpc.get('outputType'),rpc.get('description'),rpc.get('name'))
    return """
\"\"\"Services and thier resources\"\"\"
# Construct rpc's
{0}
    """.format(code)

def create_services(services):
    code = ''
    for s in services:
        svc = services[s]
        temp_rpcs = []
        for rpc in svc.get('methods'):
            temp_rpcs.append('_rpc_{0}_{1}'.format(svc.get('fullName').replace('.','_'),rpc.get('name'))) 

        temp_dependencies = []
        for d in svc.get('dependencies'):
            temp_dependencies.append('_pkg_{0}.package'.format(d.replace('.','_')))

        code += '_svc_{0} = helpers.WZService(\'{0}\',\n\
                                              methods=[{1}],\n\
                                              dependencies=[{2}],\n\
                                              description=\'{3}\')\n\
\n_svc_{0}_name, _svc_{0}_methods, _svc_{0}_dependencies, _svc_{0}_desc = _svc_{0}.to_tuple()'.format(svc.get('name'),','.join(temp_rpcs),','.join(temp_dependencies),svc.get('description'))

    return """
# Construct services
{0}
    """.format(code)

def add_services(services):
    code = ''
    for s in services:
        svc = services[s]
        code += '_svc_{0} = _architect.AddService(_svc_{0}_name,_svc_{0}_dependencies,_svc_{0}_desc,[])'.format(svc.get('name'))

    return """
# Add services
{0}
    """.format(code)


def add_rpcs(services):
    code = ''
    for s in services:
        svc = services[s]
        code += 'for rpc in _svc_{0}_methods:\n\
\trpc_name, rpc_in_out, rpc_desc = rpc\n\
\t_architect.AddRPC(_svc_{0}, rpc_name, rpc_in_out, rpc_desc)'.format(svc.get('name'))            
    return """
{0}
    """.format(code)

def save_architect():
    return """
_architect.Save()
    """