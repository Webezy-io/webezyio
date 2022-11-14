# Copyright (c) 2022 Webezy.io.

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

import inquirer
from webezyio.builder.src.main import WebezyBuilder
from webezyio.cli.theme import WebezyTheme
from webezyio.commons import client_wrapper 
from webezyio import _helpers,_fs,_pretty
import sys,importlib
from google.protobuf.timestamp_pb2 import Timestamp
import time

_supported_types = ['TYPE_STRING','TYPE_MESSAGE','TYPE_BOOL','TYPE_INT32','TYPE_INT64','TYPE_FLOAT','TYPE_DOUBLE']

def CallRPC(service_module_path:str,service_rpc_name:str,wz_json:_helpers.WZJson,host:str='localhost',port:int=50051,debug:bool=False,timeout=10):

    # Check if root directory is in current path
    if _fs.get_current_location() not in sys.path:
        sys.path.append(_fs.get_current_location())

    # Getting pythonic path for service module
    path = service_module_path.replace('.py','').replace('/','.')
    # Extracting the service name
    service_name = path.split('.')[-1].replace('_pb2_grpc','')
    stub_name = service_name+'Stub'
    rpc = service_rpc_name
    # Constructing RPC full name
    rpc_full_name = '{0}.{1}.v1.{2}'.format(wz_json.domain,service_name,rpc)
    # Check if RPC does exist under specified module
    if wz_json.get_rpc(rpc_full_name) is None:
        _pretty.print_error("Error RPC : \"{0}\", is not found under service -> [{1}]".format(rpc,service_name))
        exit(1)

    _pretty.print_info(f'calling {path = } [{stub_name}]\n\t-> {rpc  = } [{rpc_full_name}]\n\t-> {host = }\n\t-> {port = }')
    
    # Dynamic import module (Only supporting clients proto modules)
    service_module = importlib.import_module(path)
    # Init the service stub
    stub = client_wrapper.WebezyioClient(service_module,stub_name,host,port,timeout)
    # Get RPC description from webezy.json file
    rpc_description = wz_json.get_rpc(rpc_full_name)

    input_package_name = rpc_description['inputType'].split('.')[1]
    input_message_name = rpc_description['inputType'].split('.')[-1]
    
    input_message_description = wz_json.get_message(rpc_description['inputType'])
    output_message_description = wz_json.get_message(rpc_description['outputType'])

    # Get modules objects
    package_proto = getattr(service_module,input_package_name+'__pb2')
    message_proto = getattr(package_proto,input_message_name)

    # TODO allow support iterator for client stream
    msg = message_proto()
    # Ask for seed data
    seed_data = inquirer.prompt([
        inquirer.Confirm('seed',message='Do you want to send seed data?',default=True)
    ],theme=WebezyTheme())
    # Seed data input
    if seed_data is not None:
        
        # Auto seed data
        if seed_data.get('seed') == True:
            for f in input_message_description['fields']:

                if f['fieldType'] in _supported_types and f['label'] == 'LABEL_OPTIONAL':
                    if f['fieldType'] == 'TYPE_STRING':
                        setattr(msg,f['name'],'Test')
                    elif f['fieldType'] == 'TYPE_BOOL':
                        setattr(msg,f['name'],True)
                    elif f['fieldType'] == 'TYPE_INT32' or f['fieldType'] == 'TYPE_INT64':
                        setattr(msg,f['name'],10)
                    elif f['fieldType'] == 'TYPE_DOUBLE' or f['fieldType'] == 'TYPE_FLOAT':
                        setattr(msg,f['name'],10.1)
                    elif f['fieldType'] == 'TYPE_MESSAGE':
                        if f['messageType'] == 'google.protobuf.Timestamp':
                            ts = getattr(msg,f['name'])
                            getattr(ts,'GetCurrentTime')()
                        elif f['messageType'] == 'google.protobuf.Struct':
                            struct = getattr(msg,f['name'])
                            getattr(struct,'update')({'test':'struct'})
                        elif wz_json.get_message(f['messageType']) is not None:
                            _pretty.print_info(f['messageType'])

        # User input message
        else:
            fields = {}
            for f in input_message_description['fields']:
                
                if f['fieldType'] in _supported_types:
                    question = []
                    if f['fieldType'] == 'TYPE_STRING':
                        fields[f.get('name')] = None
                        question.append(inquirer.Text(f.get('name'),'Enter a value for "{0}" key (String)'.format(f.get('name')),"Test"))
                    elif f['fieldType'] =='TYPE_BOOL':
                        fields[f.get('name')] = None
                        question.append(inquirer.Confirm(f.get('name'),'Choose value for "{0}" key (Boolean)'.format(f.get('name')),"Test"))
                    elif f['fieldType'] == 'TYPE_INT32' or f['fieldType'] =='TYPE_INT64':
                        fields[f.get('name')] = None
                        question.append(inquirer.Text(f.get('name'),'Choose value for "{0}" key (Integer)'.format(f.get('name')),"Test"))
                    elif f['fieldType'] == 'TYPE_DOUBLE' or f['fieldType'] =='TYPE_FLOAT':
                        fields[f.get('name')] = None
                        question.append(inquirer.Text(f.get('name'),'Choose value for "{0}" key (Integer)'.format(f.get('name')),"Test"))
                    if len(question) == 0:
                        pass
                    else:
                        fields[f.get('name')] = inquirer.prompt(question,theme=WebezyTheme()).get(f.get('name'))
                else:
                    _pretty.print_warning('Skipping {0}->{1}:{2}'.format(f['name'],f['fieldType'],f['messageType']))
                    
            for k in fields:
                setattr(msg,k,fields[k])

    _pretty.print_info(msg,True,'Request Object [{0}]'.format(input_message_description['fullName']))
    # TODO allow support for UNARY / STREAM
    # get the start time
    if debug:
        st = time.time()    
    try:
        response = getattr(stub, rpc)(msg)
        _pretty.print_info('Waiting for server response... [{0}]'.format(output_message_description['fullName']))
        if debug:
            # get the end time
            et = time.time()
            # get the execution time
            elapsed_time = et - st
            if elapsed_time < 1:
                elapsed_time = elapsed_time * 1000
                _pretty.print_note('Execution time: {:.2f} ms.'.format(elapsed_time))
            else:
                _pretty.print_note('Execution time: {:.2f} sec.'.format(elapsed_time))
            _pretty.print_note('Response size: {}'.format(sys.getsizeof(response)))
        try:
            for i in response:
                _pretty.print_info(i,True)
        except:
            _pretty.print_info(f'{response = }')

    except Exception as e:
        if debug:
            # get the end time
            et = time.time()
            # get the execution time
            elapsed_time = et - st
            if elapsed_time < 1:
                elapsed_time = elapsed_time * 1000
                _pretty.print_note('Execution time: {:.2f} ms.'.format(elapsed_time))
            else:
                _pretty.print_note('Execution time: {:.2f} sec.'.format(elapsed_time))  
            
        _pretty.print_error(e,True)