from music.utils import get_or_create_artist
from radio.models import Play


def update_derived_data(radio, current_play):
    if not radio.first_play:
        radio.first_play = radio.get_first_play()

    radio.last_play = current_play
    radio.play_count = radio.get_play_count()
    radio.save()


def add_play(radio, artist_name, title):
    """Creates a new Play for the given radio unless it's a repeat.

    Returns a tuple:
      - True + created Play if the play was created
      - False + the last existing Play if it's a repeat
    """
    artist_name = artist_name.strip()
    title = title.strip()

    last_play = radio.get_last_play()

    if last_play and last_play.artist_name == artist_name and last_play.title == title:
        return False, last_play

    created, artist = get_or_create_artist(artist_name)
    if created:
        print("Created artist '{}' based on '{}' - '{}'".format(artist, artist_name, title))

    play = Play.objects.create(
        radio=radio,
        artist=artist,
        artist_name=artist_name,
        title=title,
    )

    update_derived_data(radio, play)

    return True, play
