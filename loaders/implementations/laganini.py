from radio.utils.normalize import split_artist_title
from radioscraper import shoutcast


async def load(session):
    stream_url = "http://194.145.208.251:8000/start/lfmzg"
    if artist_title := await shoutcast.fetch_stream_title(session, stream_url):
        artist_title = artist_title.removeprefix("Now On Air:").strip()
        return split_artist_title(artist_title, normalize_case=True)
