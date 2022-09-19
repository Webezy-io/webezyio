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
    print(bcolors.OKGREEN+"[*]",message+bcolors.ENDC)


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
    print(bcolors.WARNING+"[!]",message+bcolors.ENDC)

def print_version(version):
    sep = '*'*30
    print('',bcolors.OKCYAN+sep+bcolors.ENDC,'\n',f'\twebezyio : {version}\n',bcolors.OKCYAN+sep+bcolors.ENDC)

def print_error(message):
    print(bcolors.FAIL+"[!]",message+bcolors.ENDC)
