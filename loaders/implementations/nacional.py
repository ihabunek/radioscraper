from aiohttp.client import ClientSession
from loaders.implementations.common import shoutcast


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
    stream_url = "https://nnc1-bpmmc501.radioca.st/stream"
    result = await shoutcast.load(session, stream_url, normalize_case=True)

    if not result:
        return None

    artist, title = result

    if title.lower() in SKIP_TITLES:
        return None

    if artist.lower() in SKIP_ARTISTS:
        return None

    return artist.title(), title.capitalize()
