import json

from radio.utils.normalize import split_artist_title
from .common import timestamp_ms

async def load(session):
    url = "http://radio.unios.hr:8000/json.xsl"
    response = await session.get(url, params={
        '_': timestamp_ms()
    })
    jsonp_data = await response.text()

    data = json.loads(jsonp_data.split("(", 1)[1].strip(");"))

    artist_song = data["/fm.mp3"]["title"]

    if "OFF AIR" in artist_song or "Radio UNIOS" in artist_song:
        return None

    return split_artist_title(artist_song)
