from datetime import datetime
from requests import Request

from radio.utils.normalize import split_artist_title


def form_request():
    return Request("GET", 'http://192.240.102.133:12430/played', params={
        'sid': 1,
        'type': 'json',
        '_': datetime.now().timestamp(),
    })


def parse_response(response):
    data = response.json()
    artist_title = data[0]['title']

    return split_artist_title(artist_title)
