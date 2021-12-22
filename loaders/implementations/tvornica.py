from radio.utils.normalize import split_artist_title
from aiohttp.client import ClientSession


async def load(session: ClientSession):
    response = await session.get("https://radiotvornica.hr/sys/ajax/stream-data.aspx")
    contents = await response.text()
    return split_artist_title(contents, normalize_case=True)
