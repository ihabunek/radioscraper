from radio.utils.normalize import split_artist_title

async def load(session):
    url = 'https://stream.enterzagreb.hr/player/info/listen_enter_mp3_256_.txt'
    response = await session.get(url)
    contents = await response.text()

    if contents == "Live Broadcast":
        return None

    return split_artist_title(contents, normalize_case=True)
