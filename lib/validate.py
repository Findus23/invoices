import logging
log = logging.getLogger(__name__)

def validate(d: dict, name: str, validation_func):
    log.debug("Validating " + name.lower())
    try:
        validation_func(d)
    except KeyError as e:
        log.critical("Field required but missing (in " + name.upper() + " file): " + str(e))
        exit(1)


def validate_client(client: dict):
    """ To validate, simply check if all (later
    required) keys are present. Will throw an
    Exception if not.
    """
    client["name"]
    client["address"]
    client["zip"]
    client["city"]
    # client["country"]


def validate_user(user: dict):
    """ To validate, simply check if all (later
    required) keys are present. Will throw an
    Exception if not.
    """
    validate_client(user)
    user["IBAN"]
    user["BIC"]
    user["bank"]


def validate_details(details: dict):
    """ To validate, simply check if all (later
    required) keys are present. Will throw an
    Exception if not.
    """
    details["hourly_rate_cents"]
    details["client"]
    details["title"]
    details["description"]
    details["hours_worked"]
    details["invoice_id"]
    details["timeframe"]
