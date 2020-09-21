# Invoices

## Config

```config.yaml
default_hourly_rate: 50     # what you expect to get for each hour worked
default_recipient: <rname>  # filename of recipient in `recipients`
description: some description   # not sure where it shows up
hours: 31   # worked hours
invoice_dir: invoice    # directory needs to exist
last_id: 3  # will get updated after generating invoice
```

## Recipients
```recipients/<rname>.yaml
recipient: ?? line required?
  name: <name>
  address: <address>
  zip: <zip>
  city: <city>
  cityShort: O ??
  country: Deutschland
  IBAN: <IBAN>
  BIC: <BIC>
```

## From
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
