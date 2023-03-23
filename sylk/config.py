         
from sylk.commons.protos.SylkConfig_pb2 import SylkCliConfigs
"""
               ____  
   _______  __/ / /__
  / ___/ / / / / //_/
 (__  ) /_/ / / ,<   
/____/\__, /_/_/|_|  
     /____/ 
     
sylk cli module configuration"""
configs=SylkCliConfigs(
    host="localhost",
    port=50051,
    # Analytic gathering approval
    analytics=False,
    # First run flag
    first_run=False,
    token="macOS-12.6-arm64-arm-64bit:2023-03-22T22:50:48.956143",
    # Supported builtins templates
    sylk_templates = [
        "@sylk/Blank",
        # "@sylk/io",
        # "@sylk/SamplePy",
        # "@sylk/SampleTs",
        # "@sylk/PubSubTs",
        # "@sylk/HelloWorldPy",
        # "@sylk/HelloWorldTs"
    ]
)