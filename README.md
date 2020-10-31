# Creating Invoices
To generate invoices, you need multiple local configs. Your own information
should be present in `self.yaml`, the person (or company) you write the invoice
to should be present as a file in `clients/<cname>.yaml`, where `cname` is
the selector. Information specific to this invoice should be in `details.yaml`.

## Setup
First, you need to [install
poetry](https://python-poetry.org/docs/#installation). If you have `nix` it is
as simple as `nix-env -iA nixpkgs.poetry`. After that, create a virtual
environment and install all dependencies.

```
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ poetry install                # install dependencies
```


## Usage
When you have created all config files, creating an invoice is as simple as:

```
$ python main.py
```

There are a few more options available though:
```
usage: main.py [-h] [--locale LOCALE] [--user USER] [--clients CLIENTS]
               [--validate] [-v] [-y] [--nocolor] [--date DATE]
               [DETAILS]

script to help create invoices based on given information, should be easy to
use. By default, will print and ask for confirmation on details before
creating the invoice. This behavior can be deactivated with `-y|--yes`.

positional arguments:
  DETAILS            file with details and content specific to this invoice
                     (default: details.yml)

optional arguments:
  -h, --help         show this help message and exit
  --locale LOCALE    what language the invoice should be in (default: de)
  --user USER        your contact details and bank information. (default:
                     self.yml)
  --clients CLIENTS  relative path (folder) in which information about your
                     clients is stored in `<cname>.yml` files. (default:
                     clients/)
  --validate         only validate available information and check available
                     functionality, do not actually create invoice (default:
                     False)
  -v, --verbose      make logging output (more) verbose. Default (or 0) is
                     ERROR, -v is WARN, -vv is INFO and -vvv is DEBUG. Can be
                     passed multiple times. (default: 0)
  -y, --yes          do not ask for confirmation before creating the actual
                     invoice (default: False)
  --nocolor          deactivate colored log output (default: False)
  --date DATE        date formatting string the invoice should be dated at.
                     Can be a specific day like '2020-09-01'. Defaults to
                     today. (default: %Y-%m-%d)
```

# Config Files
## Your own information: self.yaml
Have a file called `self.yaml` with your own information structured like this:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `name`        | string    | Your full name.    |
| `address`     | string    | Your Address. Both street and number. |
| `zip`         | int       | Your area ZIP code.   |
| `city`        | string    | The city you live in. |
| `IBAN`        | string    | The IBAN of your bank account.    |
| `BIC`         | string    | The BIC of your bank account. |
| `bank`        | string    | The name of your bank.    |
| `phone`       | string    | Optional. Your Phone number. |
| `email`       | string    | Optional. Your Email address. |
| `url`         | string    | Optional. Link to your webpage. |

### Example
```self.yml
name: <name>
address: <address>
zip: <zip>
city: <name of city>
country: <country>
IBAN: <IBAN>
BIC: <BIC>
bank: <name of bank>
```

## Clients: clients/\<cname\>.yaml
For every clients `cname`, have a `clients/<cname>.yaml` file structured
like this:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `name`        | string    | Your clients name. |
| `address`     | string    | Your clients business address. Both street and number. |
| `zip`         | int       | ZIP code of your clients address.   |
| `city`        | string    | City correlating to the zip code. |
| `country`     | string    | Country of your clients business address. |

### Example
```clients/<cname>.yaml
name: <name>
address: <address>
zip: <zip>
city: <city>
country: <country>
```


## Config: details.yaml
Specific information is in a file called `details.yaml`:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `title`               | string    | Title of the invoice. |
| `description`         | string    | Description of the work you did.  |
| `timeframe`           | string    | Timeframe during which you accumulated the given number of hours. |
| `hours_worked`        | int       | Number of hours you worked for the given timeframe and client. |
| `client`              | string    | File-Selector (`cname`, before the `.yaml` from your `clients` folder) of your client for this project. |
| `invoice_id`          | int       | Unique ID of this invoice. You need to ensure that this id is unique. |
| `default_hourly_rate` | int       | The hourly rate you bill for in this invoice, in cents per hour. |
| `locale`              | string    | Optional, `de` or `en`. Ignoring `--locale` if set. Default: `de` |
<!--
| `bank_fee`            | int       | Optional. Amount of bank fees you can invoice.    |
-->

### Example
```details.yaml
title: <invoice title>
description: <work description>
timeframe: <timeframe in which you worked>
hours_worked: <hours worked>
client: <rname>
invoice_id: <int>
hourly_rate: <int>
mwst_percent: 19
```

