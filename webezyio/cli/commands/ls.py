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

import logging
from prettytable import PrettyTable
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success
from webezyio.commons.helpers import WZJson

def list_by_name(full_name,webezy_json:WZJson):
    """Will print in pretty table the resource description and child descriptions from full name of the resource 
    e.g listing package description and messages + enums child descriptions the 'full_name' param will need to be <domain>.<package>.<version>
    """
    args_split = len(full_name.split('.'))
    if args_split == 1:
        print_info(full_name)
    # Services list
    elif args_split > 1 and args_split <=2:
        try:
            header = ['Service','RPC\'s','Dependencies']
            svc = webezy_json.get_service(full_name.split('.')[1])
            tab = PrettyTable(header)
            add_service_desc(tab,svc)
            # tab.add_row([svc['name'],len(svc.get('methods') if svc.get('methods') is not None else []),svc.get('dependencies')])
            print_info(tab,True,'Listing service resource')
        except Exception:
            print_warning(f'Resource {full_name} wasnt found services')
    # Packages list
    elif args_split == 3:
        try:
            pkg = webezy_json.get_package(full_name.split('.')[1])
            header = ['Package','Messages','Enums','Dependencies']
            tab = PrettyTable(header)
            tab.add_row([pkg['name'],len(pkg.get('messages') if pkg.get('messages') is not None else []),len(pkg.get('enums')) if pkg.get('enums') is not None else 0,pkg.get('dependencies')])
            print_info(tab,True,'Listing package resource')
        except Exception as e:
            logging.error(e)
            print_warning(f'Resource {full_name} wasnt found on packages')
    # Enums list
    elif args_split > 3 and args_split <= 4:
        try:
            header = ['Field','Field type','Enum Type', 'Message Type']
            tab = PrettyTable(header)
            msg = webezy_json.get_message(full_name)
            for f in msg.get('fields'):
                tab.add_row([f['name'],f.get('fieldType'),f.get('enumType'),f.get('messageType')])
            print_info(tab,True,'Listing message [{0}] fields'.format(msg.get('fullName')))
        except Exception:
            print_warning(f'Resource {full_name} wasnt found on messages')
    # Fields list ?
    else:
        try:
            msg = webezy_json.get_message('.'.join(full_name.split('.')[:-1]))
            field = next((f for f in msg['fields'] if f['name'] == full_name.split('.')[-1]),None)
            print_info(field,True)
        except Exception:
            print_warning(f'Field {full_name} wasnt found on message')

def list_by_resource(type,webezy_json:WZJson):
    """Will print in pretty table the resource description and child descriptions from a resource type
    e.g to list all services description and all methods (RPC's) under the services, the 'type' param will need to be passed with 'service' string
    """
    # Services list
    if type == 'service':
        header = ['Service','RPC\'s','Dependencies']
        tab = PrettyTable(header)
        header = ['RPC','Type','Input','Output']
        tab_rpcs = PrettyTable(header)
        if webezy_json.services is not None:
            for svc in webezy_json.services:
                service=webezy_json.services[svc]
                if service.get('methods') is not None:
                    for rpc in service.get('methods'):
                        add_rpc_desc(tab_rpcs,rpc)
                add_service_desc(tab,service)
            print_info(tab,True,'Listing services resources')
        else:
            print_warning("No services under {}".format(webezy_json.project.get('packageName')))
    
    # Packages list
    elif type == 'package':
        header = ['Package','Messages','Enums','Dependencies']
        tab = PrettyTable(header)
        if webezy_json.packages is not None:

            for pkg in webezy_json.packages:
                pkg = webezy_json.packages[pkg]
                tab.add_row([pkg['name'],len(pkg.get('messages') if pkg.get('messages') is not None else []),len(pkg.get('enums') if pkg.get('enums') is not None else []),pkg.get('dependencies') ])
            print_info(tab,True,'Listing packages resources')
        else:
            print_warning("No packages under {}".format(webezy_json.project.get('packageName')))

    # Messages List
    elif type == 'message':
        header = ['Message','Fields','Package']
        tab = PrettyTable(header)
        if webezy_json.packages is not None:
            for pkg in webezy_json.packages:
                package = webezy_json.packages[pkg]
                if package.get('messages'):
                    for m in package['messages']:
                        tab.add_row([m['name'],len(m.get('fields') if m.get('fields') is not None else []), package.get('package') ])
            print_info(tab,True,'Listing packages resources')
        else:
            print_warning("No packages under {}".format(webezy_json.project.get('packageName')))

    # RPC's List
    elif type == 'rpc':
        header = ['RPC','Type','Input','Output']
        tab_rpcs = PrettyTable(header)
        if webezy_json.services is not None:
            for svc in webezy_json.services:
                service = webezy_json.services[svc]
                for rpc in service.get('methods'):
                    add_rpc_desc(tab_rpcs,rpc)
            print_info(tab_rpcs,True,'Listing RPC\'s')
        else:
            print_warning("No services under {}".format(webezy_json.project.get('packageName')))
    
    # Not supported listing ALL resources
    else:
        if type is not None:
            print_warning("Listing '{0}' not supported yet".format(type))
        list_all(webezy_json)

