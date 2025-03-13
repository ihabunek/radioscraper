from aiohttp.client import ClientSession
from radioscraper import shoutcast


async def load(session: ClientSession):
    stream_url = "https://audio.social3.hr/listen/top_radio_256_mp3/stream"
    return await shoutcast.load(session, stream_url, normalize_case=True)
