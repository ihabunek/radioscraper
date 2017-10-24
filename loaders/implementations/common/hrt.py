from datetime import datetime
from requests import Request
from xml.etree import ElementTree


def _timestamp():
    return int(datetime.now().timestamp() * 1000)


def form_request(name):
    url = "http://np.tritondigital.com/public/nowplaying"

    return Request("GET", url, params={
        'mountName': name,
        'numberToFetch': 10,
        'eventType': 'track,',
        'request.preventCache': _timestamp(),
    })


def parse_response(response):
    root = ElementTree.fromstring(response.text)

    for item in root.findall('nowplaying-info'):
        timestamp, title, artist = [i.text for i in item.findall('property')]

        if title != 'HRVATSKI RADIO':  # returned when no song is playing
            return [
                artist.strip().title(),
                title.strip().capitalize()
            ]
