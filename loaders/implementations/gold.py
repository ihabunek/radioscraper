from requests import Request
from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


def form_request():
    url = 'http://streaming.goldfm.hr/stream/now_playing.php'

    return Request("GET", url, params={
        'the_stream': 'http://live.goldfm.hr:8068/;',
        '_': timestamp_ms(),
    })


def parse_response(response):
    return split_artist_title(response.text)
