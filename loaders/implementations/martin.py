from requests import Request

from radio.utils.normalize import split_artist_title


def form_request():
    return Request("GET", 'http://radio-martin.hr/onAir.php')


def parse_response(response):
    return split_artist_title(response.text, normalize_case=True)
