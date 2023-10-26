import pytest

from radio.context import add_play
from music.models import Artist
from radio.models import Radio


@pytest.mark.django_db
def test_add_play():
    radio = Radio.objects.create(name="Radio One", slug="radio-one")

    assert radio.play_set.count() == 0
    assert radio.first_play is None
    assert radio.last_play is None
    assert radio.play_count == 0

    # Whitespace should be stripped
    created, play1 = add_play(radio, " foo ", "\tbar\n")

    assert created
    assert play1.artist_name == "foo"
    assert play1.title == "bar"

    assert radio.play_set.count() == 1
    assert radio.first_play == play1
    assert radio.last_play == play1
    assert radio.play_count == 1

    # Repeated song, should not create a new Play
    created, play1 = add_play(radio, "foo", "bar")

    assert not created
    assert play1.artist_name == "foo"
    assert play1.title == "bar"

    assert radio.play_set.count() == 1
    assert radio.first_play == play1
    assert radio.last_play == play1
    assert radio.play_count == 1

    # A different song, should create a new Play
    created, play2 = add_play(radio, "mrm", "brm")

    assert created
    assert play2.artist_name == "mrm"
    assert play2.title == "brm"

    assert radio.play_set.count() == 2
    assert radio.first_play == play1
    assert radio.last_play == play2
    assert radio.play_count == 2

    # One more song
    created, play3 = add_play(radio, "foo", "brm")

    assert created
    assert play3.artist_name == "foo"
    assert play3.title == "brm"

    assert radio.play_set.count() == 3
    assert radio.first_play == play1
    assert radio.last_play == play3
    assert radio.play_count == 3

    # Check artist derived data
    assert Artist.objects.get(slug='foo').play_count == 2
    assert Artist.objects.get(slug='mrm').play_count == 1


@pytest.mark.django_db
def test_artist_slug_must_not_be_empty():
    radio = Radio.objects.create(name="Radio One", slug="radio-one")
    with pytest.raises(ValueError) as exinfo:
        add_play(radio, "-", "-")
    assert str(exinfo.value).startswith("Cannot create artist")
