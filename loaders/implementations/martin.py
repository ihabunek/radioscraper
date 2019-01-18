import re
import logging

from requests import Request
from radio.utils.normalize import split_artist_title

logger = logging.getLogger(__name__)


stream = True


def form_request():
    url = "http://genf196.server4you.de:8585/"
    headers = {"Icy-MetaData": "1"}

    return Request("GET", url, headers=headers)


def parse_response(response):
    # Find chunk size, metadata is included after each chunk
    offset = int(response.headers.get('icy-metaint'))

    # Check sane offset value (usually 16k)
    logger.info("icy-metaint: {}".format(offset))
    if not (1 < offset < 64 * 1024):
        logger.error("invalid icy-metaint value: {}")
        return

    # Skip first chunk
    response.raw.read(offset)

    # Determine length of meta data from first byte
    length = response.raw.read(1)[0] * 16

    # Check sane length value (usually 32)
    logger.info("meta length: {}".format(length))
    if not (1 < length < 128):
        logger.error("invalid meta length: {}".format(length))
        return

    # Read and decode metadata
    meta = response.raw.read(length).decode("utf-8")
    match = re.search("StreamTitle='(.+)';", meta)
    if not match:
        raise ValueError("Meta data not found")

    artist, title = split_artist_title(match.group(1))

    # Skip commercials
    if artist == 'Radio Martin':
        return None

    return artist.title(), title