def list_all(webezy_json:WZJson):
    """Will print all webezy.io project resource that are declared on webezy.json file"""

    # Services list
    header = ['Service','RPC\'s','Dependencies']
    tab = PrettyTable(header)
    
    if webezy_json.services:
        # RPC's list
        header = ['RPC','Type','Input','Output']
        tab_rpcs = PrettyTable(header)
        
        for svc in webezy_json.services:
            service=webezy_json.services[svc]
            add_service_desc(tab,service)
            if service.get('methods') is not None:
                for rpc in service.get('methods'):
                    add_rpc_desc(tab_rpcs,rpc)
    
        print_info(tab,True,'Listing services resources')
        print_info(tab_rpcs,True,'Listing RPC\'s')
    
    # Packages list
    header = ['Package','Messages','Enums','Dependencies']
    tab = PrettyTable(header)
    if webezy_json.packages is not None:
        for pkg in webezy_json.packages:
            pkg = webezy_json.packages[pkg]
            add_package_desc(tab,pkg)
    else:
        print_warning("No packages on project")

    print_info(tab,True,'Listing packages resources')

    # Messages List
    header = ['Message','Fields','Package']
    tab = PrettyTable(header)

    if webezy_json.packages is not None:
        for pkg in webezy_json.packages:
            package = webezy_json.packages[pkg]
            for m in package['messages']:
                add_message_desc(tab,m,package)
    else:
        print_warning("No packages on project")
    
    print_info(tab,True,'Listing packages messages')
    
    # Enums list
    header = ['Enum','Values','Package']
    tab = PrettyTable(header)
    if webezy_json.packages is not None:
        for pkg in webezy_json.packages:
            package = webezy_json.packages[pkg]
            if package.get('enums'):

                for e in package['enums']:
                    add_enum_desc(tab,e,package)
    else:
        print_warning("No packages on project")
    print_info(tab,True,'Listing packages enums')


def add_service_desc(tab,svc_description):
    tab.add_row([svc_description.get('name'),len(svc_description.get('methods') if svc_description.get('methods') is not None else []),svc_description.get('dependencies')])

def add_package_desc(tab,package_desc):
    tab.add_row([package_desc.get('name'),len(package_desc.get('messages') if package_desc.get('messages') is not None else []),len(package_desc.get('enums') if package_desc.get('enums') is not None else []),package_desc.get('dependencies') ])

def add_message_desc(tab,msg_desc,package_desc):
    tab.add_row([msg_desc.get('name'),len(msg_desc.get('fields') if msg_desc.get('fields') is not None else []),package_desc.get('package')])

def add_enum_desc(tab,enum_desc,package_desc):
    tab.add_row([enum_desc.get('name'),len(enum_desc.get('values') if enum_desc.get('values') is not None else []),package_desc.get('package')])

def add_rpc_desc(tab,rpc_desc):
    rpc_type_server = rpc_desc.get('serverStreaming')
    rpc_type_client = rpc_desc.get('clientStreaming')
    rpc_type = 'Unary' if (rpc_type_client == False or rpc_type_client is None ) and (rpc_type_server == False or rpc_type_server is None) else 'Client stream' if rpc_type_client == True and (rpc_type_server == False or rpc_type_server is None) else 'Server Stream' if rpc_type_server == True and (rpc_type_client == False or rpc_type_client is None ) else 'Bidi' if rpc_type_client == True and rpc_type_server == True else ''
    tab.add_row([rpc_desc.get('name'),rpc_type,rpc_desc.get('inputType'),rpc_desc.get('outputType')])

