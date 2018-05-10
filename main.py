import subprocess
import sys

import jinja2

from utils import *


def create_invoice():
    current_id = config["last_id"]
    current_id += 1
    config["last_id"] = current_id
    invoice = {
        "locale": ask("locale", "set", set=["de", "en"], default="de"),
        "id": ask("id", "int", default=current_id),
        "title": ask("title"),
        "recipient": ask("recipient", "set", set=get_possible_recipents(), default=config["default_recipient"]),
        "date": ask("date", "date", default="today"),
        "mode": ask("Mode", "set", set=["single", "hourly"], default="hourly"),
        "description": ask("description"),
        "range": ask("range"),
    }
    if invoice["mode"] == "single":
        single = {
            "price": ask("price", "money")
        }
        invoice.update(single)
    elif invoice["mode"] == "hourly":
        hourly = {
            "hours": ask("hours", "int"),
            "minutes": ask("hours", "int"),
            "per_hour": ask("per hour", "money", default=config["default_hourly_rate"])
        }
        invoice.update(hourly)
    invoice["bank_fee"] = ask("bank_fee", "boolean", default=False)
    directory = invoice_dir + "/" + str(invoice["id"])
    if os.path.exists(directory):
        if not ask("overwrite", "boolean"):
            exit()
    else:
        os.mkdir(directory)
    print(invoice)
    save_yaml(invoice, directory + "/data.yaml")
    save_yaml(config, "config.yaml")


def compile_invoice(id):
    directory = invoice_dir + "/" + str(id)
    if os.path.exists(directory + "/locked"):
        print("The invoice has already been locked")
        exit()
    invoice = load_yaml(directory + "/data.yaml")
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
    if invoice["mode"] == "hourly":
        invoice["hourtotal"] = invoice["per_hour"] * (invoice["hours"] + invoice["minutes"] / 60)
        invoice["total"] = invoice["hourtotal"] + config["bank_fee"]
    data = {
        "from": load_yaml("from.yaml"),
        "to": load_yaml("recipients/{id}.yaml".format(id=invoice["recipient"])),
        "invoice": invoice,
        "config": config
    }

    strings = load_yaml("strings.yaml")

    def translate(key):
        if key in strings:
            return strings[key][invoice["locale"]]
        else:
            print("Translation key for '{key}' is missing".format(key=key))
            exit()

    def format_digit(integer):
        integer = integer / 100
        string = "{0:.2f}".format(integer)
        if invoice["locale"] == "de":
            string = string.replace(".", ",")
        return string

    def format_date(date):
        """

        :type date: datetime.datetime
        """
        if invoice["locale"] == "de":
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
    subprocess.check_call([
        "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java",  # force java8
        "-jar", "/usr/local/PDF-Over/lib/pdf-over-gui-4.1.16.jar",
        "-i", "{dir}/{name}.pdf".format(dir=directory, name=name),
        "-o", "{dir}/{name}_{signed}.pdf".format(
            dir=directory, name=name, signed=("signiert" if name == "Rechnung" else "signed")
        ),
        "-b", "LOCAL",  # use local Bürgerkarte
        "-a",  # automatically position signature
        "-v", "true" if name == "Rechnung" else "false",
        "-s"  # save without asking
    ])


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
