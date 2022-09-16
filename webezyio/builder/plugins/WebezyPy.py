import logging
import webezyio.builder as builder
from webezyio.commons import helpers,file_system

@builder.hookimpl
def init_project_structure(wz_json:helpers.WZJson):
    directories = [
        # Clients
        file_system.join_path(wz_json.path,'clients'),
        file_system.join_path(wz_json.path,'clients','python'),
        # Server
        file_system.join_path(wz_json.path,'server'),
        # Services
        file_system.join_path(wz_json.path,'services'),
        # Protos
        file_system.join_path(wz_json.path,'protos'),
        # Bin
        file_system.join_path(wz_json.path,'bin')]

    for dir in directories:
        file_system.mkdir(dir)
    
    # Init files
    files = [
        file_system.join_path(wz_json.path,'services','__init__.py'),
        file_system.join_path(wz_json.path,'clients','python','__init__.py'),
        file_system.join_path(wz_json.path,'protos','__init__.py')]

    file_system.wFile(file_system.join_path(wz_json.path,'bin','init.sh'),bash_script)

    for file in files:
        file_system.wFile(file,'')

    return [directories,files]


@builder.hookimpl
def write_services(wz_json:helpers.WZJson):
    pass


@builder.hookimpl
def compile_protos(wz_json:helpers.WZJson):
    pass

@builder.hookimpl
def write_clients(wz_json:helpers.WZJson):
    pass


bash_script = '#!/bin/bash\n\n\
declare -a services=("protos")\n\
echo "Init started for proto files"\n\
pwd\n\
DESTDIR="./protos"\n\
for SERVICE in "${services[@]}"; do\n\
    # mkdir -p $DESTDIR\n\
    echo $SERVICE\n\
    python3 -m grpc_tools.protoc --proto_path=$SERVICE/ --python_out=$DESTDIR --grpc_python_out=$DESTDIR $SERVICE/*.proto\n\
done\n\
statuscode=$?\n\
echo "Exit code for protoc -> "$statuscode\n\
cd $DESTDIR\n\
for FILE in *; do\n\
    filename=$FILE\n\
    search="import"\n\
    replace="from . import"\n\
    sed -i".bak" -e "4,20s/^$search/$replace/gi" $filename\n\
    rm -f *.bak\n\
done'