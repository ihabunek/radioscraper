from radio.utils.normalize import split_artist_title

from .common import timestamp_ms


async def load(session):
    url = "https://stream.zabavni.hr/now_playing.php"
    params = {
        "the_stream": "https://test1.secure.com.hr:8585/;",
        "_": timestamp_ms()
    }

    response = await session.get(url, params=params)
    contents = await response.text()

    artist, title = split_artist_title(contents)

    # Skip commercials
    if title == 'Reklame' and artist.title() == 'Zabavni Radio':
        return None
        
    return artist.title(), title
