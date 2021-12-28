from xml.etree import ElementTree

from . import timestamp_ms


async def load(session, name):
    url = "https://np.tritondigital.com/public/nowplaying"

    response = await session.get(url, params={
        'mountName': name,
        'numberToFetch': 10,
        'eventType': 'track',
        'request.preventCache': timestamp_ms(),
    })

    contents = await response.text()
    root = ElementTree.fromstring(contents)

    for item in root.findall('nowplaying-info'):
        artist = item.find("property[@name='track_artist_name']").text
        title = item.find("property[@name='cue_title']").text

        # Returned when no song is playing
        if title.lower() == 'hrvatski radio':
            continue

        return [
            artist.strip().title(),
            title.strip().capitalize()
        ]
