import requests

from bs4 import BeautifulSoup
from datetime import datetime
from xml.etree import ElementTree


def get_current_song(slug):
    """Returns the currently playing [artist, song] for the given radio.

    Returns None if no song is playing (e.g. talk shows).
    Raises an exception if fetching fails. """

    if slug == 'antena':
        return _prvi('antena')

    if slug == 'gold':
        return _prvi('gold')

    if slug == 'radio101':
        return _radio101()

    if slug == 'otvoreni':
        return _otvoreni()

    if slug == 'student':
        return _student()

    if slug == 'yammat':
        return _yammat()

    if slug == 'martin':
        return _martin()

    if slug == 'hrt2':
        return _hrt2()

    raise ValueError("Unknown radio '{}'".format(slug))


def _timestamp():
    return int(datetime.now().timestamp() * 1000)


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
    params = {
        "request.preventCache": _timestamp
    }

    response = requests.get(url, params)
    data = response.json()

    author, title = [
        data[0]['author'],
        data[0]['title'],
    ]

    if author and title:
        return [author, title]


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


def _student():
    url = 'http://www.radiostudent.hr/wp-admin/admin-ajax.php?action=rsplaylist_api'
    data = requests.get(url).json()

    bits = data['rows'][0]['played_song'].split('-', 1)

    # Some radio shows are in the feed, which are not songs
    if len(bits) != 2:
        return None

    artist, title = bits

    return [
        artist.strip().title(),
        title.strip().capitalize()
    ]


def _yammat():
    url = 'http://192.240.102.133:12430/played'
    params = {
        'sid': 1,
        'type': 'json',
        '_': datetime.now().timestamp(),
    }

    data = requests.get(url, params).json()
    bits = data[0]['title'].split('-', 1)

    # Some radio shows are in the feed, which are not songs
    if len(bits) != 2:
        return None

    return [x.strip() for x in bits]


def _martin():
    url = 'http://radio-martin.hr/onAir.php'
    bits = requests.get(url).text.split('-', 1)

    if len(bits) != 2:
        return None

    artist, title = bits

    return [
        artist.strip().title(),
        title.strip().capitalize()
    ]


def _hrt2():
    url = 'http://np.tritondigital.com/public/nowplaying'
    params = {
        'mountName': 'PROGRAM2',
        'numberToFetch': 10,
        'eventType': 'track,',
        'request.preventCache': _timestamp(),
    }

    data = requests.get(url, params).text
    root = ElementTree.fromstring(data)

    for item in root.findall('nowplaying-info'):
        timestamp, title, artist = [i.text for i in item.findall('property')]

        if title != 'HRVATSKI RADIO':  # returned when no song is playing
            return [
                artist.strip().title(),
                title.strip().capitalize()
            ]
