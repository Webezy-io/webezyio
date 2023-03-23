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

from sylk.architect.interfaces import  ICommand
from sylk.architect.recievers import Core,Builder

class Logger(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,sylkJson,*args,**kwargs):
        self._builder.log(sylkJson,args,**kwargs)


# Builder commands

class InitProject(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,*args):
        self._builder.create_new_project(args)

class SetDomain(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,sylkJson,*args,**kwargs):
        self._builder.set_domain(sylkJson,args,**kwargs)

class AddResource(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,sylkJson,*args,**kwargs):
        self._builder.add_resource(sylkJson,args,**kwargs)

class EditResource(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,sylkJson,resource,*args):
        self._builder.edit_resource(sylkJson,resource,args)

class RemoveResource(ICommand):
    def __init__(self, builder:Builder):
        self._builder = builder

    def execute(self,sylkJson,full_name,*args):
        self._builder.remove_resource(sylkJson,full_name,*args)


class CreateNewProject(ICommand):
    def __init__(self, creator:Builder):
        self._creeator = creator

    def execute(self,sylkJson,*args,**kwargs):
        self._creeator.create_new_project(sylkJson,args,**kwargs)


# Analayzer commands

class GetSylkJson(ICommand):
    def __init__(self, analayzer:Core):
        self._core = analayzer

    def execute(self,*args,**kwargs):
        return self._core.get_sylk_json(args,kwargs)

class SaveSylkJson(ICommand):
    def __init__(self, analayzer:Core):
        self._core = analayzer

    def execute(self,*args,**kwargs):
        self._core.save_sylk_json(args,kwargs)
