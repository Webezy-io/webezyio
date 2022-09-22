import logging
from prettytable import PrettyTable
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success
from webezyio.commons.helpers import WZJson

def list_by_name(full_name,webezy_json:WZJson):
    args_split = len(full_name.split('.'))
    if args_split == 1:
        print('*',full_name)
    elif args_split > 1 and args_split <=2:
        try:
            header = ['Service','RPC\'s','Dependencies']
            svc = webezy_json.get_service(full_name.split('.')[1])
            tab = PrettyTable(header)
            tab.add_row([svc['name'],len(svc.get('methods') if svc.get('methods') is not None else []),svc.get('dependencies')])
            print_info(tab,True,'Listing service resource')
        except Exception:
            print_warning(f'Resource {full_name} wasnt found services')
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
    elif args_split > 3 and args_split <= 4:
        try:
            header = ['Message','Fields']
            tab = PrettyTable(header)
            msg = webezy_json.get_message(full_name)
            tab.add_row([msg['name'],len(msg.get('fields') if msg.get('fields') is not None else [])])
            print_info(tab,True,'Listing message resource')
        except Exception:
            print_warning(f'Resource {full_name} wasnt found on messages')
    else:
        try:
            msg = webezy_json.get_message('.'.join(full_name.split('.')[:-1]))
            field = next((f for f in msg['fields'] if f['name'] == full_name.split('.')[-1]),None)
            print_info(field,True)
        except Exception:
            print_warning(f'Field {full_name} wasnt found on message')

def list_by_resource(type,webezy_json:WZJson):
    if type == 'service':
        header = ['Service','RPC\'s','Dependencies']
        tab = PrettyTable(header)
        for svc in webezy_json.services:
            service=webezy_json.services[svc]
            tab.add_row([svc,len(service.get('methods') if service.get('methods') is not None else []),service.get('dependencies')])
        print_info(tab,True,'Listing services resources')
    elif type == 'package':
        header = ['Package','Messages','Enums','Dependencies']
        tab = PrettyTable(header)
        for pkg in webezy_json.packages:
            pkg = webezy_json.packages[pkg]
            tab.add_row([pkg['name'],len(pkg.get('messages') if pkg.get('messages') is not None else []),len(pkg.get('enums') if pkg.get('enums') is not None else []),pkg.get('dependencies') ])
        print_info(tab,True,'Listing packages resources')
    elif type == 'message':
        header = ['Message','Fields']
        tab = PrettyTable(header)
        for pkg in webezy_json.packages:
            package = webezy_json.packages[pkg]
            for m in package['messages']:
                tab.add_row([m['name'],len(m.get('fields') if m.get('fields') is not None else []) ])
        print_info(tab,True,'Listing packages resources')
    else:
        list_all(webezy_json)

def list_all(webezy_json:WZJson):
    header = ['Service','RPC\'s','Dependencies']
    tab = PrettyTable(header)
    if webezy_json.services:
        for svc in webezy_json.services:
            service=webezy_json.services[svc]
            tab.add_row([svc,len(service.get('methods') if service.get('methods') is not None else []),service.get('dependencies')])
        print_info(tab,True,'Listing services resources')

    header = ['Package','Messages','Enums','Dependencies']
    tab = PrettyTable(header)
    for pkg in webezy_json.packages:
        pkg = webezy_json.packages[pkg]
        tab.add_row([pkg['name'],len(pkg.get('messages') if pkg.get('messages') is not None else []),len(pkg.get('enums') if pkg.get('enums') is not None else []),pkg.get('dependencies') ])
    print_info(tab,True,'Listing packages resources')

    header = ['Message','Fields']
    tab = PrettyTable(header)
    for pkg in webezy_json.packages:
        package = webezy_json.packages[pkg]
        for m in package['messages']:
            tab.add_row([m['name'],len(m.get('fields') if m.get('fields') is not None else []) ])
    print_info(tab,True,'Listing packages resources')
