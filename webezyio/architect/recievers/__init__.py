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
from webezyio.commons import resources
from webezyio.commons.pretty import print_error, print_info

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

    def edit_resource(self,webezyJson,resource,args):

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
                            if args[0] is not None:
                                if m.get('name') == args[0].get('old_name'):
                                    webezyJson['packages'][pkgname]['messages'][index] = resource
                                    break
                            if m.get('fullName') == resource.get('fullName'):
                                webezyJson['packages'][pkgname]['messages'][index] = resource
                                # removed_message = webezyJson['packages'][pkgname]['messages'][index]
                                # webezyJson['packages'][pkgname]['messages'].remove(removed_message)
                                # webezyJson['packages'][pkgname]['messages'].insert(len(webezyJson['packages'][pkgname]['messages']), removed_message)
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
        """Removing webezy.io resource by full name identifier"""

        removed = False
        full_name = full_name[0]

        if len(full_name.split('.')) == 4:

            if webezyJson.get('packages') is not None:
                pkg_name = 'protos/{0}/{1}.proto'.format(full_name.split('.')[2],full_name.split('.')[1])
                if pkg_name in webezyJson.get('packages'):

                    # Handling deletion of message
                    for m in webezyJson['packages'][pkg_name]['messages']:
                        if m.get('fullName') == full_name:
                            webezyJson['packages'][pkg_name]['messages'].remove(m)
                            removed = True

                    # Handling deletion of enum
                    if removed == False and webezyJson['packages'][pkg_name].get('enums') is not None:
                        for e in webezyJson['packages'][pkg_name]['enums']:
                            if e.get('fullName') == full_name:
                                webezyJson['packages'][pkg_name]['enums'].remove(e)
                                removed = True
                else:
                    print_error("Coludnt find {} under packages".format(full_name))

            # Handling deletion of RPC
            if removed == False and webezyJson.get('services') is not None:
                if full_name.split('.')[1] in webezyJson.get('services'):
                    svc = webezyJson['services'][full_name.split('.')[1]]
                    for r in svc.get('methods'):
                        if r.get('name') == full_name.split('.')[-1]:
                            svc['methods'].remove(r)
                            removed = True
        elif len(full_name.split('.')) == 6:
            # Handling removal of oneof fields
            if webezyJson.get('packages') is not None:
                pkg_name = 'protos/{0}/{1}.proto'.format(full_name.split('.')[2],full_name.split('.')[1])
                if pkg_name in webezyJson.get('packages'):
                    if webezyJson['packages'][pkg_name].get('messages') is not None:
                        index_msgs = 0
                        for m in webezyJson['packages'][pkg_name].get('messages'):
                            field_name = '.'.join(full_name.split('.')[:-1])
                            field = next((f for f in m.get('fields') if f.get('fullName') == field_name),None)
                            if field is not None:
                                field_index = m.get('fields').index(field)
                                oneof_field = next((one_f for one_f in field.get('oneofFields') if one_f.get('fullName') == full_name),None)
                                if oneof_field is not None:
                                    print_info(f'{pkg_name=} | {index_msgs=} | {field_index=}')
                                    webezyJson['packages'][pkg_name]['messages'][index_msgs]['fields'][field_index]['oneofFields'].remove(oneof_field)
                                    removed = True
                                    break
                            index_msgs += 1

        else:
            # Removing fields or enum values
            if webezyJson.get('packages') is not None:
                pkg_name = 'protos/{0}/{1}.proto'.format(full_name.split('.')[2],full_name.split('.')[1])
                
                if pkg_name in webezyJson.get('packages'):

                    # Handling deletion of message field
                    if webezyJson['packages'][pkg_name].get('messages') is not None:
                        index_msgs = 0
                        for m in webezyJson['packages'][pkg_name].get('messages'):
                            field = next((f for f in m.get('fields') if f.get('fullName') == full_name),None)
                            if field is not None:
                                webezyJson['packages'][pkg_name]['messages'][index_msgs]['fields'].remove(field)
                                removed = True
                                break
                            index_msgs += 1

                    # Handling deletion of enum value
                    if webezyJson['packages'][pkg_name].get('enums') is not None:
                        if removed == False:
                            index_enums = 0
                            for e in webezyJson['packages'][pkg_name].get('enums'):
                                ev = next((ev for ev in e.get('values') if ev.get('fullName') == full_name),None)
                                if ev is not None:
                                    webezyJson['packages'][pkg_name]['enums'][index_enums]['values'].remove(ev)

                            index_enums +=1

        if removed == False:
            print_error("Some error occured during deletion process !")
            exit(1)
        log.debug("Removing resource "+full_name)

    def create_new_project(self,*args,**kwargs):
        logging.debug("Create new project {0}".format(args))

    def set_domain(self,*args,**kwargs):
        # logging.debug(args[0])
        args[0]['domain'] = args[1][0][0]
        logging.debug("Setting project domain {0}".format(args[1][0][0]))