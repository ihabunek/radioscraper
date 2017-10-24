from requests import Request


def form_request(slug):
    url = 'http://www.prvi.hr/modules/mod_radioplayer/tmpl/icecast_fireplay.php'

    return Request("POST", url, data={
        "song_cache_dirname": slug,
    })


def parse_response(response):
    data = response.json()
    return [
        data['artist'],
        data['song'],
    ]
