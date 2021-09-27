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

    compiled = False
    cwd = os.getcwd()
    directory = "/tmp/invoice-" + str(md5(kwargs["DETAILS"], kwargs["directory"]))[:12]
    if not os.path.exists(directory):
        log.debug("Creating new temp directory")
        os.mkdir(directory)
    elif kwargs["clean"]:
        log.warn("No change in details.yml; but recompiling `--clean`.")
    else:
        log.warn("No change in details.yml; not recompiling.")
        compiled = True

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

    def item_to_line(item: dict) -> str:
        item["sum"] = format_digit(item["amount"] * item["item_price_cents"])
        item["item_price_cents"] = format_digit(item["item_price_cents"])
        return "{description} & {amount} & {item_price_cents} & {sum} \\\\".format(
            **item
        )

    def sum_items(items: dict) -> int:
        result = 0
        for item in items:
            result += item["item_price_cents"] * item["amount"]
        return result

    strings = load_yaml("strings.yaml")
    invoice_tex = "{name}.tex".format(name=translate("invoice"))
    invoice_pdf = "{name}.pdf".format(name=translate("invoice"))
    invoice_id = details["invoice_id"]
    datestr = datetime.today().strftime(date)

    def show_invoice():
        log.debug("Opening pdf viewer")
        os.chdir(directory)
        subprocess.Popen(["evince", invoice_pdf])

    def copy_invoice():
        log.debug("Copying file to local directory")
        os.chdir(directory)
        subprocess.Popen(
            ["cp", invoice_pdf, cwd + "/" + invoice_pdf[:-4] + "_" + datestr + ".pdf"]
        )

    if compiled:
        show_invoice()
        copy_invoice()
        return

    log.info("Using temp directory: " + directory)

    items_table = ""
    total_cost = 0

    # check if the items_table needs to be created.
    if details.get("items"):
        log.info("Noticed multiple line items. Creating table")
        if details.get("description"):
            # there is still a 'normally' defined item. Include as first
            details["items"].insert(
                0,
                {
                    "description": details["description"],
                    "amount": details.get("amount") or details.get("hours_worked"),
                    "item_price_cents": details.get("item_price_cents")
                    or details.get("hourly_rate_cents"),
                },
            )
        total_cost = sum_items(details["items"])
        items_table = "".join(item_to_line(i) for i in details["items"])
    else:
        total_cost = (details.get("hours_worked") or details.get("amount")) * (
            details.get("hourly_rate_cents") or details.get("item_price_cents")
        )

    data = {
        "user": userdata,
        "client": client,
        "details": details,
        "datestr": datestr,
        "total_cost": total_cost,
        "invoice": details,
        "items_table": items_table,
    }

    strings = load_yaml("strings.yaml")

    log.debug("Creating jinja2 substitution environment")

    env = jinja2.Environment(
        block_start_string="\BLOCK{",
        block_end_string="}",
        variable_start_string="\VAR{",
        variable_end_string="}",
        comment_start_string="\#{",
        comment_end_string="}",
        line_statement_prefix="%#",
        line_comment_prefix="%%",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(".")),
    )

    env.filters["formatdigit"] = format_digit
    env.filters["t"] = translate

    with open(directory + "/" + invoice_tex, "w") as fh:
        log.debug("Writing templated TeX file")
        template = env.get_template("template.tex")
        fh.write(template.render(section1="Long Form", section2="Short Form", **data))

    cwd = os.getcwd()
    os.chdir(directory)

    for i in range(2):
        log.debug("Compile LaTeX, round {}".format(i + 1))
        try:
            subprocess.check_call(["pdflatex", "-interaction=batchmode", invoice_tex])
        except subprocess.CalledProcessError:
            pass

    show_invoice()
    copy_invoice()


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
