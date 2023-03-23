# Copyright (c) 2022 sylk.build.

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
from sylk.commons import resources
from sylk.commons.helpers import Graph
from sylk.commons.pretty import print_error, print_info, print_warning

from sylk.commons.resources import get_blank_sylk_json
from sylk.commons.file_system import mkdir, rFile, wFile, get_current_location, join_path, check_if_file_exists
log = logging.getLogger('sylk.cli.main')

class Core:

    def get_sylk_json(self,*args,**kwargs):
        logging.debug(args)
        if args[0][0] is None:
            current_path = get_current_location()
            destination_path = join_path(current_path,'sylk.json')
            logging.debug("Writing new sylk json {1}".format(args[0][0],destination_path))
            sylkJson = get_blank_sylk_json(True)
            wFile(destination_path,sylkJson,json=True)
            # destination_path = destination_path.replace('sylk.json','.sylk')
            # mkdir(destination_path)
        else:
            logging.debug("Getting sylk json {0}".format(args[0][0]))
            try:
                sylkJson = rFile(args[0][0],json=True)
            except Exception:
                sylkJson = get_blank_sylk_json(True)
                wFile(args[0][0],sylkJson,json=True)

        return sylkJson

    def save_sylk_json(self,*args,**kwargs):
        logging.debug("Saving sylk json {0} {1}".format(args,kwargs))
        wFile(args[0][0],args[0][1][0],json=True,overwrite=True)


