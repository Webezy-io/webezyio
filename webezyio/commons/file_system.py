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
from pathlib import Path
import os
import json as JSON
import shutil
from distutils.dir_util import copy_tree


def mv(old_path, new_path):
    if check_if_file_exists(old_path):
        os.rename(old_path, new_path)


def mkdir(path):
    if check_if_dir_exists(path) == False:
        os.mkdir(path)
    else:
        logging.debug("Directory is already exists ! {0}"
                      .format(path))

def cpDir(dir_path,target_path):
    if check_if_dir_exists(dir_path):
        copy_tree(dir_path, target_path)


def removeFile(path):
    os.remove(path)

def walkDirs(path):
    return [x[0] for x in os.walk(path)]

def walkFiles(path):
    for p in os.walk(path):
        return p[2]


def copyFile(file, new_file):
    shutil.copy2(file, new_file)


def wFile(path, content, overwrite=False, json=False,force=False):
    if check_if_file_exists(path) == True:
        if force:
            os.makedirs(os.path.dirname(path),mode=0o777, exist_ok=True)
            os.chmod(os.path.dirname(path),0o777)
        if overwrite == True:
            if json:
                # Serializing json
                json_object = JSON.dumps(content, indent=4)
                # Writing to sample.json
                logging.debug(f"Overwriting json file {path}")
                with open(path, "w") as outfile:
                    outfile.write(json_object)
            else:

                logging.debug(f"Overwriting file {path}")
                with open(path, 'w') as file:
                    file.write(content)
                    file.close()
        else:
            logging.debug("{0} File is already existing ! [pass function with 'overwrite' argument if you want to override this behaviour]"
                          .format(path))
    else:
        if force:
            os.makedirs(os.path.dirname(path),mode=0o777, exist_ok=True)
            os.chmod(os.path.dirname(path),0o777)
        if json:
            # Serializing json
            json_object = JSON.dumps(content, indent=4)
            # Writing to sample.json
            logging.debug(f"Writing json file {path}")
            with open(path, "w") as outfile:
                outfile.write(json_object)
        else:
            logging.debug(f"Writing file {path}")
            with open(path, 'w') as file:
                file.write(content)
                file.close()


def rFile(path, json=False):
    logging.debug(f"Reading file -> {path}")
    if check_if_file_exists(path) == True:
        if json:
            f = open(path)
            data = JSON.load(f)
            f.close()
            return data
        else:
            with open(path, 'r') as file:
                lines = file.readlines()
                file.close()
                return lines
    else:
        raise Exception("File path is not valid ! {0}".format(path))


def check_if_dir_exists(dir_path):
    return os.path.isdir(dir_path)


def check_if_file_exists(file_path):
    return Path(file_path).exists()


def join_path(*paths):
    return os.path.join(*paths)


def get_current_location():
    return os.getcwd()
