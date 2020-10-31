from datetime import datetime
import readline
import logging
import subprocess
import sys
import os

import jinja2

# from .invoice import SingleInvoice, HourlyInvoice, Invoice
from .utils import *


def create_invoice(details, userdata, client, date, locale, **kwargs):
    def translate(key):
        if key in strings:
            return strings[key][locale]
        else:
            print("Translation key for '{key}' is missing".format(key=key))
            exit()

    def format_digit(integer):
        integer = integer / 100
        string = "{0:.2f}".format(integer)
        if details["locale"] == "de":
            string = string.replace(".", ",")
        return string


    invoice_id = details["invoice_id"]
    # invoice = HourlyInvoice()

    datestr = datetime.today().strftime(date)

    data = {
        "user": userdata,
        "client": client, # load_yaml("recipients/{id}.yaml".format(id=invoice.recipient)), # client
        "details": details,
        "datestr": datestr,
        "total_cost": details["hours_worked"] * details["hourly_rate_cents"],
        # "invoice": ""
        "invoice": details   # details
        # "config": details  # details
    }

    strings = load_yaml("strings.yaml")

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

    env.filters['formatdigit'] = format_digit
    env.filters['t'] = translate


    directory = "/tmp/invoice-" + str(md5(kwargs["DETAILS"]))[:12]  # str(invoice.id)
    if not os.path.exists(directory):
        os.mkdir(directory)

    print(directory)
    invoice_tex = '{name}.tex'.format(name=translate("invoice"))
    invoice_pdf = '{name}.pdf'.format(name=translate("invoice"))

    with open(directory + "/" + invoice_tex, "w") as fh:
        template = env.get_template('template.tex')
        fh.write(template.render(section1='Long Form', section2='Short Form', **data))

    cwd = os.getcwd()
    os.chdir(directory)

    for _ in range(2):
        try:
            subprocess.check_call(['pdflatex', '-interaction=batchmode', invoice_tex])
        except subprocess.CalledProcessError:
            pass
        # remove_tmp_files(translate("invoice"))
    # subprocess.check_call(['evince', invoice_pdf])
    subprocess.Popen(['evince', invoice_pdf])
    subprocess.Popen(['cp', invoice_pdf, cwd + "/" + invoice_pdf[:-4] + "_" + datestr + ".pdf"])

    # originally:
    # invoice.locale = "de"
    # invoice.id
    # invoice.title
    # invoice.recipient
    # invoice.description
    # invoice.range  # timeframe
    # invoice.price  # calculate
    # invoice.hours
    # invoice.minutes
    # invoice.per_hour  # hourly rate
    # invoice.mode = "hourly"
    # invoice.date = date

    # save_yaml(vars(invoice), directory + "/data.yaml")
    # save_yaml(config, "config.yaml")


def compile_invoice(id):
    pass
    # directory = invoice_dir + "/" + str(id)
    # if os.path.exists(directory + "/locked"):
    #     print("The invoice has already been locked")
    #     exit()
    # invoicedata = load_yaml(directory + "/data.yaml")
    # mode = invoicedata["mode"]
    # del invoicedata["mode"]
    # if mode == "single":
    #     invoice = SingleInvoice(**invoicedata)
    # elif mode == "hourly":
    #     invoice = HourlyInvoice(**invoicedata)
    # else:
    #     invoice = Invoice(**invoicedata)
    # env = jinja2.Environment(
    #     block_start_string='\BLOCK{',
    #     block_end_string='}',
    #     variable_start_string='\VAR{',
    #     variable_end_string='}',
    #     comment_start_string='\#{',
    #     comment_end_string='}',
    #     line_statement_prefix='%#',
    #     line_comment_prefix='%%',
    #     trim_blocks=True,
    #     autoescape=False,
    #     loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    # )
    # userdata = load_yaml("from.yaml")
    # userdata["country"] = userdata["countryDE"] if invoice.locale == "de" else userdata["countryEN"]
    # data = {
    #     "user": userdata, # user
    #     "to": load_yaml("recipients/{id}.yaml".format(id=invoice.recipient)), # client
    #     "invoice": invoice,   # details
    #     "config": config  # details
    # }

    # strings = load_yaml("strings.yaml")

    # def translate(key):
    #     if key in strings:
    #         return strings[key][invoice.locale]
    #     else:
    #         print("Translation key for '{key}' is missing".format(key=key))
    #         exit()

    # def format_digit(integer):
    #     integer = integer / 100
    #     string = "{0:.2f}".format(integer)
    #     if invoice.locale == "de":
    #         string = string.replace(".", ",")
    #     return string

    # def format_date(date):
    #     """

    #     :type date: datetime.datetime
    #     """
    #     # if invoice.locale == "de":
    #     #     return date.strftime("%d. %m. %Y")
    #     # else:
    #     return date.strftime("%Y-%m-%d")

    # env.filters['formatdigit'] = format_digit
    # env.filters['formatdate'] = format_date
    # env.filters['t'] = translate
    # with open(directory + "/{name}.tex".format(name=translate("invoice")), "w") as fh:
    #     template = env.get_template('template.tex')
    #     fh.write(template.render(section1='Long Form', section2='Short Form', **data))
    # os.chdir(directory)
    # for _ in range(2):
    #     subprocess.check_call(['pdflatex', '-interaction=nonstopmode', '{name}.tex'.format(name=translate("invoice"))])
    # print(directory)
    # remove_tmp_files(translate("invoice"))


def sign_invoice(id):
    pass
    # directory = invoice_dir + "/" + str(id)
    # if os.path.exists(directory + "/locked"):
    #     print("The invoice has already been locked")
    #     exit()
    # if os.path.exists(directory + "/Rechnung.pdf"):
    #     name = "Rechnung"
    # elif os.path.exists(directory + "/Invoice.pdf"):
    #     name = "Invoice"
    # else:
    #     print("Invoice not found")
    #     name = ""
    #     exit()
    # command = [
    #     "/usr/local/PDF-Over/scripts/pdf-over_linux.sh",
    #     "-i", "{dir}/{name}.pdf".format(dir=directory, name=name),
    #     "-o", "{dir}/{name}_{signed}.pdf".format(
    #         dir=directory, name=name, signed=("signiert" if name == "Rechnung" else "signed")
    #     ),
    #     "-b", "LOCAL",  # use local Bürgerkarte
    #     "-a",  # automatically position signature
    #     "-v", "true" if name == "Rechnung" else "false",  # set visibility
    #     "-s"  # save without asking
    # ]
    # print(" ".join(command))
    # subprocess.check_call(command)
