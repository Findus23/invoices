import os
import subprocess

import jinja2

from utils import load_yaml, remove_tmp_files

env = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%#',
    line_comment_prefix='%%',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)

DATA = {
    "invoice_id": 1234,
    "invoice_date": "01.03.2018"
}

DATA["from"] = load_yaml("from.yaml")
DATA["to"] = load_yaml("recipents/{id}.yaml".format(id="innocraft"))

# invoice = {
#     "mode": "single",
#     "description": "TESTOBJEKT",
#     "timerange": "18.12.2016 - 28.02.2017",
#     "price": 400,
#     "locale": "de"
# }
invoice = {
    "mode": "hourly",
    "title": "Example Invoice",
    "description": "Example",
    "timerange": "18.12.2016 - 28.02.2017",
    "hours": 35,
    "per_hour": 21,
    "locale": "en"
}

invoice["total"] = invoice["per_hour"] * invoice["hours"]

DATA["invoice"] = invoice

strings = load_yaml("strings.yaml")


def translate(key):
    if key in strings:
        return strings[key][invoice["locale"]]
    else:
        print("Translation key for '{key}' is missing".format(key=key))
        exit()


def format_digit(integer):
    string = "{0:.2f}".format(integer)
    if invoice["locale"] == "de":
        string = string.replace(".", ",")
    return string


env.filters['formatdigit'] = format_digit
env.filters['t'] = translate
with open("output.tex", "w") as fh:
    template = env.get_template('template.tex')
    fh.write(template.render(section1='Long Form', section2='Short Form', **DATA))
subprocess.check_call(['pdflatex', 'output.tex'])
remove_tmp_files("output")
