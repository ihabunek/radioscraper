from bs4 import BeautifulSoup
from requests import Request


def form_request():
    return Request("GET", 'http://laganini.fm/live/?station=zagreb')


def parse_response(response):
    bs = BeautifulSoup(response.text, "html.parser")
    artist = bs.find_all('span', class_="author")
    song = bs.find_all('span', class_="song")

    if artist and song:
        return [
            artist[0].text.title(),
            song[0].text.capitalize()
        ]
