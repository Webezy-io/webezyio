# Vendors
import logging

# Internal deps
from sylk.helpers import pretty

logging.basicConfig(
    level='ERROR',
    format=pretty.bcolors.OKCYAN+'[%(asctime)s] - %(filename)20s / %(funcName)25s() - %(name)s - %(levelname)7s -'+pretty.bcolors.ENDC+' %(message)s',
    datefmt='%Y%m%d-%H:%M:%S',
)