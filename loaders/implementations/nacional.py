import html


SKIP_ARTISTS = [
    "na meti nacionala",
    "nacional",
    "gradske novice",
]

SKIP_TITLES = [
    "na krilima demokracije",
    "promocija tjednika nacional",
    "stanje u prometu",
    "novice iz grada",
]


async def load(session):
    response = await session.get("https://radio.nacional.hr/current-song")
    records = await response.json(content_type=None)  # ignore invalid header

    _, playing, _ = records[0]

    if not playing or len(playing) != 2:
        return None

    artist, title = playing
    artist = html.unescape(artist)
    title = html.unescape(title)

    if title.lower() in SKIP_TITLES:
        return None

    if artist.lower() in SKIP_ARTISTS:
        return None

    return artist.title(), title.capitalize()
