from loaders.implementations.common import hrt


def form_request():
    return hrt.form_request('SLJEME')


def parse_response(response):
    return hrt.parse_response(response)