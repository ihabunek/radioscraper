from requests import Request
from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


def form_request():
    url = 'http://streaming.antenazagreb.hr/stream/now_playing.php'

    return Request("GET", url, params={
        'the_stream': 'http://live.antenazagreb.hr:8000/;',
        '_': timestamp_ms(),
    })


def parse_response(response):
    return split_artist_title(response.text)
