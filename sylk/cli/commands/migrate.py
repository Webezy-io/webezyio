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

from typing import Literal
from sylk.builder.plugins import SylkMigrate
from sylk.builder.src.main import SylkBuilder
from sylk.commons import file_system as _fs, pretty as  _pretty
import sys

from sylk.commons.protos import SylkServer_pb2, SylkClient_pb2

def migrate_project(protos_directory:str,output_path:str,format:Literal['json','python']='json',server_language=SylkServer_pb2.ServerLanguages.Name(SylkServer_pb2.python),clients=[SylkClient_pb2.ClientLanguages.Name(SylkClient_pb2.python)]):
    if format == 'python':
        raise Exception("Cannot process a migration plan into python file ! only json format is supported right now.")
    _pretty.print_info((output_path,format),True,'Starting migration process ->')
    wzcoder = SylkBuilder(path=output_path,hooks=[SylkMigrate])
    # wzcoder.PreBuild()
    if _fs.get_current_location() not in sys.path:
        sys.path.append(_fs.get_current_location())
    wzcoder.ParseProtosToResource(protos_dir=protos_directory,project_name='TEST-PROJECT',server_language=server_language,clients=clients)
    wzcoder.PostBuild()
