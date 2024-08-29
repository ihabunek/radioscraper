from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


async def load(session):
    url = "https://live.radio101.hr:8000/stats"
    params = {'sid': 1, 'json': 1, '_': timestamp_ms()}

    response = await session.get(url, params=params)
    contents = await response.json()

    return split_artist_title(contents['songtitle'])
