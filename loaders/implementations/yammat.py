import bs4
from radioscraper.utils import http

ADMIN_URL = "https://yammat.fm/wp-admin/admin-ajax.php"


def load():
    response = http.get(ADMIN_URL, params={"action": "get_nonce"})
    nonce = response.json()["afp_nonce"]

    response = http.post(ADMIN_URL, data={
        "action": "ajax_update_sidebar_songs",
        "afp_nonce": nonce
    })

    data = response.json()
    playing = data["html"]["current_desktop"]

    soup = bs4.BeautifulSoup(playing, 'html.parser')
    spans = [span.text.strip() for span in soup.find_all('span')]

    if len(spans) != 2:
        raise Exception("Can't find artist and title from: {}".format(spans))

    artist, title = spans

    if not artist or not title:
        return None

    return spans
