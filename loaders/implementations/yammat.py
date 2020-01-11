import bs4
import requests


# TODO: Make parsing multiple requests more robust, this is not optimal
def get_nonce():
    response = requests.get("https://yammat.fm/wp-admin/admin-ajax.php?action=get_nonce")
    response.raise_for_status()
    return response.json()["afp_nonce"]


def form_request():
    return requests.Request("POST", "https://yammat.fm/wp-admin/admin-ajax.php", data={
        "action": "ajax_update_sidebar_songs",
        "afp_nonce": get_nonce(),
    })


def parse_response(response):
    data = response.json()
    playing = data["html"]["current_desktop"]

    soup = bs4.BeautifulSoup(playing, 'html.parser')
    spans = [span.text.strip() for span in soup.find_all('span')]

    if len(spans) != 2:
        raise Exception("Can't find artist and title from: {}".format(spans))

    artist, title = spans

    if artist == "" or title == "":
        return None

    return spans
