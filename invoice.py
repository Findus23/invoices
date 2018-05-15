from datetime import datetime


class Invoice(object):

    def __init__(self, id: int = None, locale: int = None, title: str = None, recipient: object = None,
                 date: datetime = None, description: str = None, range: str = None, bank_fee: int = None):
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

    def __init__(self, hours: int = None, minutes: int = None, per_hour: int = None, **kwargs):
        super(HourlyInvoice, self).__init__(**kwargs)
        self.mode = "hourly"
        self.hours = hours
        self.minutes = minutes
        self.per_hour = per_hour

    def hourtotal(self):
        return self.per_hour * (self.hours + self.minutes / 60)

    def total(self):
        return self.hourtotal()
