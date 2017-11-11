import pytest

from django.urls import reverse
from radio.models import Radio, Play
from django.utils import timezone as tz


@pytest.fixture
def radio_data():
    radio = Radio.objects.create(name="Radio One", slug="radio-one")

    first = Play.objects.create(radio=radio, title="Foo", artist_name="Gang of four")
    Play.objects.create(radio=radio, title="Bar", artist_name="Gang of four")
    last = Play.objects.create(radio=radio, title="Baz", artist_name="Gang of four")

    radio.first_play = first
    radio.last_play = last
    radio.play_count = 3
    radio.save()

    return radio


@pytest.mark.django_db
def test_index_view(client, radio_data):
    dt = tz.now()
    date = dt.strftime('%d.%m.%Y')

    response = client.get(reverse('ui:index'))
    assert response.status_code == 200

    content = str(response.content)
    assert '<h5>Radio One</h5>' in content
    assert '3 plays' in content
    assert 'since {}'.format(date) in content
    assert 'Last play:' in content
    assert '<b>Baz</b>' in content
    assert 'by <b>Gang of four</b>' in content


@pytest.mark.django_db
def test_stats_views(client, radio_data):

    response = client.get(reverse('radio:stats'))
    assert response.status_code == 200

    response = client.get(reverse('radio:stats', kwargs={"radio_slug": "radio-one"}))
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
