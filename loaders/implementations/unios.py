from radio.utils.normalize import split_artist_title
from .common import timestamp_ms


async def load(session):
    url = "http://radio.unios.hr:8000/status-json.xsl"
    response = await session.get(url, params={
        '_': timestamp_ms()
    })

    data = await response.json()
    # Using [2] because that's what they do on the web site
    artist_song = data["icestats"]["source"][2]["title"]

    if "OFF AIR" in artist_song or "Radio UNIOS" in artist_song:
        return None

    return split_artist_title(artist_song)
