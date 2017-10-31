import pytest

from radio.models import Radio
from loaders.utils import add_play


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
    created, play2 = add_play(radio, "foo", "bar")

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
