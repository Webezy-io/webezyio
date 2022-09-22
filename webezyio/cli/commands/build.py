from webezyio.builder.src.main import WebezyBuilder


def build_all(path:str):
    wzBuilder = WebezyBuilder(path=path)
    wzBuilder.BuildAll()