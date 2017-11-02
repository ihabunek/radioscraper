from django.db import models
from django.db.models.deletion import CASCADE


class Artist(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, db_index=True)

    def has_name(self, name):
        return self.names.filter(name=name).exists()

    def add_name(self, name):
        return ArtistName.objects.get_or_create(artist=self, name=name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ArtistName(models.Model):
    """Artists can have multiple variations of their name"""
    artist = models.ForeignKey(Artist, CASCADE, related_name="names")
    name = models.CharField(max_length=255, unique=True, db_index=True)
