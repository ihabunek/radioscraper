import traceback

import sys


from django.core.management.base import BaseCommand
from django.utils import timezone as tz
from radio.models import Radio, Play
from radio.utils import get_current_song


class Command(BaseCommand):
    help = 'For each defined radio, loads the current playing song and saves it to the database.'

    def log_error(self, string):
        self.stderr.write(string)

    def save(self, radio, artist, title):
        last_play = Play.objects.filter(radio=radio).order_by('-timestamp').first()

        if last_play and last_play.artist == artist and last_play.title == title:
            self.stdout.write("Repeated play {}, skipping".format(last_play))
            return

        play = Play.objects.create(radio=radio, artist=artist, title=title)
        self.stdout.write("Added play {}".format(play))

    def load_song(self, radio):
        try:
            self.stdout.write("\nLoading song for {}".format(radio.name))
            artist, title = get_current_song(radio.slug)
            self.save(radio, artist, title)
        except Exception:
            self.log_error("Failed loading song")
            traceback.print_exc()

    def handle(self, *args, **options):
        self.stdout.write("\n--- " + str(tz.now()) + " " + "-" * 60)
        for radio in Radio.objects.all():
            self.load_song(radio)

            # Required to preserve order when redirecting output to a file
            sys.stdout.flush()
            sys.stderr.flush()
