from aiohttp.client import ClientSession
from radio.utils.normalize import split_artist_title
from radioscraper import shoutcast


async def load(session: ClientSession):
    stream_url = "https://audio.social3.hr/listen/top_radio_256_mp3/stream"
    artist_title = await shoutcast.fetch_stream_title(session, stream_url)
    return split_artist_title(artist_title, normalize_case=True)
