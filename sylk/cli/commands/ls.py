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

import logging
from prettytable import PrettyTable
from sylk.commons.pretty import print_info,print_warning,print_error,print_note,print_success
from sylk.commons.helpers import Graph, SylkJson
# from sylk.commons.protos import SylkCommons_pb2


def list_dependencies(resource,sylk_json:SylkJson):
    resources = []

    if resource is None or resource in ['service','package']:
        for p in sylk_json.packages:
            pkg = sylk_json.packages[p]
            resources.append(pkg)
        for s in sylk_json.services:
            svc = sylk_json.services[s]
            resources.append(svc)

        resourcesSorted = Graph(resources,True).topologicalSort()
    elif resource == 'message':
        for p in sylk_json.packages:
            pkg = sylk_json.packages[p]
            for m in pkg.get('messages'):
                resources.append(m)
        resourcesSorted = dict(Graph(resources).graph)
        del resourcesSorted[None]

    print_info('Listing Dependencies {}'.format(resource if resource is not None else 'All'),True)
    
    for dep in resourcesSorted:

        if len(dep.split('.')) == 1:
            if resource is None or resource == 'service':
                print()
                print_success('|| Service: {}'.format(dep))

                if sylk_json.services[dep].get('dependencies'):
                    for d in sylk_json.services[dep].get('dependencies'):
                        print('    ||\t     |\n    ||\t      -- {}'.format(d))
        elif resource is None or resource == 'package':
            print()
            print_note('| Package: {}'.format(dep))
            pkg_name = 'protos/{}/{}.proto'.format(dep.split('.')[-1],dep.split('.')[1])
            if sylk_json.packages[pkg_name].get('dependencies'):
                for d in sylk_json.packages[pkg_name].get('dependencies'):
                    print('    ||\t     |\n    ||\t      -- {}'.format(d))
        
        elif resource == 'message':
            msg = resourcesSorted[dep]
            print()
            print_note('|| Message: {}'.format(dep))
            for m in msg:
                if m is not None:
                    print('    ||\t     |\n    |\t      - * {}'.format(m))

            print()


def list_by_name(full_name,sylk_json:SylkJson):
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
            svc = sylk_json.get_service(full_name.split('.')[1],wz_json=sylk_json._sylk_json)
            tab = PrettyTable(header)
            add_service_desc(tab,svc)
            # tab.add_row([svc['name'],len(svc.get('methods') if svc.get('methods') is not None else []),svc.get('dependencies')])
            print_info(tab,True,'Listing service resource')
        except Exception:
            print_warning(f'Resource {full_name} wasnt found services')
    # Packages list
    elif args_split == 3:
        try:
            pkg = sylk_json.get_package(full_name.split('.')[1])
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
            enum = sylk_json.get_enum(full_name)
            if enum is not None:
                header = ['Name', 'Value']
                tab = PrettyTable(header)
                for v in enum.get('values'):
                    tab.add_row([v['name'],v.get('number')])
                print_info(tab,True,'Listing enum [{0}] values'.format(enum.get('fullName')))
            else:
                msg = sylk_json.get_message(full_name)
                header = ['Field', 'Field type', 'Enum type', 'Message type']
                oneof_exist = next((f for f in msg.get('fields') if f.get('fieldType') == 'TYPE_ONEOF'),False)
                map_exist = next((f for f in msg.get('fields') if f.get('fieldType') == 'TYPE_MAP'),False)
                
                if oneof_exist:
                    header.append('Oneof')
                if map_exist:
                    header.append('Key type')
                    header.append('Value type')
                tab = PrettyTable(header)

                for f in msg.get('fields'):
                    
                    temp_row = [f['name'],f.get('fieldType','-'),f.get('enumType','-'),f.get('messageType','-')]

                    if oneof_exist:
                        temp_row.append(list(map(lambda x: x.get('name'),f.get('oneofFields'))))
                    if map_exist:
                        temp_row.append(f.get('keyType','-'))
                        temp_row.append(f.get('valueType','-'))

                    tab.add_row(temp_row)
                print_info(tab,True,'Listing message [{0}] fields'.format(msg.get('fullName')))
        except Exception as e:
            print_error(e)
            print_warning(f'Resource {full_name} wasnt found on enums or messages')
    # Fields list ?
    else:
        try:
            msg = sylk_json.get_message('.'.join(full_name.split('.')[:-1]))
            field = next((f for f in msg['fields'] if f['name'] == full_name.split('.')[-1]),None)
            print_info(field,True)
        except Exception:
            print_warning(f'Field {full_name} wasnt found on message')

