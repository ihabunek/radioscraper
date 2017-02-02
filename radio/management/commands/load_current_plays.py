import traceback

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone as tz
from radio.models import Radio, Play
from radio.utils.loaders import get_current_song
from raven import Client


class Command(BaseCommand):
    help = 'For each defined radio, loads the current playing song and saves it to the database.'

    def __init__(self, *args, **kwargs):
        self.now = "{:%Y-%m-%d %H:%M:%S}".format(tz.now())
        super(Command, self).__init__(*args, **kwargs)

    def save(self, radio, artist_name, title):
        last_play = Play.objects.filter(radio=radio).order_by('-timestamp').first()

        if last_play and last_play.artist_name == artist_name and last_play.title == title:
            self.stdout.write("Repeated play {}, skipping".format(last_play))
            return

        play = Play.objects.create(radio=radio, artist_name=artist_name, title=title)
        self.stdout.write("Added play {}".format(play))

    def load_song(self, radio):
        try:
            self.stdout.write("\nLoading song for {}".format(radio.name))
            song = get_current_song(radio.slug)
            if song:
                artist_name, title = song
                self.save(radio, artist_name, title)

        except Exception:
            self.stdout.write("#############################################")
            self.stdout.write("### Failed loading song. Check error log. ###")
            self.stdout.write("#############################################")

            # traceback will write to stderr
            self.stderr.write("\n--- " + self.now + " " + "-" * 60)
            traceback.print_exc()

            # Report to Sentry
            if settings.SENTRY_DSN:
                client = Client(settings.SENTRY_DSN)
                client.captureException()

    def handle(self, *args, **options):
        self.stdout.write("\n--- " + self.now + " " + "-" * 60)
        for radio in Radio.objects.all():
            self.load_song(radio)
