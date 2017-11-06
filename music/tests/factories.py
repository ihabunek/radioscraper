import factory

from factory.django import DjangoModelFactory
from music.models import Artist, ArtistName


class ArtistFactory(DjangoModelFactory):
    name = factory.Faker('name')
    slug = factory.Faker('slug')

    class Meta:
        model = Artist


class ArtistNameFactory(DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = ArtistName
