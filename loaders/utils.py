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
    last_play = radio.get_last_play()

    if last_play and last_play.artist_name == artist_name and last_play.title == title:
        return False, last_play

    play = Play.objects.create(
        radio=radio,
        artist_name=artist_name.strip(),
        title=title.strip(),
    )

    update_derived_data(radio, play)

    return True, play
