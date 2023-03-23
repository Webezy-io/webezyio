# Copyright (c) 2023 sylk.build

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from sylk import builder
from sylk.commons import helpers, file_system,pretty
import logging


@builder.hookimpl
def pre_build(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    pretty.print_info("Starting sylk build process %s plugin" % (__name__))


@builder.hookimpl
def post_build(sylk_json: helpers.SylkJson, sylk_context: helpers.SylkContext):
    pretty.print_success("Finished sylk build process %s plugin" % (__name__))
    return (__name__,'OK')


@builder.hookimpl
def write_readme(sylk_json: helpers.SylkJson):
    file_path = 'README.md' 
    if sylk_json._config.get('docs') is not None:
        alt_path = sylk_json._config.get('docs').get('file')
        file_path = file_path if alt_path is None else alt_path
    file_system.wFile(file_system.join_path(
        sylk_json.path, file_path), get_readme(sylk_json), overwrite=True)

_OPEN_BRCK = '{'
_CLOSING_BRCK = '}'

def get_readme(sylk_json: helpers.SylkJson):
    project_name = sylk_json.project.get('name')
    index = {'services':[],'packages':[]}
    project_package_name = sylk_json.project.get('packageName')

    svcs = []
    for svc in sylk_json.services:
        service = sylk_json.services[svc]
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
            in_type_name = in_type.split('.')[-1].lower()
            out_type_name = out_type.split('.')[-1].lower()

            rpcs.append(f'__`{rpc_name}`__ [{type}]\n- Input: [{in_type}](#{in_type_name})\n- Output: [{out_type}](#{out_type_name})')

        rpcs = '\n\n'.join(rpcs)
        svcs.append(f'## {svc}\n\n{rpcs}')
    
    pkgs = []
    for pkg in sylk_json.packages:
        package = sylk_json.packages[pkg]
        package_name = package['package']
        msgs = []
        index['packages'].append(package_name)
        for msg in package['messages']:
            msg_name = msg['name']
            fields = []
            for f in msg['fields']:
                field_name = f['name']
                f_type = f['fieldType']
                f_type = '[{0}](#{0})'.format(f['messageType'].split('.')[-1]) if f['fieldType'] == 'TYPE_MESSAGE' else f_type
                f_type = '[{0}](#{0})'.format(f['enumType'].split('.')[-1]) if f['fieldType'] == 'TYPE_ENUM' else f_type
                f_desc = '' if f.get('description') is None else f.get('description')
                fields.append(f'* __{field_name}__ [{f_type}]\n{f_desc}\n')
            fields = '\n'.join(fields)
            msg_desc = '' if msg.get('description') is None else '{0}\n'.format(msg.get('description')) 
            msgs.append(f'\n<details id="#{msg_name}">\n<summary><b>{msg_name}</b></summary>\n\n### __{msg_name}__\n: {msg_desc}\n{fields}</details>')
        msgs = '\n\n'.join(msgs)
        pkgs.append(f'## `{package_name}`\n\n{msgs}')
    
    pkgs = '\n\n'.join(pkgs)
    svcs = '\n\n'.join(svcs)
    clients_usage_i = []
    clients_usage = []
    for c in sylk_json.project.get('clients'):
        client_lang = c.get('language')
        client_lang = client_lang[0].upper()+client_lang[1:]
        clients_usage_i.append(f'- [{client_lang}](#{client_lang.lower()})')
        if client_lang=='Python':
            clients_usage.append(f'### Python\n\n```py\nfrom clients.python import {project_package_name}\n\nclient = {project_package_name}()\n\n# Unary call\nresponse = stub.<Unary>(<InMessage>())\nprint(response)\n\n# Server stream\nresponses = stub.<ServerStream>(<InMessage>())\nfor res in responses:\n\tprint(res)\n\n# Client Stream\nrequests = iter([<InMessage>(),<InMessage>()])\nresponse = client.<ClientStream>(requests)\nprint(response)\n\n# Bidi Stream\nresponses = client.<BidiStream>(requests)\nfor res in responses:\n\tprint(res)\n```\n')
        elif client_lang=='Typescript':
            clients_usage.append(f'### Typescript\n\n```ts\nimport {_OPEN_BRCK} {project_package_name} {_CLOSING_BRCK} from \'./clients/typescript/\';\n\nlet client = new {project_package_name}();\n\n// Unary call\nclient.<Unary>(<InMessage>)\n\t.then((res:<OutMessage>) => {_OPEN_BRCK}\n\t\tconsole.log(res);\n\t{_CLOSING_BRCK}).catch((err: any) => console.log(err));\n\n// Server Stream\nclient.<ServerStream>(<InMessage>)\n\t.subscribe((res: <OutMessage>) => {_OPEN_BRCK}\n\t\tconsole.log(res);\n\t{_CLOSING_BRCK})\n\n// Client Stream\n\n// Bidi Stream\nresponses = client.<BidiStream>()\n\t.subscribe((res: <OutMessage>) => {_OPEN_BRCK}\n\t\tconsole.log(res)\n\t{_CLOSING_BRCK})\n\nresponses.write(<InMessage>)\n```\n')
        elif client_lang=='Go':
            go_package_name = sylk_json.project.get('goPackage')
            clients_usage.append(f'### Go\n\n```go\npackage main\nimport (\n\t"fmt"\n\n\tclient "{go_package_name}/clients/go"\n)\n\nfunc main() {_OPEN_BRCK}\n\t//Init the client\n\tc := client.Default()\n\n\t// Construct a message\n\tmsg :=  <SomePackage>.<SomeMessage>{_OPEN_BRCK}{_CLOSING_BRCK}\n\n\t// Send unary\n\tres := c.<SomeRpc>(&msg)\n\tfm.tPrintf("Got server unary response: %v",res)\n\n\t// Client Stream\n\tListMessages := []*<Package>.<Message>{_OPEN_BRCK}\n\t\t{_OPEN_BRCK}{_CLOSING_BRCK},\n\t{_CLOSING_BRCK}\n\tclientStream := c.<ClientStreamingRPC>(ListMessages)\n\tfmt.Printf("Got response for client stream: %v", clientStream)\n\n\t// Server stream\n\tresponse_stream := c.<SomeServerStreamRPC>(&msg)\n\tfmt.Prontf("Got server stream response: %v", response_stream)\n\n{_CLOSING_BRCK}\n```\n')
    temp_index = []
    for k in index:
        for i in index[k]:
            temp_i = i
            link = i
            if len(i.split('.')) > 1:
                temp_i = i.split('.')[1]
            temp_index.append(f'- [{temp_i}](#{temp_i.lower()})')
    index = '\n'.join(temp_index)
    clients_usage = '\n'.join(clients_usage)
    clients_usage_i = '\n'.join(clients_usage_i)
    extra_links = sylk_json._config.get('docs')
    temp_links = ''
    if extra_links is not None:
        for k in extra_links:
            if file_system.check_if_file_exists(sylk_json.project.get('uri')+''+ extra_links[k]):
                temp_links += '{2}\n[{0}]({1})'.format(k,extra_links[k],temp_links)
            else :
                pretty.print_error("Extra docs file is not found ! [{0}]({1})".format(k,extra_links[k]))
    temp_links = '\n### Further Reading\n{0}'.format(temp_links) if extra_links is not None else ''

    readme_file = f'# {project_name}\n\nThis project has been generated thanks to [```sylk.build```](https://www.sylk.build) !\n\nThis project is using gRPC as main code generator and utilize HTTP2 + protobuf protocols for communication.\n\n# Index\nUsage:\n{clients_usage_i}\n\nResources:\n{index}\n\n# Services\n\n{svcs}\n\n# Packages\n\n{pkgs}\n\n\n# Usage\n\nThis project supports clients communication in the following languages:\n\n{clients_usage}\n{temp_links}\n* * *\n__This project and README file has been created thanks to [sylk.build](https://www.sylk.build)__'
    return readme_file
