from aiohttp.client import ClientSession
from radioscraper import shoutcast


SKIP_ARTISTS = [
    "centralne vijesti",
    "coolturnet",
    "financijske vijesti",
    "gost dana",
    "gradske novice",
    "kulturni gost",
    "na krilima demokracije",
    "na meti nacionala",
    "nacional",
    "nacionalov zajutrak",
    "nacionalov zornjak",
    "najava programa",
    "promocija tjednika nacional",
    "radio nacional",
    "radio nacionala",
    "sport i tjelovježba",
    "sport subotom",
    "stanje u prometu",
    "subotnja porcija sporta",
    "tako dobro",
    "vijesti iz europe",
    "vijesti iz kulture",
    "vijesti iz sporta",
    "uj fuj tjedna",
]

SKIP_TITLES = [
    "centralne vijesti",
    "gradske novice",
    "ljeto na nacionalu",
    "na meti nacionala",
    "nacionalov zajutrak",
    "nacionalov zornjak",
    "novice iz grada",
    "poslovne vijesti radio nacionala",
    "prognoza vremena",
    "promocija tjednika nacional",
    "stanje u prometu",
    "vremenska prognoza vremena",
]


async def load(session: ClientSession):
    stream_url = "https://nnc1-bpmmc501.radioca.st/stream"
    result = await shoutcast.load(session, stream_url, normalize_case=True)

    if not result:
        return None

    artist, title = result

    if title.lower().startswith("centralne vijesti"):
        return None

    if "whatsapp" in title.lower():
        return None

    if "vijesti" in artist.lower():
        return None

    if title.lower() in SKIP_TITLES:
        return None

    if artist.lower() in SKIP_ARTISTS:
        return None

    return artist, title
