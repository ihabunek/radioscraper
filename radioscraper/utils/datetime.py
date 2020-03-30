from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware


def day_start(date):
    """Returns an aware datetime at the beginning of the given day."""
    return make_aware(datetime(date.year, date.month, date.day))


def day_end(date):
    """Returns an aware datetime at the end of the given day."""
    return day_start(date) + relativedelta(days=1)


def month_start(year, month):
    """Returns an aware datetime at the beginning of the given month."""
    return make_aware(datetime(year, month, 1))


def month_end(year, month):
    """Returns an aware datetime at the end of the given month."""
    return month_start(year, month) + relativedelta(months=1)
