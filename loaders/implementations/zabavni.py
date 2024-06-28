from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


async def load(session):
    url = "https://stream.zabavni.hr/now_playing.php"
    params = {
        "the_stream": "https://genf196.server4you.de:8585;",
        "_": timestamp_ms(),
    }

    response = await session.get(url, params=params)
    contents = await response.text()

    # Handle error returned in HTTP 200 response
    if contents == "The song title is not available":
        return None

    result = split_artist_title(contents)

    if not result:
        return None

    artist, title = result

    # Skip commercials
    if title == "Reklame" and artist.title() == "Zabavni Radio":
        return None

    return artist.title(), title
