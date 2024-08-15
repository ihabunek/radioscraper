from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.functions import Lower

from radioscraper.postgres.lookups import ImmutableUnaccent


class Artist(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, db_index=True)

    # Derived data, cached for performance
    play_count = models.IntegerField(default=0)

    def has_name(self, name):
        return self.names.filter(name=name).exists()

    def add_name(self, name):
        return ArtistName.objects.get_or_create(artist=self, name=name)

    def recalculate_derived_data(self):
        self.play_count = self.play_set.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class ArtistName(models.Model):
    """Artists can have multiple variations of their name"""

    artist = models.ForeignKey(Artist, CASCADE, related_name="names")
    name = models.CharField(max_length=255, unique=True, db_index=True)
    search = models.GeneratedField(
        expression=Lower(ImmutableUnaccent("name")),
        output_field=models.CharField(max_length=255, db_index=True),
        db_persist=True,
    )
