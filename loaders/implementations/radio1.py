import json
from aiohttp import ClientSession


async def load(session: ClientSession):
    response = await session.get("https://radio1.hr/getLiveStream.php")
    contents = await response.read()

    # Strip UTF-8 BOM and decode
    data = json.loads(contents.decode("utf-8-sig"))
    artist = data["rs_artist"]
    title = data["rs_title"]

    if artist == "RADIO 1":
        return None

    return artist.title(), title.capitalize()
