import pytest

from music.models import Artist, ArtistName
from music.utils import find_artist, find_artist_by_name, _name_variants


@pytest.mark.django_db
def test_find_artist_1():
    artist = Artist.objects.create(name="Sia", slug="sia")
    ArtistName.objects.create(artist=artist, name="Sia")

    assert find_artist('sia') == artist
    assert find_artist('Sia') == artist
    assert find_artist('SIA') == artist

    # Random whitespace
    assert find_artist('\t sia \n') == artist
    assert find_artist('\t Sia \n') == artist
    assert find_artist('\t SIA \n') == artist

    # Featuring in various combinations
    assert find_artist('Sia feat. some guy') == artist
    assert find_artist('Sia feat some guy') == artist
    assert find_artist('Sia Feat. some guy') == artist
    assert find_artist('Sia Feat some guy') == artist
    assert find_artist('Sia FEAT. some guy') == artist
    assert find_artist('Sia FEAT some guy') == artist
    assert find_artist('Sia ft. some guy') == artist
    assert find_artist('Sia ft some guy') == artist
    assert find_artist('Sia Ft. some guy') == artist
    assert find_artist('Sia Ft some guy') == artist
    assert find_artist('Sia FT. some guy') == artist
    assert find_artist('Sia FT some guy') == artist

    # Control
    assert find_artist('Sija') is None
    assert find_artist('Sija feat some guy') is None


def test_name_variants():
    assert list(_name_variants("Simon & Garfunkel")) == [
        'Simon & Garfunkel',
        'The Simon & Garfunkel',
        'Simon i Garfunkel',
        'Simon and Garfunkel',
        'Simon + Garfunkel'
    ]

    assert list(_name_variants("Simon + Garfunkel")) == [
        'Simon + Garfunkel',
        'The Simon + Garfunkel',
        'Simon & Garfunkel',
        'Simon i Garfunkel',
        'Simon and Garfunkel'
    ]

    assert list(_name_variants("Simon and Garfunkel")) == [
        'Simon and Garfunkel',
        'The Simon and Garfunkel',
        'Simon & Garfunkel',
        'Simon i Garfunkel',
        'Simon + Garfunkel'
    ]

    assert list(_name_variants("Simon i Garfunkel")) == [
        'Simon i Garfunkel',
        'The Simon i Garfunkel',
        'Simon & Garfunkel',
        'Simon and Garfunkel',
        'Simon + Garfunkel'
    ]


@pytest.mark.django_db
def test_find_artist_conjunctions():
    artist = Artist.objects.create(name="Tamara Obrovac & Transhistria Electric", slug="foo")
    ArtistName.objects.create(artist=artist, name="Tamara Obrovac & Transhistria Electric")

    assert find_artist_by_name('Tamara Obrovac & Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac and Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac AND Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac i Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac I Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac + Transhistria Electric') == artist

    artist.delete()

    artist = Artist.objects.create(name="Tamara Obrovac i Transhistria Electric", slug="foo")
    ArtistName.objects.create(artist=artist, name="Tamara Obrovac i Transhistria Electric")

    assert find_artist_by_name('Tamara Obrovac & Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac and Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac AND Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac i Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac I Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac + Transhistria Electric') == artist

    artist.delete()

    artist = Artist.objects.create(name="Tamara Obrovac I Transhistria Electric", slug="foo")
    ArtistName.objects.create(artist=artist, name="Tamara Obrovac i Transhistria Electric")

    assert find_artist_by_name('Tamara Obrovac & Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac and Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac AND Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac i Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac I Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac + Transhistria Electric') == artist

    artist.delete()

    artist = Artist.objects.create(name="Tamara Obrovac and Transhistria Electric", slug="foo")
    ArtistName.objects.create(artist=artist, name="Tamara Obrovac and Transhistria Electric")

    assert find_artist_by_name('Tamara Obrovac & Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac and Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac AND Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac i Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac I Transhistria Electric') == artist
    assert find_artist_by_name('Tamara Obrovac + Transhistria Electric') == artist

    artist.delete()


@pytest.mark.django_db
@pytest.mark.parametrize("name", [
    'sia',
    'Śìá',
    'ŚÌÁ',
    'śìá',
])
def test_find_artist_accents(name):
    artist = Artist.objects.create(name=name, slug="foo")
    ArtistName.objects.create(artist=artist, name=name)

    assert find_artist_by_name('sia') == artist
    assert find_artist_by_name('Śìá') == artist
    assert find_artist_by_name('ŚÌÁ') == artist
    assert find_artist_by_name('śìá') == artist


@pytest.mark.django_db
def test_find_artist_reversed():
    artist = Artist.objects.create(name="Alen Vitasović", slug="foo")
    ArtistName.objects.create(artist=artist, name="Alen Vitasović")

    assert find_artist_by_name('Vitasović Alen') == artist

    # Testing a bug which was fixed
    artist = Artist.objects.create(name="Jones Tom", slug="bar")
    ArtistName.objects.create(artist=artist, name="Jones Tom")

    assert find_artist_by_name('Tom Jones & Elvis presley') is None


@pytest.mark.django_db
def test_the_article_removal():
    artist = Artist.objects.create(name="The Queen", slug="foo")
    ArtistName.objects.create(artist=artist, name="The Queen")

    assert find_artist_by_name('Queen') == artist


@pytest.mark.django_db
def test_the_article_addition():
    artist = Artist.objects.create(name="Queen", slug="foo")
    ArtistName.objects.create(artist=artist, name="Queen")

    assert find_artist_by_name('The Queen') == artist


@pytest.mark.django_db
def test_track_number_preceding_artist_name():
    artist = Artist.objects.create(name="Elvis Costello", slug="foo")
    ArtistName.objects.create(artist=artist, name="Elvis Costello")

    assert find_artist_by_name('01 Elvis Costello') == artist
    assert find_artist_by_name('01. Elvis Costello') == artist
    assert find_artist_by_name('01.Elvis Costello') == artist
    assert find_artist_by_name('1.Elvis Costello') == artist
    assert find_artist_by_name('1 Elvis Costello') == artist
    assert find_artist_by_name('01-Elvis Costello') == artist
    assert find_artist_by_name('1-Elvis Costello') == artist
