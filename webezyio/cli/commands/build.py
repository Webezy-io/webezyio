from webezyio.builder.src.main import WebezyBuilder

def build_all(path:str):
    wzBuilder = WebezyBuilder(path=path)
    wzBuilder.BuildAll()

def build_code(path:str):
    wzBuilder = WebezyBuilder(path=path)
    wzBuilder.BuildOnlyCode()

def build_protos(path:str):
    wzBuilder = WebezyBuilder(path=path)
    wzBuilder.BuildOnlyProtos()