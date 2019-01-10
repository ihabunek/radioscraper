from requests import Request
from xml.etree import ElementTree


def form_request():
    return Request("GET", "http://laganini.fm/logs/zagreb/NowOnAir.xml")


def parse_response(response):
    root = ElementTree.fromstring(response.text)
    song = root.find('.//Song')
    title = song.attrib.get('title').strip()

    artist = song.find('Artist')
    artist_name = artist.get('name').strip()

    if artist_name and title:
        return (
            artist_name.title(),
            title,
        )
