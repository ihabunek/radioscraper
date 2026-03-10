import re

from radio.utils.normalize import split_artist_title


async def load(session):
    response = await session.get("https://808proxy.contrib.hr/7.html")
    contents = await response.text()

    match = re.search(r"<html><body>\d+,\d+,\d+,\d+,\d+,\d+,(.+)</body></html>", contents)
    if match:
        return split_artist_title(match.group(1))

    return None
