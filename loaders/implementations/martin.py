import re

from radio.utils.normalize import split_artist_title


async def load(session):
    url = "http://genf196.server4you.de:8585/"
    headers = {"Icy-MetaData": "1"}

    async with session.get(url, headers=headers) as response:
        # Find chunk size, metadata is included after each chunk
        offset = int(response.headers.get('icy-metaint'))

        # Check sane offset value (usually 16k)
        if not (1 < offset < 64 * 1024):
            raise Exception(f"invalid icy-metaint value: {offset}")

        # Skip first chunk
        await response.content.readexactly(offset)

        # Determine length of meta data from first byte
        b = await response.content.readexactly(1)
        length = b[0] * 16

        # Check sane length value (usually 32)
        if not (1 < length < 128):
            raise Exception(f"invalid meta length: {length}")

        # Read and decode metadata
        meta = await response.content.readexactly(length)

    meta = meta.decode("utf-8")
    match = re.search("StreamTitle='(.+)';", meta)
    if not match:
        raise Exception(f"metadata not found in: {meta}")

    parts = split_artist_title(match.group(1))
    if parts is None:
        return None

    artist, title = parts

    # Skip commercials
    if artist.lower() == 'zabavni radio' and title.lower() == 'reklame':
        return None

    return artist.title(), title
