from radio.utils.normalize import split_artist_title


async def load(session):
    response = await session.get("http://radio.unios.hr:8000/status-json.xsl")
    data = await response.json()
    # Using [2] because that's what they do on the web site
    source = data["icestats"]["source"][2]["title"]
    return split_artist_title(source)
