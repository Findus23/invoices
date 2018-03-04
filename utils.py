import os

import yaml


def load_yaml(filename):
    with open(filename, 'r') as stream:
        return yaml.load(stream)


def remove_tmp_files(base):
    for ext in ["aux", "log"]:
        os.remove(base + "." + ext)
