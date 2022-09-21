import bs4

ADMIN_URL = "https://www.yammat.fm/wp-admin/admin-ajax.php"


async def load(session):
    response = await session.get(ADMIN_URL, params={"action": "get_nonce"})
    response.raise_for_status()
    data = await response.json()

    response = await session.post(ADMIN_URL, data={
        "action": "ajax_update_sidebar_songs",
        "afp_nonce": data["afp_nonce"]
    })
    response.raise_for_status()
    data = await response.json()

    playing = data["html"]["current_desktop"]
    soup = bs4.BeautifulSoup(playing, 'html.parser')
    spans = [span.text.strip() for span in soup.find_all('span')]

    if len(spans) != 2:
        raise Exception("Can't find artist and title from: {}".format(spans))

    artist, title = spans

    if not artist or not title:
        return None

    # Skip commercials
    if artist.startswith("SHOP") or artist.startswith("SHCL"):
        return None

    # Skip whatever this is
    if artist == "NO" and title == "UPDATE":
        return None

    return artist, title
