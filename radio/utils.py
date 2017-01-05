import requests
import logging


def get_current_song(radio_slug):
    url = 'http://www.prvi.hr/modules/mod_radioplayer/tmpl/icecast_fireplay.php'
    data = {"song_cache_dirname": radio_slug}

    logging.debug("Fetching {} with data {}".format(url, data))

    response = requests.post(url, data=data)
    data = response.json()

    return [
        data['artist'],
        data['song'],
    ]
