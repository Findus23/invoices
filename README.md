# Invoices

## Config: config.yaml
The main config is in a file called `config.yaml`:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `default_hourly_rate` | int       | The hourly rate you bill for in this receipt. |
| `default_recipient`   | string    | Filename (before the `.yaml`) of your default recipient. |
| `description`         | string    | Description of the work you did.  |
| `title`               | string    | Title of the invoice. |
| `hours`               | int       | Probably: number of hours worked. Will be asked regardless, for some reason. |
| `invoice_dir`         | string    | Directory in which the invoice will be generated. Needs to exist prior to execution. |
| `last_id`             | int       | Since invoices need to have unique IDs, this number will be increased by one. After that, the config will be written back to the file. This deletes any prior comments. |
| `bank_fee`            | int       | Optional. If there are some bank fees you can invoice.    |

### Example
```config.yaml
default_hourly_rate: 50     # what you expect to get for each hour worked
default_recipient: <rname>  # filename of recipient in `recipients`
description: some description   # description of what you've been working on
hours: 31   # worked hours
invoice_dir: invoice    # directory needs to exist
last_id: 3  # will get updated after generating invoice
```

## Recipients: recipients/\<rname.yaml\>
For every recipient `rname`, have a `recipients/<rname>.yaml` file structured
like this:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `name`        | string    | Your recipients name. |
| `address`     | string    | Your recipients business address. Both street and number. |
| `zip`         | int       | ZIP code of your recipients address.   |
| `city`        | string    | City correlating to the zip code. |
| `country`     | string    | Country of your recipients business address. |
<!--
| `IBAN`        | string    | The IBAN of your bank account.    |
| `BIC`         | string    | The BIC of your bank account. |
| `bank`        | string    | The name of your bank.    |
-->

### Example
```recipients/<rname>.yaml
name: <name>
address: <address>
zip: <zip>
city: <city>
cityShort: O ??
country: Deutschland
IBAN: <IBAN>
BIC: <BIC>
```

## Your own information: from.yaml
Have a file called `from.yaml` with your own information structured like this:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `name`        | string    | Your full name.    |
| `address`     | string    | Your Address. Both street and number. |
| `zip`         | int       | Your area ZIP code.   |
| `city`        | string    | The city you live in. |
| `cityShort    | string    | Shortened version of your city name.  |
| `countryDE`   | strang    | Name of your country in german, used for an invoice in german. |
| `countryEN`   | strang    | Name of your country in english, used for an invoice in english. |
| `IBAN`        | string    | The IBAN of your bank account.    |
| `BIC`         | string    | The BIC of your bank account. |
| `bank`        | string    | The name of your bank.    |

### Example
```from.yaml
name: <name>
address: <address>
zip: <zip>
city: <city>
cityShort: <string>
country: Deutschland
IBAN: <IBAN>
BIC: <BIC>
countryDE: <string>
```

## Structure
```
mkdir invoice
mkdir recipients
```

## Setup
```
virtualenv -p python3 .venv
source .venv/bin/activate
# apparently this is one of the few ways to install poetry?
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
poetry install              # install dependencies
```


## Usage

```
$ python main.py create
...     # you will be asked for details and further information here
$ python main.py compile
```
