import os
from glob import glob

import dateparser
import yaml


def load_yaml(filename):
    with open(filename, 'r') as stream:
        return yaml.load(stream)


def save_yaml(data, filename):
    with open(filename, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def remove_tmp_files(base):
    for ext in ["aux", "log"]:
        os.remove(base + "." + ext)


def get_possible_recipents():
    return [os.path.splitext(os.path.basename(file))[0] for file in glob("recipients/*.yaml")]


def ask(question, validator=None, default=None, set=None):
    while True:
        string = question + (" [{default}]".format(default=default) if default else "") + ": "
        answer = input(string)
        if answer == "":
            if default:
                answer = default
                print("\033[F" + string + str(answer))
            else:
                continue
        if validator == "float":
            try:
                answer = float(answer)
            except ValueError:
                continue
        if validator == "money":
            try:
                answer = int(float(answer) * 100)
            except ValueError:
                continue
        if validator == "int":
            try:
                answer = int(answer)
            except ValueError:
                continue
        if validator == "date":
            answer = dateparser.parse(answer).date()
            if answer is None:
                continue
        if validator == "set":
            if answer not in set:
                print("only [{formats}] are allowed".format(formats=", ".join(set)))
                continue
        if validator == "boolean":
            if answer.lower() in ['true', '1', 't', 'y', 'yes']:
                return True
            elif answer.lower() in ["false", "0", "f", "n", "no"]:
                return False
            else:
                continue
        return answer
