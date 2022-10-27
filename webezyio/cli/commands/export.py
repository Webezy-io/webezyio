from webezyio.architect import WebezyArchitect
from webezyio.commons.helpers import WZJson,MessageToDict
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success

def parse_wz_json():
    pass

def create_webezy_template_py():
    return f'{create_init()}{create_constants()}{create_clients()}{create_fields()}{create_msgs()}{add_msgs()}{create_pckgs()}{add_packgs()}{create_rpcs()}{add_rpcs()}{create_services()}{add_services()}{save_architect()}'

def create_init():
    return """
\"\"\"Init script for webezy.io platform services\"\"\"
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

    """

def create_constants():
    return """
\"\"\"Initialize constants and WebezyArchitect class\"\"\"
# Constants
_PATH = file_system.join_path(os.getcwd(), 'webezy.json') 
_DOMAIN = 'webezy'
_PROJECT_NAME = 'webezy-platform'
_SERVER_LANGUAGE = Language.Name(Language.python)

# Initializing WebezyArchitect class which we going to interact with
# It is used to create all of our 'webezyio' resources
_architect = WebezyArchitect(path=_PATH,
                             domain=_DOMAIN,
                             project_name=_PROJECT_NAME)
_architect.SetConfig({'host': 'localhost', 'port': 50051})
_architect.SetDomain('webezy')
print(helpers.wzJsonToMessage(_architect._webezy._webezy_json))
    """

def create_clients():
    return """
\"\"\"Project specific configurations\"\"\"
# Init all the client to be used with your services
# Here we configured a python + typescript clients to be created with our services    

    """

def create_fields():
    return """
\"\"\"Packages and thier resources\"\"\"
# Construct fields    

    """

def create_msgs():
    return """
# Construct messages
    """

def add_msgs():
    pass

def create_pckgs():
    return """
# Construct packages
    """

def add_packgs():
    pass

def create_rpcs():
    return """
\"\"\"Services and thier resources\"\"\"
# Construct rpc's
    """

def add_rpcs():
    pass

def create_services():
    return """
# Construct services
    """

def add_services():
    pass

def save_architect():
    return """
_architect.Save()
    """