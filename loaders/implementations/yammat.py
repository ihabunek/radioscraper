import random

from loaders.implementations.common import timestamp_ms


async def load(session):
    response = await session.get(
        "https://stream.yammat.fm/api/nowplaying/1",
        params={
            "_": timestamp_ms(),
            "rand": random.randint(1, 999),
        },
    )
    data = await response.json()
    artist = data["now_playing"]["song"]["artist"]
    title = data["now_playing"]["song"]["title"]

    if artist and title:
        return artist, title
