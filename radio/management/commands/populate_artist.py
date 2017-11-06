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

    def process_plays(self, plays):
        print(plays.values_list('radio__slug', flat=True).distinct())

        names = (plays
            .filter(artist__isnull=True)
            .order_by('-artist_name')
            .values_list('artist_name', flat=True)
            .distinct())

        count = names.count()
        start = datetime.now()

        for ord, name in enumerate(names):
            with atomic():
                created, artist = self.process_name(name)
                duration = (datetime.now() - start).total_seconds()
                speed = 1000 * duration / ord if ord else 0
                new = "NEW" if created else ""
                print("{:5}/{} {:50} {:3} {:.1f} ms/item".format(ord, count, name, new, speed))

    def handle(self, *args, **options):
        # Process radios Martin and Student last, because they have the worst tag quality
        problematic =['martin', 'student']
        best_plays = Play.objects.exclude(radio__slug__in=problematic)
        worst_plays = Play.objects.filter(radio__slug__in=problematic)

        self.process_plays(best_plays)
        self.process_plays(worst_plays)
