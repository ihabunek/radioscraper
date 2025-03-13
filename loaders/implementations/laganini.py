from radio.utils.normalize import split_artist_title
from radioscraper import shoutcast


async def load(session):
    stream_url = "http://194.145.208.251:8000/start/lfmzg"
    artist_title = await shoutcast.fetch_stream_title(session, stream_url)

    prefix = "Now On Air:"
    if artist_title.startswith(prefix):
        artist_title = artist_title[len(prefix) :].strip()

    return split_artist_title(artist_title, normalize_case=True)
