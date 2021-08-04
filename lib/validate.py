import logging

log = logging.getLogger(__name__)


def validate(d: dict, name: str, validation_func):
    """Validate the given dictionary with its validation function."""
    log.debug("Validating " + name.lower())
    try:
        validation_func(d)
    except KeyError as e:
        log.critical(
            "Field required but missing (in " + name.upper() + " file): " + str(e)
        )
        exit(1)
    except ValueError as e:
        log.critical("Wrong Type (in " + name.upper() + " file): " + str(e))
        exit(1)


def validate_client(client: dict):
    """To validate, simply check if all (later
    required) keys are present. Will throw an
    Exception if not.
    """
    str(client["name"])
    str(client["address"])
    int(client["zip"])
    str(client["city"])
    # client["country"]


def validate_user(user: dict):
    """To validate, simply check if all (later
    required) keys are present. Will throw an
    Exception if not.
    """
    validate_client(user)
    str(user["IBAN"])
    str(user["BIC"])
    str(user["bank"])


def validate_details(details: dict):
    """To validate, simply check if all (later
    required) keys are present. Will throw an
    Exception if not.
    """
    details["client"]
    str(details["title"])
    int(details["invoice_id"])
    str(details["timeframe"])  # not just one value
    # 'hours_worked' or 'amount'
    # 'hourly_rate_cents' or 'item_price_cents'
    if details.get("items"):
        validate_items(details["items"])
    else:
        str(details["description"])
        int(validate_either(details, "amount", "hours_worked"))
        int(validate_either(details, "item_price_cents", "hourly_rate_cents"))


def validate_items(items: dict):
    for item in items:
        str(item["description"])
        int(item["amount"])
        int(item["item_price_cents"])


def validate_either(d: dict, k1, k2):
    if d.get(k1):
        return d[k1]
    return d[k2]
