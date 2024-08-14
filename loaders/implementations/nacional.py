import html


async def load(session):
    response = await session.get("https://radio.nacional.hr/current-song")
    records = await response.json(content_type=None)  # ignore invalid header

    _, (artist, title), _ = records[0]
    artist = html.unescape(artist)
    title = html.unescape(title)

    return artist.title(), title.capitalize()
