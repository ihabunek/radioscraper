from loaders.implementations.common import prvi


def form_request():
    return prvi.form_request('gold')


def parse_response(response):
    return prvi.parse_response(response)
