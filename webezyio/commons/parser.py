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

from webezyio.commons import file_system
import re

from webezyio.commons.pretty import print_error

class WebezyParser():

    def __init__(self,**kwargs) -> None:
        if kwargs.get('path'):
            if file_system.check_if_file_exists(kwargs['path']):
                
                self.is_package = False
                self.is_service = False

                file = self.__clean_file(file_system.rFile(kwargs['path']))
                self._metadata = self.__parse_metadata(file)
                
                self._messages = []
                self._enums = []
                self._methods = []

               
            elif file_system.check_if_dir_exists(kwargs['path']):
                pass

    def __remove_newlines(self,text) -> str:
        return re.sub('\n', '', text)

    def __parse_metadata(self,text_lines):
        metadata = {}
        metadata['imports'] = []
        for l in text_lines:
            if 'syntax' in l:
                if 'proto3' not in l:
                    print_error('Not supporting proto syntax other then proto3 !')
                else:
                    metadata['syntax'] = re.sub('"|;','',l.split('=')[1].strip())
            elif 'package' in l:
                metadata['package'] = re.sub(';|\n','',l.split('package ')[1])
            elif 'import' in l:
                metadata['imports'].append(re.sub('"|;','',l.split('import ')[1].strip()))
        return metadata

    def __clean_file(self,text_lines):
        temp_lines = []
        for l in text_lines:
            if '//' not in l:
                temp_lines.append(l)
        return temp_lines