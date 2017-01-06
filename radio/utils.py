import requests

from datetime import datetime


def get_current_song(slug):
    if slug == 'antena':
        return _prvi('antena')

    if slug == 'gold':
        return _prvi('gold')

    if slug == 'radio101':
        return _radio101()

    raise ValueError("Unknown radio '{}'".format(slug))


def _prvi(slug):
    url = 'http://www.prvi.hr/modules/mod_radioplayer/tmpl/icecast_fireplay.php'
    data = {"song_cache_dirname": slug}

    response = requests.post(url, data=data)
    data = response.json()

    return [
        data['artist'],
        data['song'],
    ]


def _radio101():
    url = 'http://www.radio101.hr/generated/radio_playlist.json'
    params = {"request.preventCache": datetime.now().timestamp()}

    response = requests.get(url, params)
    data = response.json()

    return [
        data[0]['author'],
        data[0]['title'],
    ]
