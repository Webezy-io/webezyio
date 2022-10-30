import logging
import subprocess
import webezyio.builder as builder
from webezyio.commons import helpers, file_system, resources,pretty
from webezyio.builder.plugins.static import gitignore_py


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    pretty.print_info("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # TODO add postbuild validation of generated code
    pretty.print_success("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def init_project_structure(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    directories = [
        # Clients
        file_system.join_path(wz_json.path, 'clients', 'python'),
        # Protos
        file_system.join_path(wz_json.path, 'services', 'protos')]

    for dir in directories:
        file_system.mkdir(dir)

    # Init files
    files = [
        file_system.join_path(wz_json.path, 'services', '__init__.py'),
        file_system.join_path(wz_json.path, 'clients',
                              'python', '__init__.py'),
        file_system.join_path(wz_json.path, 'protos', '__init__.py')]
    # Bin files
    file_system.wFile(file_system.join_path(
        wz_json.path, 'bin', 'init-py.sh'), bash_init_script)
    
    # file_system.wFile(file_system.join_path(wz_json.path,'.webezy','contxt.json'),'{"files":[]}')
    # .gitignore
    file_system.wFile(file_system.join_path(wz_json.path,'.gitignore'),gitignore_py)
    for file in files:
        file_system.wFile(file, '')

    return [directories, files]

@builder.hookimpl
def compile_protos(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    # Running ./bin/init.sh script for compiling protos
    logging.info("Running ./bin/init-py.sh script for 'protoc' compiler")
    proc = subprocess.run(['bash', file_system.join_path(
        wz_json.path, 'bin', 'init-py.sh')])
    if proc.returncode != 0:
        pretty.print_error("ERROR occured during building process some more info on specific error can be found above")
        exit(proc.returncode)
    # Moving .py files to ./services/protos dir
    for file in file_system.walkFiles(file_system.join_path(wz_json.path, 'protos')):
        if '.py' in file:
            file_system.mv(file_system.join_path(wz_json.path, 'protos', file),
                           file_system.join_path(wz_json.path, 'services', 'protos', file))


@builder.hookimpl
def write_clients(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    for f in file_system.walkFiles(file_system.join_path(wz_json.path, 'services', 'protos')):
        if '.py' in f:
            file = file_system.rFile(file_system.join_path(
                wz_json.path, 'services', 'protos', f))
            if '_grpc' not in f:
                index = 13
            else:
                index = 0
            for l in file[index:]:

                if 'import ' in  l and 'grpc' not in l and 'typing' not in l and 'google.protobuf' not in l:
                    file[index] = l.replace('import ','from . import ')

                index += 1
            file_system.wFile(file_system.join_path(wz_json.path, 'clients', 'python', f), ''.join(file),True)

    client = helpers.WZClientPy(wz_json.project.get(
        'packageName'), wz_json.services, wz_json.packages, wz_context)
    file_system.wFile(file_system.join_path(
        wz_json.path, 'clients', 'python', '__init__.py'), client.__str__(), overwrite=True)

@builder.hookimpl
def override_generated_classes(wz_json: helpers.WZJson, wz_context: helpers.WZContext):

    for f in file_system.walkFiles(file_system.join_path(wz_json.path, 'services', 'protos')):
        name = f.split('_pb2')
        if '_grpc' not in name:
            file_content = file_system.rFile(
                file_system.join_path(wz_json.path, 'services', 'protos', f))
            file_content.insert(
                5, '\nfrom typing import overload, Iterator, List\n')
            if len(name) > 1:
                name = name[0]

                # svc_proto = next((svc for svc in wz_json.services if svc == name),None)
                pkg_proto = next((pkg for pkg in wz_json.packages if pkg.split(
                    '/')[-1].split('.')[0] == name), None)
                if pkg_proto is not None:
                    pkg_proto_name = pkg_proto.split('/')[-1].split('.')[0]

                    for m in wz_json.packages[pkg_proto].get('messages'):
                        index = 0
                        for l in file_content:
                            message_name = m['name']
                            if f'{message_name} = _reflection' in l:
                                temp_fields = []
                                init_fields = []
                                # pretty.print_info(init_fields)
                                for field in m['fields']:

                                    fName = field['name']
                                    fType = parse_proto_type_to_py(field['fieldType'].split(
                                        '_')[-1].lower(), field['label'].split('_')[-1].lower(), field.get('messageType'), field.get('enumType'),current_pkg=pkg_proto_name)
                                    if field['fieldType'].split(
                                        '_')[-1].lower() == 'enum':
                                        temp_fields.append(
                                            f'{fName} = {fType} # type: enum_type_wrapper.EnumTypeWrapper')
                                    else:
                                        temp_fields.append(
                                            f'{fName} = {fType} # type: {fType}')
                                    init_fields.append(f'{fName}={fType}')
                                temp_fields = '\n\t'.join(temp_fields)
                                init_fields = ', '.join(init_fields)
                                file_content.insert(
                                    index, f'\n@overload\nclass {message_name}:\n\t"""webezyio generated message [{wz_json.domain}.{pkg_proto_name}.v1.{message_name}]\n\tA class respresent a {message_name} type\n\t"""\n\t{temp_fields}\n\n\tdef __init__(self, {init_fields}):\n\t\tpass\n')
                                break
                            index += 1
                    file_system.wFile(file_system.join_path(
                        wz_json.path, 'services', 'protos', f), ''.join(file_content), True)

bash_init_script = '#!/bin/bash\n\n\
declare -a services=("protos")\n\
echo "[WEBEZYIO] proto-py.sh starting protoc compiler"\n\
DESTDIR="./protos"\n\
for SERVICE in "${services[@]}"; do\n\
    python3 -m grpc_tools.protoc --proto_path=$SERVICE/ --python_out=$DESTDIR --grpc_python_out=$DESTDIR $SERVICE/*.proto\n\
done\n\
statuscode=$?\n\
echo "Exit code for protoc -> "$statuscode\n\
exit 0'

def parse_proto_type_to_py(type, label, messageType=None, enumType=None,current_pkg=None):
    temp_type = 'None'
    if 'int' in type:
        temp_type = 'int'
    elif type == 'float' or type == 'double':
        temp_type = 'float'
    elif type == 'string':
        temp_type = 'str'
    elif type == 'byte':
        temp_type = 'bytes'
    elif type == 'message':
        # pretty.print_info(current_pkg)
        if messageType.split('.')[1] != current_pkg:
            if messageType.split('.')[1] == 'protobuf':
                temp_type = 'google_dot_protobuf_dot_{0}__pb2.{1}'.format(messageType.split('.')[-1].lower(),messageType.split('.')[-1])
            else:
                temp_type = '{0}__pb2.{1}'.format(
                    messageType.split('.')[1], messageType.split('.')[-1])
        else:
            temp_type = '{1}'.format(
                messageType.split('.')[1], messageType.split('.')[-1])
    elif type == 'enum':
        if enumType.split('.')[1] != current_pkg:
            temp_type = '{0}__pb2.{1}'.format(
                enumType.split('.')[1], enumType.split('.')[-1])
        else:
            temp_type = '{1}'.format(
                enumType.split('.')[1], enumType.split('.')[-1])
    elif type == 'bool':
        temp_type = 'bool'

    if label == 'repeated':
        temp_type = f'List[{temp_type}]'

    return temp_type

