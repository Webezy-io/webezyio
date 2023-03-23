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
import subprocess
from typing import List, Literal
from webezyio.cli.prompter import QCheckbox,QConfirm,QList,QText,ask_user_question
from webezyio.cli.theme import WebezyTheme
from webezyio.commons import file_system,protos
from webezyio.commons.helpers import WZEnumValue, WZField,_BUILTINS_TEMPLATES, WZJson
from webezyio.commons.platform import WebezyPlatform
from webezyio.commons.pretty import print_info,print_warning,print_error,print_note,print_success
from webezyio.commons.file_system import join_path,mkdir, wFile
from webezyio.architect import WebezyArchitect
import os
import inquirer
from inquirer import errors
from google.protobuf.json_format import MessageToDict

_do_not_change=['uri','type','kind','clients','server']

def pull_changes(architect:WebezyArchitect,wz_json: WZJson,remote:str='',force:bool=False):
    print_info('Pulling remote project resources "{}"...'.format(remote))
    root = os.getcwd()
    stub = WebezyPlatform(root)
    prj = MessageToDict(stub.dump_project(remote))
    keys = ['project','packages','services']
    for k in keys:
        compare_changes(force,architect._webezy.webezyJson,prj,k)
    architect.Save()
    
    
def compare_changes(force,wz_json,remote,key):
    print_info('\t* Checking deltas -> {}...'.format(key))
    x = wz_json[key]
    y = remote[key]
    shared_items = {k: x[k] for k in x if k in y and x[k] == y[k]}
    # if key in ['packages','services']:
        # print(key,len(shared_items))
    if force:
        added, removed, modified, same = dict_compare(y,x)
        for k in modified:
            if k not in _do_not_change:
                wz_json[key][k]=modified[k][0]
                print_note('{} -> {}'.format(modified[k][1],modified[k][0]),True,'Modified '+key)
        for k in added:
            print_note('{}'.format(k),True,'Added '+key)
            wz_json[key][k] = y[k]
        for k in removed:
            print_note('{}'.format(k),True,'Removed '+key)
            del wz_json[key][k]
    else:
        added, removed, modified, same = dict_compare(x,y)
        if len(added) > 0:
            print('Added',added)
        if len(removed) > 0:
            print('Removed',removed)
        if len([k for k in modified.keys() if k not in _do_not_change]) > 0:
            print_warning('Remote repo is not updated with local changes.\nplease push the changes before pulling or use "--force" flag to overwrite changes')
            exit(1)
        added, removed, modified, same = dict_compare(y,x)
        for k in modified:
            if k not in _do_not_change:
                wz_json[key][k]=modified[k][0]
                print_note('{} -> {}'.format(modified[k][1],modified[k][0]),True,'Modified '+key)
        for k in added:
            print_note('{}'.format(k),True,'Added '+key)
            wz_json[key][k] = y[k]
        for k in removed:
            print_note('{}'.format(k),True,'Removed '+key)
            del wz_json[key][k]


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same