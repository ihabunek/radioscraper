from radio.utils.normalize import split_artist_title


async def load(session):
    url = "https://www.radiocentar.hr:8585/currentsong?sid=1"

    response = await session.get(url, params={"sid": "1"})
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
