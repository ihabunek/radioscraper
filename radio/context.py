import logging

from music.utils import get_or_create_artist
from radio.models import Radio, Play

logger = logging.getLogger(__name__)


def radios(request):
    return {
        "radios": Radio.objects.active().order_by('name')
    }


def add_play(radio, artist_name, title):
    artist_name = artist_name.strip()
    title = title.strip()

    last_play = radio.last_play
    if last_play and last_play.artist_name == artist_name and last_play.title == title:
        return False, last_play

    created, artist = get_or_create_artist(artist_name)
    if created:
        logger.info("Created artist '{}' based on '{}' - '{}'".format(artist, artist_name, title))

    play = Play.objects.create(
        radio=radio,
        artist=artist,
        artist_name=artist_name,
        title=title,
    )

    update_derived_data(radio, artist, play)

    return True, play


def update_derived_data(radio, artist, play):
    if not radio.first_play:
        radio.first_play = radio.get_first_play()

    radio.last_play = play
    radio.play_count = radio.get_play_count()
    radio.save()

    artist.recalculate_derived_data()
    artist.save()
