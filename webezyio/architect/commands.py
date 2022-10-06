from webezyio.architect.interfaces import  ICommand
from webezyio.architect.recievers import Core,Builder

class Logger(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,webezyJson,*args,**kwargs):
        self._builder.log(webezyJson,args,**kwargs)


# Builder commands

class InitProject(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,*args):
        self._builder.create_new_project(args)

class SetDomain(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,webezyJson,*args,**kwargs):
        self._builder.set_domain(webezyJson,args,**kwargs)

class AddResource(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,webezyJson,*args,**kwargs):
        self._builder.add_resource(webezyJson,args,**kwargs)

class EditResource(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,webezyJson,resource,*args):
        self._builder.edit_resource(webezyJson,resource=resource)

class RemoveResource(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,webezyJson,full_name,*args):
        self._builder.remove_resource(webezyJson,full_name,*args)


class CreateNewProject(ICommand):
    def __init__(self, creator:Builder):
        self._creeator = creator

    def execute(self,webezyJson,*args,**kwargs):
        self._creeator.create_new_project(webezyJson,args,**kwargs)


# Analayzer commands

class GetWebezyJson(ICommand):
    def __init__(self, analayzer:Core):
        self._core = analayzer

    def execute(self,*args,**kwargs):
        return self._core.get_webezy_json(args,kwargs)

class SaveWebezyJson(ICommand):
    def __init__(self, analayzer:Core):
        self._core = analayzer

    def execute(self,*args,**kwargs):
        self._core.save_webezy_json(args,kwargs)
