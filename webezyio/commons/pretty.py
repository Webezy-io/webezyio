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

from pprint import pprint as pretty

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_success(message):
    print(bcolors.OKGREEN+"[*]",str(message)+bcolors.ENDC)


def print_note(message,pprint=False,tag=None):
    if pprint:
        sep = '-'*45
        if tag is not None:
            print_note(tag)
        print(bcolors.OKBLUE+sep+bcolors.ENDC)
        pretty(message)
        print(bcolors.OKBLUE+sep+bcolors.ENDC)

    else:
        print(bcolors.OKBLUE+"[*]"+bcolors.ENDC,message)


def print_info(message,pprint=False,tag=None):
    if pprint:
        sep = '-'*45
        if tag is not None:
            print_info(tag)
        print(bcolors.OKCYAN+sep+bcolors.ENDC)
        pretty(message)
        print(bcolors.OKCYAN+sep+bcolors.ENDC)

    else:
        print(bcolors.OKCYAN+"[*]"+bcolors.ENDC,message)

def print_warning(message):
    print(bcolors.WARNING+"[!]",str(message)+bcolors.ENDC)

def print_version(version):
    sep = '*'*30
    print('',bcolors.OKCYAN+sep+bcolors.ENDC,'\n',f'\twebezyio : {version}\n',bcolors.OKCYAN+sep+bcolors.ENDC)

def print_error(message,pprint=False,tag=None):
    if pprint:
        sep = '-'*45
        if tag is not None:
            print_error(tag)
        print(bcolors.FAIL+sep+bcolors.ENDC)
        pretty(message)
        print(bcolors.FAIL+sep+bcolors.ENDC)

    else:
        print(bcolors.FAIL+"[!]"+bcolors.ENDC,message)
