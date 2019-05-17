from requests import Request
from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


def form_request():
    url = "https://zet.pluginsandthemes.ro/http://live.radio101.hr:9531/stats"
    headers = {"Origin": "http://radio101.hr"}
    return Request("GET", url, headers=headers, params={
        'sid': 1,
        'json': 1,
        '_': timestamp_ms(),
    })


def parse_response(response):
    data = response.json()
    return split_artist_title(data['songtitle'])
