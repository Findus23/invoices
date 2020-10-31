# noinspection PyUnresolvedReferences
import readline
import logging
import subprocess
import sys
import os

import jinja2

from lib.invoice import SingleInvoice, HourlyInvoice, Invoice
from lib.utils import *
from lib.functionality import create_invoice, compile_invoice, sign_invoice

def create_parser():
    import argparse
    parser = argparse.ArgumentParser(
        description="script to help create invoices based on given information, should be easy to use. By default, will print and ask for confirmation on details before creating the invoice. This behavior can be deactivated with `-y|--yes`.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "DETAILS",
        default="details.yml", # originally: `config.yml`
        nargs="?",
        help="file with details and content specific to this invoice",
    )
    parser.add_argument(
        "--locale",
        default="de",
        help="what language the invoice should be in. Ignored if set in `details.yml`",
    )
    parser.add_argument(
        "--user",
        default="self.yml",    # originally: `from.yaml`
        help="your contact details and bank information.",
    )
    parser.add_argument(
        "--clients",
        default="clients/",     # originally: `recipients/`
        help="relative path (folder) in which information about your clients is stored in `<cname>.yml` files."
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="only validate available information and check available functionality, do not actually create invoice",
    )
    # parser.add_argument(
    #     "--finalize",
    #     action="store_true",
    #     help="finish creation of invoice, copies it to the local folder and increases counter id.",
    # )
    # parser.add_argument(
    #     "--sign",
    #     action="store_true",
    #     help="digitally sign invoice with pdf-over (austria only). Only possible in combination with `--finalize`.",
    # )
    # parser.add_argument(
    #     "--pdf-viewer",
    #     default="evince",
    #     help="tool to open the created invoice with, prior to finalizing",
    # )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="make logging output (more) verbose. Default (or 0) is ERROR, -v is WARN, -vv is INFO and -vvv is DEBUG. Can be passed multiple times."
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="do not ask for confirmation before creating the actual invoice",
    )
    parser.add_argument(
        "--nocolor",
        action="store_true",
        help="deactivate colored log output",
    )
    # parser.add_argument(
    #     "--invoice-dir",
    #     default="invoice",
    #     help="directory in which to template the invoice."
    # )
    parser.add_argument(
        "--date",
        default="%Y-%m-%d",
        help="datetime formatting string the invoice should be dated at. Can be a specific day like '2020-09-01'. Defaults to today.",
    )
    # missing arguments:
    # - take part of the config arguments as separate arguments

    return parser


def main(**kwargs):
    # stuff to do:
    # figure out mode:
    # - create
    # - compile
    # - sign ?
    #
    # - autodetection if you actually want to increase invoice number
    #
    # create ?? or
    # get config
    # get invoice dir (create if not existent)
    # get id
    # compile/sign

    log.debug("Loading user and detail files")
    user = load_yaml(kwargs["user"])
    details = load_yaml(kwargs["DETAILS"])

    from lib.validate import validate, validate_user, validate_client, validate_details
    validate(user, "user", validate_user)
    validate(details, "details", validate_details)

    log.debug("Loading client data")
    client_file = kwargs["clients"] + "/" + details["client"] + ".yml"

    # check if clients folder exists, load and validate
    if not os.path.isdir(kwargs["clients"]):
        log.critical("Client folder '" + kwargs["clients"] + "' does not exist.")
        exit(1)

    client = load_yaml(client_file)
    validate(client, "client", validate_client)

    if not ("locale" in details):
        details["locale"] = kwargs["locale"]

    if not ("mins_worked" in details):
        details["mins_worked"] = 0

    if not kwargs["yes"]:
        log.debug("Printing information to user and asking for conformation")
        print("Please check that the following information is correct:")
        print("\nUSER" + "-" * 31)
        for key, item in user.items():
            print(str(item))
        print("\nDETAILS" + "-" * 28)
        for key, item in details.items():
            print(key + ": " + str(item))
        print("\nCLIENT" + "-" * 29)
        for key, item in client.items():
            print(str(item))

        try:
            input("\nCreate Invoice [Enter]")
        except (KeyboardInterrupt, EOFError):
            print()
            log.error("Stopped by user. Not continuing")
            exit(0)

    create_invoice(details, user, client, **kwargs)
    return

    # steps:
    # [x] collect all information (read config.yml, from.yml)
    # [x] validate all data, ensure that it is complete (print to user for conformation)
    # [ ] validate that all required programs are installed for execution run
    #       (pdflatex, pdf-over, evince, ...?)
    # [x] ask for user conformation
    # [ ] template tex and build it (in /tmp/somewhere)
    # [ ] rename file to 'invoice_name.pdf' or sth
    # [ ] show invoice to user
    # [ ] copy invoice and increase id number with --finalize (or similar)
    #
    # [ ] implement 'single'-item mode
    # [ ] Add MwSt calculation
    # [ ] Add optional USt-IdNr field
    # [ ] allow multiple differently described hourly tasks
    # [ ] enable addition of 'Spesen' after-tax
    # [ ] be aware of locales (de/en)

    # if sys.argv[1] == "create":
    #     create_invoice()
    # if sys.argv[1] == "compile" or sys.argv[1] == "sign":
    #     if len(sys.argv) == 3:
    #         try:
    #             invoice_id = int(sys.argv[2])
    #         except ValueError:
    #             invoice_id = False
    #             print("invalid id")
    #             exit()
    #     else:
    #         invoice_id = config["last_id"]
    #     if sys.argv[1] == "compile":
    #         compile_invoice(invoice_id)
    #     else:
    #         sign_invoice(invoice_id)


if __name__ == "__main__":
    args = create_parser().parse_args()

    loglevels = [
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        ]
    logformats = [
            "\33[0;37m%-8s\033[1;0m",  # DEBUG
            "\33[1;32m%-8s\033[1;0m",  # INFO
            "\33[1;33m%-8s\033[1;0m",  # WARNING
            "\33[1;31m%-8s\033[1;0m",  # ERROR
            "\33[1;41m%-8s\033[1;0m",  # CRITICAL
        ]
    loggingformats = list(zip(loglevels, logformats))

    # check if the terminal supports colored output
    colors = os.popen("tput colors 2> /dev/null").read()
    if colors and int(colors) < 8 or args.nocolor:
        # do not show colors, either not enough are supported or they are not
        # wanted
        nocolor = True
        for level, _format in loggingformats:
            set_log_level_format(level, "%-8s")
    else:
        nocolor = False
        for level, format in loggingformats:
            set_log_level_format(level, format)

    logging.basicConfig(level=get_logging_level(args))
    log = logging.getLogger(__name__)
    log.info("Executing as main")
    log.debug("Using terminal color output: %r" % (not nocolor))

    log.debug("Args passed: " + str(args))
    main(**vars(args))
