from xml.etree import ElementTree

from radioscraper.utils import http

from . import timestamp_ms


def load(name):
    url = "http://np.tritondigital.com/public/nowplaying"

    response = http.get(url, params={
        'mountName': name,
        'numberToFetch': 10,
        'eventType': 'track',
        'request.preventCache': timestamp_ms(),
    })

    root = ElementTree.fromstring(response.text)

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
