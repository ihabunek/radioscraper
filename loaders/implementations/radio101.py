from radio.utils.normalize import split_artist_title
from radioscraper.utils import http

from .common import timestamp_ms


def load():
    url = "http://live.radio101.hr:9531/stats"
    headers = {"Origin": "http://radio101.hr"}
    response = http.get(url, headers=headers, params={
        'sid': 1,
        'json': 1,
        '_': timestamp_ms(),
    })

    songtitle = response.json()['songtitle']

    return split_artist_title(songtitle)
