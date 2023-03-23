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

from sylk.builder.src.main import SylkBuilder
from sylk.commons.config import parse_project_config

def build_all(path:str):
    prj_configs = parse_project_config(path,proto=True)
    sylkBuilder = SylkBuilder(path=path,configs=prj_configs)
    sylkBuilder.BuildAll()

def build_code(path:str):
    prj_configs = parse_project_config(path,proto=True)
    sylkBuilder = SylkBuilder(path=path,configs=prj_configs)
    sylkBuilder.BuildOnlyCode()

def build_protos(path:str):
    prj_configs = parse_project_config(path,proto=True)
    sylkBuilder = SylkBuilder(path=path,configs=prj_configs)
    sylkBuilder.BuildOnlyProtos()