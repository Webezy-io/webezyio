import subprocess
from webezyio.commons.helpers import WZJson


def run_server(webezy_json:WZJson):
    subprocess.run(['bash',webezy_json.path+'/bin/run-server.sh'])
