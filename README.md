# Invoices
To generate invoices, you need multiple local configs. Your own information
should be present in `from.yaml`, the person (or company) you write the invoice
to should be present as a file in `recipients/<rname>.yaml`, where `rname` is
the selector. The specific information about this invoice should be in
`config.yaml`.

## Your own information: from.yaml
Have a file called `from.yaml` with your own information structured like this:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `name`        | string    | Your full name.    |
| `address`     | string    | Your Address. Both street and number. |
| `zip`         | int       | Your area ZIP code.   |
| `city`        | string    | The city you live in. |
| `cityShort`   | string    | Shortened version of your city name.  |
| `countryDE`   | strang    | Name of your country in German, used for an invoice in German. |
| `countryEN`   | strang    | Name of your country in English, used for an invoice in English. |
| `IBAN`        | string    | The IBAN of your bank account.    |
| `BIC`         | string    | The BIC of your bank account. |
| `bank`        | string    | The name of your bank.    |
| `phone`       | string    | Optional. Your phone number. |
| `email`       | string    | Optional. Your mail address. |
| `url`         | string    | Optional. Your homepage.  |

### Example
```from.yaml
name: <name>
address: <address>
zip: <zip>
city: <name of city>
cityShort: <short name of city>
countryDE: Deutschland
countryEN: Germany
IBAN: <IBAN>
BIC: <BIC>
bank: <name of bank>
```

It's no big deal to leave some of the fields empty.

## Clients: recipients/\<rname\>.yaml
For every clients `rname`, have a `recipients/<rname>.yaml` file structured
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
```recipients/<rname>.yaml
name: <name>
address: <address>
zip: <zip>
city: <city>
country: <country>
```


## Config: config.yaml
The main config is in a file called `config.yaml`:

### Field descriptions
| Field | Type | description |
|:---|:---:|:---|
| `title`               | string    | Title of the invoice. |
| `description`         | string    | Description of the work you did.  |
| `range`               | string    | Timeframe during which you accumulated the given number of hours. |
| `hours`               | int       | Number of hours you worked for the given timeframe and client. |
| `default_recipient`   | string    | Filename (before the `.yaml`) of your default client. |
| `last_id`             | int       | Since invoices need to have unique IDs, this number will be increased by one. After that, the config will be written back to the file. This deletes any prior comments. |
| `invoice_dir`         | string    | Directory in which the invoice will be generated. Needs to exist prior to execution. |
| `default_hourly_rate` | int       | The hourly rate you bill for in this receipt. |
| `bank_fee`            | int       | Optional. Amount of bank fees you can invoice.    |

### Example
```config.yaml
title: <invoice title>
description: <work description>
range: <timeframe in which you worked>
hours: <hours worked>
default_recipient: <rname>
last_id: <int>
invoice_dir: invoice    # directory needs to exist
default_hourly_rate: <int>
```

## Structure
The directory structure of where you execute this script should look something
like this:
```
$ tree
.
├── invoice     # content is generated, but folder needs to exist
│   ├── <id>
│   └── <id>
├── recipients
│   ├── <rname>.yaml
│   └── <rname>.yaml
├── from.yaml
└── config.yaml
```

## Setup
Make sure to install poetry first.

### Nix
`nix-env -iA nixpkgs.poetry`

### Other
According to [their website](https://python-poetry.org/docs/#installation),
this is the recommended way of installation:
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`

### Install dependencies
Make sure to switch to a virtual environment prior to installing dependencies.
```
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ poetry install              # install dependencies
```


## Usage

```
$ python main.py create
...     # you will be asked for details and further information interactively
$ python main.py compile
```