class Builder:

    def log(self,hook,command_name,*args,**kwargs):
        logging.debug(f"[EXCUTE-HOOK-{hook.upper()}] {command_name} : {args}")
   
    def add_resource(self,sylkJson,*args,**kwargs):
        request = args[0][0][0]
        for k in request:
            logging.debug(f"Adding resource : {k}")
            if sylkJson.get(k) is None:
                sylkJson[k] = request[k]
            else:
                if k == 'domain':
                    sylkJson[k] = request[k]
                else:
                    for j in request[k]:
                        sylkJson[k][j] = request[k][j]

    def edit_resource(self,sylkJson,resource,args):

        resource = resource[0]
        type = resource.get('type')
        kind = resource.get('kind')

        if type is not None:
            if type == 'descriptors':
                if kind == resources.ResourceKinds.message.value:
                    fullname = resource.get('fullName')
                    pkgname = 'protos/{0}/{1}.proto'.format(fullname.split('.')[2],fullname.split('.')[1])
                    package = sylkJson.get('packages').get(pkgname)
                    if package is not None:

                        index = 0
                        for m in package['messages']:

                            if args[0] is not None and args[0].get('old_name') is not None:

                                if m.get('name') == args[0].get('old_name'):
                                    sylkJson['packages'][pkgname]['messages'][index] = resource
                                    break

                            if m.get('fullName') == resource.get('fullName'):
                                
                                sylkJson['packages'][pkgname]['messages'][index] = resource
                                try:
                                    sort_topological = Graph(sylkJson['packages'][pkgname]['messages']).topologicalSort()
                                    temp_messages = []
                                    for m in sort_topological[::-1]:
                                        temp_messages.append(next((tmpM for tmpM in sylkJson['packages'][pkgname]['messages'] if tmpM.get('fullName') == m),None))
                                    sylkJson['packages'][pkgname]['messages'] = temp_messages
                                except KeyError as e:
                                    print_warning("Error while sorting the dependencies graph of package messages\n\t- If this error appeared right after making rename of message then ignore it...\n\t- Else please issue a bug report !")
                                
                                # sylkJson['packages'][pkgname]['messages'].insert(len(sylkJson['packages'][pkgname]['messages']), removed_message)
                                break
                            index += 1
                elif kind == resources.ResourceKinds.method.value:
                    pass
                elif kind == resources.ResourceKinds.enum.value:
                    fullname = resource.get('fullName')
                    pkgname = 'protos/{0}/{1}.proto'.format(fullname.split('.')[2],fullname.split('.')[1])
                    package = sylkJson.get('packages').get(pkgname)
                    if package is not None:
                        index = 0
                        for e in package['enums']:
                            if e.get('fullName') == resource.get('fullName'):
                                sylkJson['packages'][pkgname]['enums'][index] = resource
                                break
                            index += 1
                elif kind == resources.ResourceKinds.enum_value.value:
                    pass
                elif kind == resources.ResourceKinds.field.value:
                    pass
            elif type == 'packages':
                fullname = resource.get('package')
                pkgname = 'protos/{0}/{1}.proto'.format(fullname.split('.')[2],fullname.split('.')[1])
                package = sylkJson.get('packages').get(pkgname)
                if package is not None:
                    sylkJson['packages'][pkgname] = resource
            elif type == 'services':
                sylkJson['services'][resource.get('name')] = resource

    def remove_resource(self,sylkJson,full_name,*args,**kwargs):
        """Removing sylk.build resource by full name identifier"""

        removed = False
        full_name = full_name[0]

        if len(full_name.split('.')) == 4:

            if sylkJson.get('packages') is not None:
                pkg_name = 'protos/{0}/{1}.proto'.format(full_name.split('.')[2],full_name.split('.')[1])
                if pkg_name in sylkJson.get('packages'):

                    # Handling deletion of message
                    for m in sylkJson['packages'][pkg_name]['messages']:
                        if m.get('fullName') == full_name:
                            sylkJson['packages'][pkg_name]['messages'].remove(m)
                            removed = True

                    # Handling deletion of enum
                    if removed == False and sylkJson['packages'][pkg_name].get('enums') is not None:
                        for e in sylkJson['packages'][pkg_name]['enums']:
                            if e.get('fullName') == full_name:
                                sylkJson['packages'][pkg_name]['enums'].remove(e)
                                removed = True
                else:
                    print_error("Coludnt find {} under packages".format(full_name))

            # Handling deletion of RPC
            if removed == False and sylkJson.get('services') is not None:
                if full_name.split('.')[1] in sylkJson.get('services'):
                    svc = sylkJson['services'][full_name.split('.')[1]]
                    for r in svc.get('methods'):
                        if r.get('name') == full_name.split('.')[-1]:
                            svc['methods'].remove(r)
                            removed = True
        elif len(full_name.split('.')) == 6:
            # Handling removal of oneof fields
            if sylkJson.get('packages') is not None:
                pkg_name = 'protos/{0}/{1}.proto'.format(full_name.split('.')[2],full_name.split('.')[1])
                if pkg_name in sylkJson.get('packages'):
                    if sylkJson['packages'][pkg_name].get('messages') is not None:
                        index_msgs = 0
                        for m in sylkJson['packages'][pkg_name].get('messages'):
                            field_name = '.'.join(full_name.split('.')[:-1])
                            field = next((f for f in m.get('fields') if f.get('fullName') == field_name),None)
                            if field is not None:
                                field_index = m.get('fields').index(field)
                                oneof_field = next((one_f for one_f in field.get('oneofFields') if one_f.get('fullName') == full_name),None)
                                if oneof_field is not None:
                                    print_info(f'{pkg_name=} | {index_msgs=} | {field_index=}')
                                    sylkJson['packages'][pkg_name]['messages'][index_msgs]['fields'][field_index]['oneofFields'].remove(oneof_field)
                                    removed = True
                                    break
                            index_msgs += 1

        else:
            # Removing fields or enum values
            if sylkJson.get('packages') is not None:
                pkg_name = 'protos/{0}/{1}.proto'.format(full_name.split('.')[2],full_name.split('.')[1])
                
                if pkg_name in sylkJson.get('packages'):

                    # Handling deletion of message field
                    if sylkJson['packages'][pkg_name].get('messages') is not None:
                        index_msgs = 0
                        for m in sylkJson['packages'][pkg_name].get('messages'):
                            field = next((f for f in m.get('fields') if f.get('fullName') == full_name),None)
                            if field is not None:
                                sylkJson['packages'][pkg_name]['messages'][index_msgs]['fields'].remove(field)
                                removed = True
                                break
                            index_msgs += 1

                    # Handling deletion of enum value
                    if sylkJson['packages'][pkg_name].get('enums') is not None:
                        if removed == False:
                            index_enums = 0
                            for e in sylkJson['packages'][pkg_name].get('enums'):
                                ev = next((ev for ev in e.get('values') if ev.get('fullName') == full_name),None)
                                if ev is not None:
                                    sylkJson['packages'][pkg_name]['enums'][index_enums]['values'].remove(ev)

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