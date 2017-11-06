import pytest

from music.models import Artist, ArtistName
from music.utils import merge_artists
from music.tests.factories import ArtistFactory, ArtistNameFactory
from radio.tests.factories import RadioFactory, PlayFactory


@pytest.mark.django_db
def test_merge():
    r = RadioFactory()

    a1 = ArtistFactory()
    a2 = ArtistFactory()
    a3 = ArtistFactory()

    PlayFactory(radio=r, artist=a1)
    PlayFactory(radio=r, artist=a1)
    PlayFactory(radio=r, artist=a2)
    PlayFactory(radio=r, artist=a2)
    PlayFactory(radio=r, artist=a3)
    PlayFactory(radio=r, artist=a3)

    n11 = ArtistNameFactory(artist=a1)
    n12 = ArtistNameFactory(artist=a1)
    n21 = ArtistNameFactory(artist=a2)
    n22 = ArtistNameFactory(artist=a2)
    n31 = ArtistNameFactory(artist=a3)
    n32 = ArtistNameFactory(artist=a3)

    assert r.play_set.count() == 6
    assert r.play_set.filter(artist=a1).count() == 2
    assert r.play_set.filter(artist=a2).count() == 2
    assert r.play_set.filter(artist=a3).count() == 2

    artists = Artist.objects.filter(pk__in=[a2.pk, a3.pk])
    merge_artists(artists, a1, n32)

    assert Artist.objects.filter(pk=a1.pk).exists()
    assert not Artist.objects.filter(pk=a2.pk).exists()
    assert not Artist.objects.filter(pk=a3.pk).exists()

    assert r.play_set.count() == 6
    assert r.play_set.filter(artist=a1).count() == 6

    assert ArtistName.objects.filter(artist=a1).count() == 6
