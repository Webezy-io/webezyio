"""Builder workflow"""
from webezyio import WebezyBuilder,WebezyMigrate
from webezyio.commons.protos.webezy_pb2 import Language
_PATH = "/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/migrate/webezy.json"
def main():
   # Init builder class with webezy.json file
   wzcoder = WebezyBuilder(path=_PATH,hooks=[WebezyMigrate])
   wzcoder.PreBuild()
   wzcoder.ParseProtosToResource(project_name='TEST-PROJECT',server_language='python',clients=[Language.PYTHON])
   wzcoder.PostBuild()
   
if __name__ == "__main__":
   main()