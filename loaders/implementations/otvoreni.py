from bs4 import BeautifulSoup
from requests import Request


def form_request():
    return Request("GET", "http://www.otvoreni.hr/player/")


def parse_response(response):
    bs = BeautifulSoup(response.text, "html.parser")
    artist = bs.find(id="song-artist")
    song = bs.find(id="song-track")

    return [
        artist.text.title(),
        song.text.capitalize()
    ]