def list_by_resource(type,sylk_json:SylkJson):
    """Will print in pretty table the resource description and child descriptions from a resource type
    e.g to list all services description and all methods (RPC's) under the services, the 'type' param will need to be passed with 'service' string
    """
    # Services list
    if type == 'service':
        header = ['Service','RPC\'s','Dependencies','Extensions']
        tab = PrettyTable(header)
        header = ['RPC','Type','Input','Output']
        tab_rpcs = PrettyTable(header)
        if sylk_json.services is not None:
            for svc in sylk_json.services:
                service=sylk_json.services[svc]
                ext = []
                if service.get('extensions') is not None:
                    ext = list(map(lambda k: k,service.get('extensions')))
                ext = ext if len(ext) >0 else '-'
                if service.get('methods') is not None:
                    for rpc in service.get('methods'):
                        add_rpc_desc(tab_rpcs,rpc)
                add_service_desc(tab,service,ext)
            print_info(tab,True,'Listing services resources')
        else:
            print_warning("No services under {}".format(sylk_json.project.get('packageName')))
    
    # Packages list
    elif type == 'package':
        header = ['Package','Messages','Enums','Dependencies','Extensions']
        tab = PrettyTable(header)
        if sylk_json.packages is not None:

            for pkg in sylk_json.packages:
                pkg = sylk_json.packages[pkg]
                ext = []
                if pkg.get('extensions') is not None:
                    ext = list(map(lambda k: k,pkg.get('extensions')))
                ext = ext if len(ext) >0 else '-'
                tab.add_row([pkg['name'],len(pkg.get('messages') if pkg.get('messages') is not None else []),len(pkg.get('enums') if pkg.get('enums') is not None else []),pkg.get('dependencies'),ext ])
            print_info(tab,True,'Listing packages resources')
        else:
            print_warning("No packages under {}".format(sylk_json.project.get('packageName')))

    # Messages List
    elif type == 'message':
        header = ['Message','Fields','Package','Extensions','Extending']
        tab = PrettyTable(header)
        if sylk_json.packages is not None:
            for pkg in sylk_json.packages:
                package = sylk_json.packages[pkg]
                if package.get('messages'):
                    for m in package['messages']:
                        ext = []
                        if m.get('extensions') is not None:
                            ext = list(map(lambda k: k,m.get('extensions')))
                        ext_type = m.get('extensionType') if m.get('extensionType') is not None else '-'
                        ext = ext if len(ext) >0 else '-'
                        tab.add_row([m['name'],len(m.get('fields') if m.get('fields') is not None else []), package.get('package'), ext,ext_type ])
            print_info(tab,True,'Listing packages resources')
        else:
            print_warning("No packages under {}".format(sylk_json.project.get('packageName')))

    # RPC's List
    elif type == 'rpc':
        header = ['RPC','Type','Input','Output']
        tab_rpcs = PrettyTable(header)
        if sylk_json.services is not None:
            for svc in sylk_json.services:
                service = sylk_json.services[svc]
                for rpc in service.get('methods'):
                    add_rpc_desc(tab_rpcs,rpc)
            print_info(tab_rpcs,True,'Listing RPC\'s')
        else:
            print_warning("No services under {}".format(sylk_json.project.get('packageName')))
    
    # Extensions List
    elif type == 'extension':
        header = ['Name','Package','Extending']
        tab_exts = PrettyTable(header)
        
        options = sylk_json.get_extensions()
        # Extensions fields options
        if len(options) > 0:
            for opt in options:
                add_ext_desc(tab_exts,opt)
            print_info(tab_exts,True,'Listing Extensions')
        else:
            print_warning("No services under {}".format(sylk_json.project.get('packageName')))
    

    # Not supported listing ALL resources
    else:
        if type is not None:
            print_warning("Listing '{0}' not supported yet".format(type))
        list_all(sylk_json)

