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

from webezyio.architect import WebezyArchitect
from webezyio.commons.helpers import WZJson,MessageToDict
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success

def import_package(source,target,path,webezy_json:WZJson):
    importing_into_pkg = False
    old_pkg = None
    old_svc = None
    ARCHITECT = WebezyArchitect(
        path=path,domain=webezy_json.domain,project_name=webezy_json.project.get('name'))

    if len(target.split('.')) > 2:
        importing_into_pkg = True
        old_pkg = webezy_json.get_package(
            target.split('.')[1])
        dep = []
        if old_pkg is None:
            print_error(f"Package '{target}' not exists")
            exit(1)
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
        ARCHITECT.EditPackage(old_pkg.get('name'), dep,temp_msgs,description=old_pkg.get('description'),enums=old_pkg.get('enums'),extensions=old_pkg.get('extensions'))
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
                dep = old_svc.get('dependencies')
                dep.append(source)
            else:
                print_warning(
                    f"Package '{source}' already injected into '{target}' service")
                exit(1)
        else:
            dep.append(source)

        ARCHITECT.EditService(old_svc.get('name'), dep, old_svc.get('description'),old_svc.get('methods'),extensions=old_svc.get('extensions'))
        ARCHITECT.Save()

    importing_into_pkg = 'package' if importing_into_pkg == True else 'service'
    print_info(
        f"Attaching package '{source}' -> '{target}' {importing_into_pkg}")

def remove_import(source,target,path,webezy_json:WZJson):
    ARCHITECT = WebezyArchitect(
        path=path,domain=webezy_json.domain,project_name=webezy_json.project.get('name'))

    if len(target.split('.')) > 2:
        old_pkg = webezy_json.get_package(
            target.split('.')[1])
        dep = []
        if old_pkg is None:
            print_error(f"Package '{target}' not exists")
            exit(1)
        if old_pkg.get('dependencies') is not None:
            dep = old_pkg.get('dependencies')
            if source not in old_pkg.get('dependencies'):
                print_error(f"'{source}' not in '{target}'")
                exit(1)
                
            else:
                dep = old_pkg.get('dependencies')
                dep.remove(source)
        else:
            print_error(f"'{source}' cannot be found under '{target}'")
            exit(1)
            
        pkg = webezy_json.get_package(old_pkg.get('name'),False)
        temp_msgs = []
        for m in pkg.messages:
            temp_msgs.append(MessageToDict(m))
        ARCHITECT.EditPackage(old_pkg.get('name'), dep,temp_msgs,description=old_pkg.get('description'),enums=old_pkg.get('enums'),extensions=old_pkg.get('extensions'))
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
                print_warning(
                    f"Package '{source}' not injected into '{target}' service")
                exit(1)
            else:
                dep = old_svc.get('dependencies')
                dep.remove(source)
        
        ARCHITECT.EditService(old_svc.get('name'), dep, old_svc.get('description'),old_svc.get('methods'),description=old_svc.get('description'),extensions=old_svc.get('extensions'))
        ARCHITECT.Save()

    print_warning(
        f"Removed package '{source}' -> '{target}'")