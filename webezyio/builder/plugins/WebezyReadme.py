from webezyio import builder
from webezyio.commons import helpers, file_system
import logging


@builder.hookimpl
def pre_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Starting webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(wz_json: helpers.WZJson, wz_context: helpers.WZContext):
    logging.debug("Finished webezyio build process %s plugin" % (__name__))


@builder.hookimpl
def write_readme(wz_json: helpers.WZJson):
    file_system.wFile(file_system.join_path(
        wz_json.path, 'README.md'), get_readme(wz_json), overwrite=True)


def get_readme(wz_json: helpers.WZJson):
    project_name = wz_json.project.get('name')
    index = {'services':[],'packages':[]}
    svcs = []
    for svc in wz_json.services:
        service = wz_json.services[svc]
        rpcs = []
        index['services'].append(service.get('name'))
        for rpc in service['methods']:
            rpc_name = rpc['name']
            type = 'Unary'
            _client_stream = False
            _server_stream = False
            if rpc.get('clientStreaming'):
                _client_stream = True
            if rpc.get('serverStreaming'):
                _server_stream = True
            if _client_stream and _server_stream:
                type = 'Bidi stream'
            elif _client_stream and _server_stream == False:
                type = 'Client stream'
            elif _client_stream == False and _server_stream:
                type = 'Server stream'
            in_type = rpc.get('inputType')
            out_type = rpc.get('outputType')
            in_type_name = in_type.split('.')[-1]
            out_type_name = out_type.split('.')[-1]

            rpcs.append(f'__{rpc_name}__ [{type}]\n- Input: [{in_type}](#{in_type_name})\n- Output: [{out_type}](#{out_type_name})')

        rpcs = '\n\n'.join(rpcs)
        svcs.append(f'## {svc}\n\n{rpcs}')
    
    pkgs = []
    for pkg in wz_json.packages:
        package = wz_json.packages[pkg]
        package_name = package['package']
        msgs = []
        index['packages'].append(package_name)
        for msg in package['messages']:
            msg_name = msg['name']
            fields = []
            for f in msg['fields']:
                field_name = f['name']
                f_type = f['fieldType']
                f_type = '[{0}](#{0})'.format(f['messageType'] .split('.')[-1]) if f['fieldType'] == 'TYPE_MESSAGE' else f_type
                f_type = '[{0}](#{0})'.format(f['enumType'].split('.')[-1]) if f['fieldType'] == 'TYPE_ENUM' else f_type
                f_desc = '' if f.get('description') is None else f.get('description')
                fields.append(f'__{field_name}__ [{f_type}]\n{f_desc}\n')
            fields = '\n'.join(fields)
            msg_desc = '' if msg.get('description') is None else '{0}\n'.format(msg.get('description')) 
            msgs.append(f'### {msg_name}\n{msg_desc}\n{fields}')
        msgs = '\n\n'.join(msgs)
        pkgs.append(f'## {package_name}\n\n{msgs}')
    
    pkgs = '\n\n'.join(pkgs)
    svcs = '\n\n'.join(svcs)
    temp_index = []
    for k in index:
        for i in index[k]:
            temp_i = i
            link = i
            if len(i.split('.')) > 1:
                temp_i = i.split('.')[1]
            temp_index.append(f'- [{temp_i}](#{link})')
    index = '\n'.join(temp_index)
    readme_file = f'# {project_name}\n\nThis project has been generated thanks to [```Webezy.io```](https://www.webezy.io) !\n\n# Index\n{index}\n\n# Services\n\n{svcs}\n\n# Packages\n\n{pkgs}\n\n\n__This project and README file has been created thanks to [webezy.io](https://www.webezy.io)__'
    return readme_file
