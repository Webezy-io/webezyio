import logging
"""Commons"""
from .commons.protos.webezy_pb2 import Options as extensionOpt
from .commons import file_system as _fs,resources as _resources,helpers as _helpers,pretty as _pretty
logging.basicConfig(
    level='DEBUG',
    format=_pretty.bcolors.OKCYAN+'%(asctime)s - [%(filename)15s] - %(funcName)20s() - %(name)s - %(levelname)s -'+_pretty.bcolors.ENDC+' %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)
"""builder"""
from .builder.src.main import WebezyBuilder
from .builder.plugins import WebezyPy, WebezyTs, WebezyProto, WebezyReadme
"""architect"""
from .architect import WebezyArchitect

