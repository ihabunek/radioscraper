from requests import Request
from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


def form_request():
    return Request("GET", 'http://138.201.248.219:8006/stats', params={
        'sid': 1,
        'json': 1,
        '_': timestamp_ms(),
    })


def parse_response(response):
    data = response.json()
    return split_artist_title(data['songtitle'])
