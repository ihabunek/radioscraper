from radio.utils.normalize import split_artist_title
from radioscraper import shoutcast


async def load(session):
    # At time of writing, the stream works but does not contain metadata
    # Also this endpoint is used on web but returns no data:
    #   http://laganini.fm/logs/zagreb/NowOnAir.xml
    stream_url = "http://c8.hostingcentar.com:10043/start/lfmzg"
    if artist_title := await shoutcast.fetch_stream_title(session, stream_url):
        artist_title = artist_title.removeprefix("Now On Air:").strip()
        return split_artist_title(artist_title, normalize_case=True)
