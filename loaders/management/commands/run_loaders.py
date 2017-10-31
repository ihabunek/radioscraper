from django.core.management.base import BaseCommand
from django.utils import timezone as tz

from radio.models import Radio
from loaders.loaders import load_current_song, LoaderError
from loaders.utils import add_play


class Command(BaseCommand):
    help = 'For each defined radio, loads the current playing song and saves it to the database.'

    def __init__(self, *args, **kwargs):
        self.now = "{:%Y-%m-%d %H:%M:%S}".format(tz.now())
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('radio', nargs='?', type=str)

    def save(self, radio, artist_name, title):
        created, play = add_play(radio, artist_name, title)

        if created:
            self.stdout.write("Added play {}".format(play))
        else:
            self.stdout.write("Repeated play {}, skipping".format(play))

    def load_song(self, radio):
        try:
            self.stdout.write("\nLoading song for {}".format(radio.name))
            song = load_current_song(radio)
            if song:
                artist_name, title = song
                self.save(radio, artist_name, title)
            else:
                self.stdout.write("Looks like nothing is being played.")

        except LoaderError:
            self.stdout.write("Failed loading song :/")

    def handle(self, *args, **options):
        self.stdout.write("\n--- " + self.now + " " + "-" * 60)

        radio = options['radio']
        qs = Radio.objects.all().order_by('name')
        if radio:
            qs = qs.filter(slug=radio)

        for radio in qs:
            self.load_song(radio)
