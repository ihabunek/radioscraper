from xml.etree import ElementTree


# This hasn't given any info in a while
# TODO: check out the shoutcast server at
# http://194.145.208.251:8000/played.html?sid=1

async def load(session):
    response = await session.get("http://laganini.fm/logs/zagreb/NowOnAir.xml")
    contents = await response.text()

    root = ElementTree.fromstring(contents)
    song = root.find('.//Song')
    title = song.attrib.get('title').strip()

    artist = song.find('Artist')
    artist_name = artist.get('name').strip()

    if artist_name and title:
        return (
            artist_name.title(),
            title,
        )
