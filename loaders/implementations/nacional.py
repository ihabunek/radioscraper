import html
from aiohttp import ClientSession


SKIP_ARTISTS = [
    "kulturni gost",
    "na meti nacionala",
    "nacional",
    "gradske novice",
    "najava programa",
    "gost dana",
    "sport i tjelovježba",
    "nacionalov zajutrak",
    "nacionalov zornjak",
    "coolturnet",
    "sport subotom",
]

SKIP_TITLES = [
    "na krilima demokracije",
    "promocija tjednika nacional",
    "stanje u prometu",
    "novice iz grada",
    "ljeto na nacionalu",
    "vremenska prognoza vremena",
    "centralne vijesti",
    "poslovne vijesti radio nacionala",
]


async def load(session: ClientSession):
    url = "https://player.nacional.hr/api/playlist/current_entry"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"}
    response = await session.get(url, headers=headers)
    response.raise_for_status()

    data = await response.json()

    artist = data["artist"]
    title = data["song"]

    artist = html.unescape(artist)
    title = html.unescape(title)

    if title.lower() in SKIP_TITLES:
        return None

    if artist.lower() in SKIP_ARTISTS:
        return None

    return artist.title(), title.capitalize()
