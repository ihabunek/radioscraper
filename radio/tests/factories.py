import factory

from factory.django import DjangoModelFactory
from radio.models import Radio, Play
from music.tests.factories import ArtistFactory


class RadioFactory(DjangoModelFactory):
    name = factory.Faker('text')
    slug = factory.Faker('slug')

    class Meta:
        model = Radio


class PlayFactory(DjangoModelFactory):
    radio = factory.SubFactory(RadioFactory)
    artist = factory.SubFactory(ArtistFactory)
    artist_name = factory.Faker('text', max_nb_chars=30)
    title = factory.Faker('text', max_nb_chars=50)

    class Meta:
        model = Play
