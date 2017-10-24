from datetime import date
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import Count
from django.db.models.functions.datetime import TruncDay
from django.db.models.deletion import PROTECT


class RadioManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Radio(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    objects = RadioManager()

    def first_play(self):
        return self.play_set.order_by('timestamp').first()

    def last_play(self):
        return self.play_set.order_by('-timestamp').first()

    def plays(self, start=None, end=None):
        qs = self.play_set

        if start:
            qs = qs.filter(timestamp__date__gte=start)

        if end:
            qs = qs.filter(timestamp__date__lte=end)

        return qs

    def most_played_songs(self, start=None, end=None):
        return (self.plays(start, end)
                    .values('radio_id', 'artist_name', 'title')
                    .annotate(count=Count('*'))
                    .order_by("-count"))

    def most_played_daily(self, start=None, end=None):
        return (self.plays(start, end)
                    .annotate(day=TruncDay('timestamp'))
                    .values('radio_id', 'artist_name', 'title', 'day')
                    .annotate(count=Count('*'))
                    .order_by("-count"))

    def most_played_artists(self, start=None, end=None):
        return (self.plays(start, end)
                    .values('artist_name')
                    .annotate(count=Count('*'))
                    .order_by("-count"))

    def __str__(self):
        return '<Radio "{}">'.format(self.name)


class PlayManager(models.Manager):
    def month(self, year, month):
        """Returns plays within a given calendar month"""
        start = date(year, month, 1)
        end = start + relativedelta(months=1)

        return (self.get_queryset()
            .filter(timestamp__date__gte=start)
            .filter(timestamp__date__lt=end))


class Play(models.Model):
    radio = models.ForeignKey(Radio, PROTECT)
    artist_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PlayManager()

    def __str__(self):
        return '<Play "{}" by "{}">'.format(self.title, self.artist_name)
