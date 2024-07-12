import json
from aiohttp import ClientSession


async def load(session: ClientSession):
    response = await session.get("https://radio1.hr/getLiveStream.php")
    contents = await response.read()
    decoded = contents.decode("utf-8-sig")  # Strip UTF-8 BOM and decode

    # Empty string sent when nothing is playing
    if decoded:
        data = json.loads(decoded)
        artist = data["rs_artist"]
        title = data["rs_title"]

        if artist == "RADIO 1":
            return None

        if artist and title:
            return artist.title(), title.capitalize()
