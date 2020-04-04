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
        timestamp, title, artist = [i.text for i in item.findall('property')]

        if title != 'HRVATSKI RADIO':  # returned when no song is playing
            return [
                artist.strip().title(),
                title.strip().capitalize()
            ]
