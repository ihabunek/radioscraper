from radio.utils.normalize import split_artist_title


async def load(session):
    response = await session.get('http://c5.hostingcentar.com:8059/currentsong')
    contents = await response.text()

    return split_artist_title(contents, normalize_case=True)
