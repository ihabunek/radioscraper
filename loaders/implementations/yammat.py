from bs4 import BeautifulSoup


async def load(session):
    response = await session.get("https://www.yammat.fm/wp-json/yammat/v1/json_sidebar_songs")
    data = await response.json()
    html = data["html"]["current_desktop"]
    soup = BeautifulSoup(html, "html.parser")

    # Yes, title and artist are the wrong way around
    [artist] = soup.select(".stream-content__title")
    [title] = soup.select(".stream-content__artist")

    artist = artist.text.strip()
    title = title.text.strip()

    if not artist or not title:
        return None

    return artist, title
