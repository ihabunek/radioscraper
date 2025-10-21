import pytz

from datetime import datetime, timedelta

from django.db import models
from django.db.models import Count
from django.db.models.deletion import PROTECT
from django.db.models.functions.datetime import TruncDay

from radioscraper.utils.datetime import day_start, day_end
from radioscraper.utils.datetime import month_start, month_end


class RadioManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class Radio(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    offline = models.BooleanField(default=False, help_text="Show as offline in the UI")
    load = models.BooleanField(default=True, help_text="Run loaders for this radio")

    # Derived data, cached for performance
    first_play = models.ForeignKey("radio.Play", on_delete=PROTECT, blank=True, null=True, related_name="+")
    last_play = models.ForeignKey("radio.Play", on_delete=PROTECT, blank=True, null=True, related_name="+")
    play_count = models.PositiveIntegerField(default=0)

    objects = RadioManager()

    def get_first_play(self):
        return self.play_set.order_by('timestamp').first()

    def get_last_play(self):
        return self.play_set.order_by('-timestamp').first()

    def get_play_count(self):
        return self.play_set.count()

    def recalculate_derived_data(self):
        self.first_play = self.get_first_play()
        self.last_play = self.get_last_play()
        self.play_count = self.get_play_count()

    def plays(self, start=None, end=None):
        qs = self.play_set

        if start:
            qs = qs.filter(timestamp__gte=day_start(start))

        if end:
            qs = qs.filter(timestamp__lt=day_end(end))

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

    @property
    def show_outage(self):
        if self.last_play:
            last = self.last_play.timestamp
            limit = datetime.now(pytz.UTC) - timedelta(days=1)
            return last < limit
        return False

    def __repr__(self):
        return 'Radio (name="{}")'.format(self.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PlayManager(models.Manager):
    def month(self, year, month):
        """Returns plays within a given calendar month"""
        return self.get_queryset().filter(
            timestamp__gte=month_start(year, month),
            timestamp__lt=month_end(year, month)
        )


class Play(models.Model):
    radio = models.ForeignKey(Radio, on_delete=PROTECT)
    artist = models.ForeignKey('music.Artist', on_delete=models.CASCADE, null=True)
    artist_name = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = PlayManager()

    def __str__(self):
        return '"{}" by "{}"'.format(self.title, self.artist_name)

    def __repr__(self):
        return 'Play (title="{}" artist="{}"'.format(self.title, self.artist_name)
