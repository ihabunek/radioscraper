from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from music.utils import get_or_create_artist
from radio.models import Play


class Command(BaseCommand):
    def process_name(self, name):
        created, artist = get_or_create_artist(name)
        Play.objects.filter(artist_name=name).update(artist=artist)
        return created, artist


    def handle(self, *args, **options):
        names = (Play.objects
            .filter(artist__isnull=True)
            .order_by('artist_name')
            .values_list('artist_name', flat=True)
            .distinct())

        count = names.count()
        start = datetime.now()

        for ord, name in enumerate(names):
            with atomic():
                created, artist = self.process_name(name)
                duration = (datetime.now() - start).total_seconds()
                speed = 1000 * duration / ord if ord else 0
                print("{:5}/{} {:50} {:3} {:.1f} ms/item".format(ord, count, name, "NEW" if created else "", speed))
