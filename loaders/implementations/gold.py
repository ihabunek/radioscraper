from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


async def load(session):
    url = 'http://streaming.goldfm.hr/stream/now_playing.php'

    response = await session.get(url, params={
        'the_stream': 'http://live.goldfm.hr:8068/;',
        '_': timestamp_ms(),
    })
    contents = await response.text()

    return split_artist_title(contents, normalize_case=True)
