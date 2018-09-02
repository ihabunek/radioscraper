import re

from requests import Request
from radio.utils.normalize import split_artist_title


stream = True


def form_request():
    url = "http://genf196.server4you.de:8585/"
    headers = {"Icy-MetaData": "1"}

    return Request("GET", url, headers=headers)


def parse_response(response):
    # Find chunk size, metadata is included after each chunk
    length = int(response.headers.get('icy-metaint'))

    # Skip first chunk
    response.raw.read(length)

    # Determine length of meta data from first byte
    meta_length = response.raw.read(1)[0] * 16

    # Read and decode metadata
    meta = response.raw.read(meta_length).decode("utf-8")

    match = re.search("StreamTitle='(.+)';", meta)
    if not match:
        raise ValueError("Meta data not found")

    artist, title = split_artist_title(match.group(1))

    # Skip commercials
    if artist == 'Radio Martin':
        return None

    return artist.title(), title
