import logging
from pathlib import Path
import os
import json as JSON

def mv(old_path,new_path):
    if check_if_file_exists(old_path):
        os.rename(old_path, new_path)

def mkdir(path):
    if check_if_dir_exists(path) == False:
        os.mkdir(path)
    else:
        logging.warning("Directory is already exists ! {0}"
            .format(path))

def wFile(path,content,overwrite=False,json=False):
    if check_if_file_exists(path) == True:
        if overwrite == True:
            if json:
                # Serializing json
                json_object = JSON.dumps(content, indent=4)
                # Writing to sample.json
                with open(path, "w") as outfile:
                    outfile.write(json_object)
            else:
                with open(path, 'w') as file:
                    file.write(content)
                    file.close()
        else:
            logging.warning("{0} File is already existing ! [pass function with 'overwrite' argument if you want to override this behaviour]"
                .format(path))
    else:
        if json:
            # Serializing json
            json_object = JSON.dumps(content, indent=4)
            # Writing to sample.json
            with open(path, "w") as outfile:
                outfile.write(json_object)
        else:
            with open(path, 'w') as file:
                file.write(content)
                file.close()

def rFile(path,json=False):
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