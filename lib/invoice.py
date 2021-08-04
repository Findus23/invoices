from datetime import datetime


class Invoice(object):
    def __init__(
        self,
        id: int = None,
        locale: int = None,
        title: str = None,
        recipient: object = None,
        date: datetime = None,
        description: str = None,
        range: str = None,
        bank_fee: int = None,
    ):
        self.id = id
        self.locale = locale
        self.title = title
        self.recipient = recipient
        self.date = date
        self.description = description
        self.range = range
        self.locale = locale


class SingleInvoice(Invoice):
    def __init__(self, price: int = None, **kwargs):
        super(SingleInvoice, self).__init__(**kwargs)
        self.mode = "single"
        self.price = price


class HourlyInvoice(Invoice):
    def __init__(self, details, **kwargs):
        super(HourlyInvoice, self).__init__(**kwargs)
        self.mode = "hourly"
        self.hours = details["hours"]
        self.per_hour = per_hour

        if "minutes" in details:
            self.minutes = details["minutes"]
        else:
            self.minutes = 0

    def hourtotal(self):
        return self.per_hour * (self.hours + self.minutes / 60)

    def total(self):
        return self.hourtotal()
