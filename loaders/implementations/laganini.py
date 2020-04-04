from radioscraper.utils import http

from xml.etree import ElementTree


def load():
    response = http.get("http://laganini.fm/logs/zagreb/NowOnAir.xml")

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
