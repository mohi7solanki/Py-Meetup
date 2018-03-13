from calendar import monthrange
from datetime import timedelta


def next_month(date):
    return date + timedelta(days=monthrange(date.year, date.month)[1])
