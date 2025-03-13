# live.radio101.hr uses azuracast
# https://www.azuracast.com/docs/developers/now-playing-data/


async def load(session):
    url = "https://live.radio101.hr/api/nowplaying/radio_101"

    response = await session.get(url)
    contents = await response.json()

    artist = contents["now_playing"]["song"]["artist"]
    title = contents["now_playing"]["song"]["title"]

    if artist and title:
        return artist, title

    # TODO: what does the data look like when nothing is playing?
