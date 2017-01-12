from django.db import models
from django.db.models.deletion import PROTECT


class Radio(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def first_play(self):
        return self.play_set.order_by('timestamp').first()

    def __str__(self):
        return '<Radio "{}">'.format(self.name)


class Play(models.Model):
    radio = models.ForeignKey(Radio, PROTECT)
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Play "{}" by "{}">'.format(self.title, self.artist)
