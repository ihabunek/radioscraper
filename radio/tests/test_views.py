import pytest

from django.urls import reverse
from django.utils import timezone as tz

from music.models import Artist
from radio.models import Radio, Play


@pytest.fixture
def radio_data():
    radio = Radio.objects.create(name="Radio One", slug="radio-one")

    artist = Artist.objects.create(name="Gang of four", slug="gang-of-four")

    common = {"radio": radio, "artist": artist}
    first = Play.objects.create(title="Foo", artist_name="Gang of four", **common)
    Play.objects.create(title="Bar", artist_name="Gang of four", **common)
    last = Play.objects.create(title="Baz", artist_name="Gang of four", **common)

    radio.first_play = first
    radio.last_play = last
    radio.play_count = 3
    radio.save()

    return radio


@pytest.mark.django_db
def test_index_view(client, radio_data):
    date = tz.now()

    response = client.get(reverse('ui:index'))
    assert response.status_code == 200

    content = str(response.content)
    assert '<h5>Radio One</h5>' in content
    assert '3 plays' in content
    assert 'since {:%d.%m.%Y}'.format(date) in content
    assert 'Last play:' in content
    assert '<b>Baz</b>' in content
    assert 'by <b>Gang of four</b>' in content


@pytest.mark.django_db
def test_stats_views(client, radio_data):

    response = client.get(reverse('radio:stats'))
    assert response.status_code == 200

    response = client.get(reverse('radio:stats', args=["radio-one"]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_plays_view(client, radio_data):
    response = client.get(reverse('radio:plays'))
    assert response.status_code == 200

    content = str(response.content)
    assert "Foo" in content
    assert "Bar" in content
    assert "Baz" in content
    assert "Gang of four" in content
