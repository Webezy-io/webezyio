"""Builder workflow"""
from importlib.resources import path
import os
import sys
from webezyio import load_wz_json
from webezyio import WebezyBuilder,WebezyMigrate


from webezyio.commons.protos.webezy_pb2 import Language
_PATH = "/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/migrate/webezy.json"
def main():
   # Init builder class with webezy.json file
   wzcoder = WebezyBuilder(path=_PATH,hooks=[WebezyMigrate])
   wzcoder.PreBuild()
   wzcoder.ParseProtosToResource(project_name='TEST-PROJECT',server_language=Language.Name(Language.python),clients=[Language.python])
   wzcoder.PostBuild()
   
def test_extensions():
   if os.getcwd() not in sys.path:
      sys.path.append(os.getcwd())

   from clients import python as client
   wz_json = load_wz_json('/Users/amitshmulevitch/Projects/wz/webezyio/webezyio/tests/migrate/webezy.json')
   msg = client.SamplePackage.SampleMessage(ExtendedField=True)
   
   print(wz_json.get_extended_fields(msg.DESCRIPTOR.full_name))
   # print(dir(msg))
   # ext = msg.DESCRIPTOR.GetOptions() \
      # .Extensions[client.SamplePackage.ExtensionMessage.BoolExtend]
   # print(ext)
   for f in msg.DESCRIPTOR.fields:
      if getattr(msg,f.name) is not None:
         if f.has_options:
            print(f.GetOptions().Extensions[client.SamplePackage.ExtensionMessage.BoolExtend])
         break
   
if __name__ == "__main__":
   test_extensions()