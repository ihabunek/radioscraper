from requests import Request

from radio.utils.normalize import split_artist_title


def form_request():
    url = 'http://www.radiostudent.hr/wp-admin/admin-ajax.php?action=rsplaylist_api'
    return Request("GET", url)


def parse_response(response):
    data = response.json()
    artist_title = data['rows'][0]['played_song']

    return split_artist_title(artist_title)
