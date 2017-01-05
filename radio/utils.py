import requests


def get_current_song(radio_slug):
    url = 'http://www.prvi.hr/modules/mod_radioplayer/tmpl/icecast_fireplay.php'
    data = {"song_cache_dirname": radio_slug}

    response = requests.post(url, data=data)
    data = response.json()

    return [
        data['artist'],
        data['song'],
    ]
