# noinspection PyUnresolvedReferences
import readline
import subprocess
import sys

import jinja2

from invoice import SingleInvoice, HourlyInvoice, Invoice
from utils import *


def create_invoice():
    current_id = config["last_id"]
    mode = ask("Mode", "set", set=["single", "hourly"], default="hourly")
    if mode == "single":
        invoice = SingleInvoice()
    elif mode == "hourly":
        invoice = HourlyInvoice()
    else:
        invoice = Invoice()
    current_id += 1
    config["last_id"] = current_id
    invoice.locale = ask("locale", "set", set=["de", "en"], default="de")
    invoice.id = ask("id", "int", default=current_id)
    invoice.title = ask("title")
    invoice.recipient = ask("recipient", "set", set=get_possible_recipents(), default=config["default_recipient"])
    invoice.date = ask("date", "date", default="today")
    invoice.description = ask("description")
    invoice.range = ask("range")

    if invoice.mode == "single":
        invoice.price = ask("price", "money")

    elif invoice.mode == "hourly":
        invoice.hours = ask("hours", "int")
        invoice.minutes = ask("minutes", "int")
        invoice.per_hour = ask("per hour", "money", default=config["default_hourly_rate"])
    directory = invoice_dir + "/" + str(invoice.id)
    if os.path.exists(directory):
        if not ask("overwrite", "boolean"):
            exit()
    else:
        os.mkdir(directory)
    save_yaml(vars(invoice), directory + "/data.yaml")
    save_yaml(config, "config.yaml")


def compile_invoice(id):
    directory = invoice_dir + "/" + str(id)
    if os.path.exists(directory + "/locked"):
        print("The invoice has already been locked")
        exit()
    invoicedata = load_yaml(directory + "/data.yaml")
    mode = invoicedata["mode"]
    del invoicedata["mode"]
    if mode == "single":
        invoice = SingleInvoice(**invoicedata)
    elif mode == "hourly":
        invoice = HourlyInvoice(**invoicedata)
    else:
        invoice = Invoice(**invoicedata)
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
    data = {
        "from": load_yaml("from.yaml"),
        "to": load_yaml("recipients/{id}.yaml".format(id=invoice.recipient)),
        "invoice": invoice,
        "config": config
    }

    strings = load_yaml("strings.yaml")

    def translate(key):
        if key in strings:
            return strings[key][invoice.locale]
        else:
            print("Translation key for '{key}' is missing".format(key=key))
            exit()

    def format_digit(integer):
        integer = integer / 100
        string = "{0:.2f}".format(integer)
        if invoice.locale == "de":
            string = string.replace(".", ",")
        return string

    def format_date(date):
        """

        :type date: datetime.datetime
        """
        if invoice.locale == "de":
            return date.strftime("%d. %m. %Y")
        else:
            return date.strftime("%Y-%m-%d")

    env.filters['formatdigit'] = format_digit
    env.filters['formatdate'] = format_date
    env.filters['t'] = translate
    with open(directory + "/{name}.tex".format(name=translate("invoice")), "w") as fh:
        template = env.get_template('template.tex')
        fh.write(template.render(section1='Long Form', section2='Short Form', **data))
    os.chdir(directory)
    for _ in range(2):
        subprocess.check_call(['pdflatex', '{name}.tex'.format(name=translate("invoice"))])
    print(directory)
    remove_tmp_files(translate("invoice"))


def sign_invoice(id):
    directory = invoice_dir + "/" + str(id)
    if os.path.exists(directory + "/locked"):
        print("The invoice has already been locked")
        exit()
    if os.path.exists(directory + "/Rechnung.pdf"):
        name = "Rechnung"
    elif os.path.exists(directory + "/Invoice.pdf"):
        name = "Invoice"
    else:
        print("Invoice not found")
        name = ""
        exit()
    command = [
        "/usr/local/PDF-Over/scripts/pdf-over_linux.sh",
        "-i", "{dir}/{name}.pdf".format(dir=directory, name=name),
        "-o", "{dir}/{name}_{signed}.pdf".format(
            dir=directory, name=name, signed=("signiert" if name == "Rechnung" else "signed")
        ),
        "-b", "LOCAL",  # use local Bürgerkarte
        "-a",  # automatically position signature
        "-v", "true" if name == "Rechnung" else "false",
        "-s"  # save without asking
    ]
    print(" ".join(command))
    subprocess.check_call(command)


if __name__ == "__main__":
    if len(sys.argv) == 1 or len(sys.argv) > 3 or sys.argv[1] not in ["create", "compile", "sign"]:
        print("please use 'create', 'compile' or 'sign'")
        exit()
    config = load_yaml("config.yaml")
    invoice_dir = config["invoice_dir"]

    if sys.argv[1] == "create":
        create_invoice()
    if sys.argv[1] == "compile" or sys.argv[1] == "sign":
        if len(sys.argv) == 3:
            try:
                invoice_id = int(sys.argv[2])
            except ValueError:
                invoice_id = False
                print("invalid id")
                exit()
        else:
            invoice_id = config["last_id"]
        if sys.argv[1] == "compile":
            compile_invoice(invoice_id)
        else:
            sign_invoice(invoice_id)
