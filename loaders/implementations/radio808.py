import re
import logging

from radio.utils.normalize import split_artist_title

logger = logging.getLogger(__name__)

async def load(session):
    url = 'https://808proxy.contrib.hr/7'

    response = await session.get(url)
    contents = await response.text()

    match = re.search(r"<html><body>\d+,\d+,\d+,\d+,\d+,\d+,(.+)</body></html>", contents)
    if match:
        return split_artist_title(match.group(1))

    logger.error("Failed parsing file", extra=dict(contents=contents))
    return None