def list_all(sylk_json:SylkJson):
    """Will print all sylk.build project resource that are declared on sylk.json file"""

    # Services list
    header = ['Service','RPC\'s','Dependencies','Extensions']
    tab = PrettyTable(header)
    
    if sylk_json.services:
        # RPC's list
        header = ['RPC','Type','Input','Output']
        tab_rpcs = PrettyTable(header)
        
        for svc in sylk_json.services:
            service=sylk_json.services[svc]
            ext = []
            if service.get('extensions') is not None:
                ext = list(map(lambda k: k,service.get('extensions')))
            ext = ext if len(ext) >0 else '-'
            add_service_desc(tab,service,ext)
            if service.get('methods') is not None:
                for rpc in service.get('methods'):
                    add_rpc_desc(tab_rpcs,rpc,)
    
        print_info(tab,True,'Listing services resources')
        print_info(tab_rpcs,True,'Listing RPC\'s')
    
    # Packages list
    header = ['Package','Messages','Enums','Dependencies','Extensions']
    tab = PrettyTable(header)
    if sylk_json.packages is not None:
        for pkg in sylk_json.packages:
            pkg = sylk_json.packages[pkg]
            ext = []
            if pkg.get('extensions') is not None:
                ext = list(map(lambda k: k,pkg.get('extensions')))
            ext = ext if len(ext) >0 else '-'
            add_package_desc(tab,pkg,ext)
    else:
        print_warning("No packages on project")

    print_info(tab,True,'Listing packages resources')

    # Messages List
    header = ['Message','Fields','Package','Extensions','Extending']
    tab = PrettyTable(header)

    if sylk_json.packages is not None:
        for pkg in sylk_json.packages:
            package = sylk_json.packages[pkg]
            if package.get('messages'):
                for m in package['messages']:
                    ext = []
                    if m.get('extensions') is not None:
                        ext = list(map(lambda k: k,m.get('extensions')))
                    ext_type = m.get('extensionType') if m.get('extensionType') is not None else '-'
                    ext = ext if len(ext) >0 else '-'
                    add_message_desc(tab,m,package,ext,ext_type)
    else:
        print_warning("No packages on project")
    
    print_info(tab,True,'Listing packages messages')
    
    # Enums list
    header = ['Enum','Values','Package']
    tab = PrettyTable(header)
    if sylk_json.packages is not None:
        for pkg in sylk_json.packages:
            package = sylk_json.packages[pkg]
            if package.get('enums'):

                for e in package['enums']:
                    add_enum_desc(tab,e,package)
    else:
        print_warning("No packages on project")
    print_info(tab,True,'Listing packages enums')


def add_service_desc(tab,svc_description,extensions=None):
    tab.add_row([svc_description.get('name'),len(svc_description.get('methods') if svc_description.get('methods') is not None else []),svc_description.get('dependencies'),extensions])

def add_package_desc(tab,package_desc,ext):
    tab.add_row([package_desc.get('name'),len(package_desc.get('messages') if package_desc.get('messages') is not None else []),len(package_desc.get('enums') if package_desc.get('enums') is not None else []),package_desc.get('dependencies'),ext ])

def add_message_desc(tab,msg_desc,package_desc, ext,ext_type ):
    tab.add_row([msg_desc.get('name'),len(msg_desc.get('fields') if msg_desc.get('fields') is not None else []),package_desc.get('package'), ext,ext_type ])

def add_enum_desc(tab,enum_desc,package_desc):
    tab.add_row([enum_desc.get('name'),len(enum_desc.get('values') if enum_desc.get('values') is not None else []),package_desc.get('package')])

def add_rpc_desc(tab,rpc_desc):
    rpc_type_server = rpc_desc.get('serverStreaming')
    rpc_type_client = rpc_desc.get('clientStreaming')
    rpc_type = 'Unary' if (rpc_type_client == False or rpc_type_client is None ) and (rpc_type_server == False or rpc_type_server is None) else 'Client stream' if rpc_type_client == True and (rpc_type_server == False or rpc_type_server is None) else 'Server Stream' if rpc_type_server == True and (rpc_type_client == False or rpc_type_client is None ) else 'Bidi' if rpc_type_client == True and rpc_type_server == True else ''
    tab.add_row([rpc_desc.get('name'),rpc_type,rpc_desc.get('inputType'),rpc_desc.get('outputType')])

def add_ext_desc(tab,ext_desc):
    ext_package = '.'.join(ext_desc.get('fullName').split('.')[:-1])
    tab.add_row([ext_desc.get('name'),ext_package,ext_desc.get('extensionType')])
