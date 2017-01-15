from django.db import models
from django.db.models import Count
from django.db.models.functions.datetime import TruncDay
from django.db.models.deletion import PROTECT


class Radio(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def first_play(self):
        return self.play_set.order_by('timestamp').first()

    def plays(self, start=None, end=None):
        qs = self.play_set

        if start:
            qs = qs.filter(timestamp__date__gte=start)

        if end:
            qs = qs.filter(timestamp__date__lte=end)

        return qs

    def most_played(self, start=None, end=None):
        return (self.plays(start, end)
                    .values('radio_id', 'artist', 'title')
                    .annotate(count=Count('*'))
                    .order_by("-count"))

    def most_played_daily(self, start=None, end=None):
        return (self.plays(start, end)
                    .annotate(day=TruncDay('timestamp'))
                    .values('radio_id', 'artist', 'title', 'day')
                    .annotate(count=Count('*'))
                    .order_by("-count"))

    def __str__(self):
        return '<Radio "{}">'.format(self.name)


class Play(models.Model):
    radio = models.ForeignKey(Radio, PROTECT)
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Play "{}" by "{}">'.format(self.title, self.artist)
