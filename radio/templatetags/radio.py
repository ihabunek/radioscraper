from django import template
from http import HTTPStatus

register = template.Library()


@register.filter()
def http_status(code):
    """For a given status code, renders it with the reason phrase"""
    for status in HTTPStatus:
        if code == status:
            return "{} {}".format(status, status.phrase)

    return "{} {}".format(code, "UNKNOWN")
