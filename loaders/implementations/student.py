from radio.utils.normalize import split_artist_title
from radioscraper.utils import http


def load():
    url = 'http://www.radiostudent.hr/wp-admin/admin-ajax.php'
    response = http.get(url, params={"action": "rsplaylist_api"})

    data = response.json()
    artist_title = data['rows'][0]['played_song']

    return split_artist_title(artist_title)
