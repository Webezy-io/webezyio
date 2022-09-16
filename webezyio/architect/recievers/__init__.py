import logging

from webezyio.commons.resources import get_blank_webezy_json
from webezyio.commons.file_system import rFile, wFile, get_current_location, join_path, check_if_file_exists

class Core:

    def get_webezy_json(self,*args,**kwargs):
        logging.debug(args)
        if args[0][0] is None:
            current_path = get_current_location()
            destination_path = join_path(current_path,'webezy.json')
            logging.debug("Writing new webezy json {1}".format(args[0][0],destination_path))
            wzJson = get_blank_webezy_json(True)
            wFile(destination_path,wzJson,json=True)
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
        logging.info(f"[EXCUTE-HOOK-{hook.upper()}] {command_name} : {args}")
   
    def add_resource(self,webezyJson,*args,**kwargs):
        request = args[0][0][0]
        for k in request:
            logging.debug(f"Adding resource : {k}")
            if webezyJson.get(k) is None:
                webezyJson[k] = request[k]
            else:
                for j in request[k]:
                    webezyJson[k][j] = request[k][j]

    def remove_resource(self,webezyJson,*args,**kwargs):
        logging.debug("Removing resource")

    def create_new_project(self,*args,**kwargs):
        logging.debug("Create new project {0}".format(args))

    def set_domain(self,*args,**kwargs):
        # logging.debug(args[0])
        args[0]['domain'] = args[1][0][0]
        logging.debug("Setting project domain {0}".format(args[1][0][0]))