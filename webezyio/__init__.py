import logging
"""Commons"""
from .commons.protos import WebezyPrometheus_pb2 as WebezyPrometheus,WebezyProxy_pb2 as WebezyProxy,WebezyTemplate_pb2 as WebezyTemplate, WebezyConfig_pb2 as WebezyConfig
from .commons import file_system as _fs,resources as _resources,helpers as _helpers,pretty as _pretty
from .commons.helpers import load_wz_json
logging.basicConfig(
    level='ERROR',
    format=_pretty.bcolors.OKCYAN+'[%(asctime)s] - %(filename)20s / %(funcName)25s() - %(name)s - %(levelname)7s -'+_pretty.bcolors.ENDC+' %(message)s',
    datefmt='%Y%m%d-%H:%M:%S',
)
"""builder"""
from .builder.src.main import WebezyBuilder
from .builder.plugins import WebezyBase, WebezyPy, WebezyTsServer,WebezyTsClient, WebezyProto, WebezyReadme, WebezyMigrate
"""architect"""
from .architect import WebezyArchitect
