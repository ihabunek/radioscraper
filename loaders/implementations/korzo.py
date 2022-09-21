from xml.etree import ElementTree


async def load(session):
    response = await session.get("https://web.radiokorzo.hr/stream-info/si.xml")

    contents = await response.text()
    root = ElementTree.fromstring(contents)

    # The currently playing song has an Expire child element
    for song in root.findall("Song"):
        if song.find("Expire") is not None:
            title = song.attrib["title"]
            artist_node = song.find("Artist")
            if artist_node:
                artist = artist_node.attrib["name"]
                return [artist, title]
