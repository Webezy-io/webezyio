import logging
from webezyio.commons import resources
from webezyio.commons.pretty import print_error

from webezyio.commons.resources import get_blank_webezy_json
from webezyio.commons.file_system import mkdir, rFile, wFile, get_current_location, join_path, check_if_file_exists
log = logging.getLogger('webezyio.cli.main')

class Core:

    def get_webezy_json(self,*args,**kwargs):
        logging.debug(args)
        if args[0][0] is None:
            current_path = get_current_location()
            destination_path = join_path(current_path,'webezy.json')
            logging.debug("Writing new webezy json {1}".format(args[0][0],destination_path))
            wzJson = get_blank_webezy_json(True)
            wFile(destination_path,wzJson,json=True)
            # destination_path = destination_path.replace('webezy.json','.webezy')
            # mkdir(destination_path)
        else:
            logging.debug("Getting webezy json {0}".format(args[0][0]))
            try:
                wzJson = rFile(args[0][0],json=True)
            except Exception:
                wzJson = get_blank_webezy_json(True)
                wFile(args[0][0],wzJson,json=True)

        return wzJson

    def save_webezy_json(self,*args,**kwargs):
        logging.debug("Saving webezy json {0} {1}".format(args,kwargs))
        wFile(args[0][0],args[0][1][0],json=True,overwrite=True)


class Builder:

    def log(self,hook,command_name,*args,**kwargs):
        logging.debug(f"[EXCUTE-HOOK-{hook.upper()}] {command_name} : {args}")
   
    def add_resource(self,webezyJson,*args,**kwargs):
        request = args[0][0][0]
        for k in request:
            logging.debug(f"Adding resource : {k}")
            if webezyJson.get(k) is None:
                webezyJson[k] = request[k]
            else:
                if k == 'domain':
                    webezyJson[k] = request[k]
                else:
                    for j in request[k]:
                        webezyJson[k][j] = request[k][j]

    def edit_resource(self,webezyJson,resource,*args):
        resource = resource[0]
        type = resource.get('type')
        kind = resource.get('kind')
        if type is not None:
            if type == 'descriptors':
                if kind == resources.ResourceKinds.message.value:
                    fullname = resource.get('fullName')
                    pkgname = 'protos/{0}/{1}.proto'.format(fullname.split('.')[2],fullname.split('.')[1])
                    package = webezyJson.get('packages').get(pkgname)
                    if package is not None:
                        index = 0
                        for m in package['messages']:
                            if m.get('fullName') == resource.get('fullName'):
                                webezyJson['packages'][pkgname]['messages'][index] = resource
                                break
                            index += 1
                elif kind == resources.ResourceKinds.method.value:
                    pass
                elif kind == resources.ResourceKinds.enum.value:
                    fullname = resource.get('fullName')
                    pkgname = 'protos/{0}/{1}.proto'.format(fullname.split('.')[2],fullname.split('.')[1])
                    package = webezyJson.get('packages').get(pkgname)
                    if package is not None:
                        index = 0
                        for e in package['enums']:
                            if e.get('fullName') == resource.get('fullName'):
                                webezyJson['packages'][pkgname]['enums'][index] = resource
                                break
                            index += 1
                elif kind == resources.ResourceKinds.enum_value.value:
                    pass
                elif kind == resources.ResourceKinds.field.value:
                    pass
            elif type == 'packages':
                fullname = resource.get('package')
                pkgname = 'protos/{0}/{1}.proto'.format(fullname.split('.')[2],fullname.split('.')[1])
                package = webezyJson.get('packages').get(pkgname)
                if package is not None:
                    webezyJson['packages'][pkgname] = resource
            elif type == 'services':
                webezyJson['services'][resource.get('name')] = resource

    def remove_resource(self,webezyJson,full_name,*args,**kwargs):
        removed = False
        full_name = full_name[0]
        if len(full_name.split('.')) == 4:
            if webezyJson.get('packages') is not None:
                pkg_name = 'protos/{0}/{1}.proto'.format(full_name.split('.')[2],full_name.split('.')[1])
                if pkg_name in webezyJson.get('packages'):
                    for m in webezyJson['packages'][pkg_name]['messages']:
                        if m.get('fullName') == full_name:
                            webezyJson['packages'][pkg_name]['messages'].remove(m)
                            removed = True

                    if removed == False and webezyJson['packages'][pkg_name].get('enums') is not None:
                        for e in webezyJson['packages'][pkg_name]['enums']:
                            if e.get('fullName') == full_name:
                                webezyJson['packages'][pkg_name]['enums'].remove(e)
                                removed = True

            if removed == False and webezyJson.get('services') is not None:
                if full_name.split('.')[1] in webezyJson.get('services'):
                    svc = webezyJson['services'][full_name.split('.')[1]]
                    for r in svc.get('methods'):
                        if r.get('name') == full_name.split('.')[-1]:
                            svc['methods'].remove(r)
                            removed = True
                
        
        log.debug("Removing resource "+full_name)

    def create_new_project(self,*args,**kwargs):
        logging.debug("Create new project {0}".format(args))

    def set_domain(self,*args,**kwargs):
        # logging.debug(args[0])
        args[0]['domain'] = args[1][0][0]
        logging.debug("Setting project domain {0}".format(args[1][0][0]))