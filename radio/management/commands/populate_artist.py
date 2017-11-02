from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from music.utils import get_or_create_artist
from radio.models import Play


class Command(BaseCommand):
    def handle(self, *args, **options):
        names = (Play.objects
            .filter(artist__isnull=True)
            .order_by('artist_name')
            .values_list('artist_name', flat=True)
            .distinct())

        count = names.count()

        for ord, name in enumerate(names):
            with atomic():
                created, artist = get_or_create_artist(name)
                print("{}/{} {:50} {}".format(ord, count, name, "CREATED" if created else ""))
                Play.objects.filter(artist_name=name).update(artist=artist)
