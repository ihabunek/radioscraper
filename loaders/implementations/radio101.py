from datetime import datetime
from requests import Request

from radio.utils.normalize import split_artist_title


def _timestamp():
    return int(datetime.now().timestamp() * 1000)


def form_request():
    return Request("GET", 'http://138.201.248.219:8006/stats', params={
        'sid': 1,
        'json': 1,
        '_': _timestamp(),
    })


def parse_response(response):
    data = response.json()
    return split_artist_title(data['songtitle'])
