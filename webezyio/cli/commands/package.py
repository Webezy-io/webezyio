from webezyio.architect import WebezyArchitect
from webezyio.commons.helpers import WZJson,MessageToDict
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success

def import_package(source,target,path,webezy_json:WZJson):
    importing_into_pkg = False
    old_pkg = None
    old_svc = None
    ARCHITECT = WebezyArchitect(
        path=path)

    if len(target.split('.')) > 2:
        importing_into_pkg = True
        old_pkg = webezy_json.get_package(
            target.split('.')[1])
        dep = []
        if old_pkg.get('dependencies') is not None:
            dep = old_pkg.get('dependencies')
            if source not in old_pkg.get('dependencies'):
                dep = old_pkg.get('dependencies')
                dep.append(source)
            else:
                print_warning(
                    f"Package '{source}' already injected into '{target}' package")
                exit(1)
        else:
            dep.append(source)
        pkg = webezy_json.get_package(old_pkg.get('name'),False)
        temp_msgs = []
        for m in pkg.messages:
            temp_msgs.append(MessageToDict(m))
        ARCHITECT.AddPackage(old_pkg.get('name'), dep,temp_msgs)
        ARCHITECT.Save()

    else:
        dep = []
        old_svc = webezy_json.get_service(target)
        if old_svc is None:
            print_error(f"Service '{target}' not exists")
            exit(1)
        if old_svc.get('dependencies') is not None:
            dep = old_svc.get('dependencies')
            if source not in old_svc.get('dependencies'):
                dep = old_pkg.get('dependencies')
                dep.append(source)
            else:
                print_warning(
                    f"Package '{source}' already injected into '{target}' service")
                exit(1)
        else:
            dep.append(source)

        ARCHITECT.AddService(old_svc.get('name'), dep, None)
        ARCHITECT.Save()

    importing_into_pkg = 'package' if importing_into_pkg == True else 'service'
    print_info(
        f"Attaching package '{source}' -> '{target}' {importing_into_pkg}")