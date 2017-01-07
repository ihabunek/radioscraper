import requests

from bs4 import BeautifulSoup
from datetime import datetime


def get_current_song(slug):
    if slug == 'antena':
        return _prvi('antena')

    if slug == 'gold':
        return _prvi('gold')

    if slug == 'radio101':
        return _radio101()

    if slug == 'otvoreni':
        return _otvoreni()

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


def _otvoreni():
    url = "http://www.otvoreni.hr/player/"
    html = requests.get(url).text

    bs = BeautifulSoup(html, "html.parser")
    artist = bs.find(id="song-artist")
    song = bs.find(id="song-track")

    return [
        artist.text.title(),
        song.text.capitalize()
    ]
