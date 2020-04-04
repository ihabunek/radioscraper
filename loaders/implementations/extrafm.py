from radioscraper.utils import http
from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


def load():
    url = 'http://streaming.extrafm.hr/stream/now_playing.php'

    response = http.get(url, params={
        'the_stream': 'http://streams.extrafm.hr:8110/;',
        '_': timestamp_ms(),
    })

    return split_artist_title(response.text)
