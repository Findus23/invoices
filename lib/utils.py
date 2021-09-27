import os
import readline
import logging
from glob import glob

import dateparser
import yaml
import logging

log = logging.getLogger(__name__)

# noinspection PyStatementEffect
readline  # this does nothing but make sure the import readline is not removed accidently


def load_yaml(filename, root="./"):
    name = ".".join(filename.split(".")[:-1])
    endings = [".yaml", ".yml"]
    err = None
    for end in endings:
        try:
            with open(root + name + end, "r") as stream:
                return yaml.safe_load(stream)
        except FileNotFoundError as e:
            err = e
    log.critical(err)
    log.error("Occured when attempting to load '{}'".format(filename))
    exit(1)


def save_yaml(data, filename):
    with open(filename, "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


def remove_tmp_files(base):
    for ext in ["aux", "log"]:
        os.remove(base + "." + ext)


def get_possible_recipents():
    return [
        os.path.splitext(os.path.basename(file))[0]
        for file in glob("recipients/*.yaml")
    ]


def ask(question, validator=None, default=None, set=None):
    while True:
        string = (
            question
            + (" [{default}]".format(default=default) if default else "")
            + ": "
        )
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
            if answer.lower() in ["true", "1", "t", "y", "yes"]:
                return True
            elif answer.lower() in ["false", "0", "f", "n", "no"]:
                return False
            else:
                continue
        return answer


def get_logging_level(args):
    if args.verbose >= 3:
        return logging.DEBUG
    if args.verbose == 2 or args.validate:
        return logging.INFO
    if args.verbose >= 1:
        return logging.WARNING
    return logging.ERROR


def set_log_level_format(logging_level, format):
    logging.addLevelName(logging_level, format % logging.getLevelName(logging_level))


def md5(fname, root="./"):
    import hashlib

    hash_md5 = hashlib.md5()
    with open(root + fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
