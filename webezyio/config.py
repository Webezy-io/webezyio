from webezyio.commons.protos import WebezyConfig
"""
                 _                           _        
 __      __ ___ | |__    ___  ____ _   _    (_)  ___  
 \ \ /\ / // _ \| '_ \  / _ \|_  /| | | |   | | / _ \ 
  \ V  V /|  __/| |_) ||  __/ / / | |_| | _ | || (_) |
   \_/\_/  \___||_.__/  \___|/___| \__, |(_)|_| \___/ 
                                   |___/              .configs

webezyio cli module configuration"""
configs=WebezyConfig(
    host="localhost",
    port=50051,
    # Analytic gathering approval
    analytics=False,
    # First run flag
    first_run=False,
    token="macOS-12.6-arm64-arm-64bit:2022-12-24T21:18:56.815297",
    # Supported builtins templates
    webezyio_templates = [
        "@webezyio/Blank",
        "@webezyio/io",
        "@webezyio/SamplePy",
        "@webezyio/SampleTs",
        "@webezyio/PubSubTs",
        "@webezyio/HelloWorldPy",
        "@webezyio/HelloWorldTs"
    ]
)