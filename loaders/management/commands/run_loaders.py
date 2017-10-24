from django.core.management.base import BaseCommand
from django.utils import timezone as tz

from radio.models import Radio, Play
from loaders.loaders import load_current_song, LoaderError


class Command(BaseCommand):
    help = 'For each defined radio, loads the current playing song and saves it to the database.'

    def __init__(self, *args, **kwargs):
        self.now = "{:%Y-%m-%d %H:%M:%S}".format(tz.now())
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('radio', nargs='?', type=str)

    def save(self, radio, artist_name, title):
        last_play = radio.get_last_play()

        if last_play and last_play.artist_name == artist_name and last_play.title == title:
            self.stdout.write("Repeated play {}, skipping".format(last_play))
            return

        play = Play.objects.create(
            radio=radio,
            artist_name=artist_name,
            title=title,
        )

        # Update derived data on Radio
        radio.last_play = play
        radio.play_count = radio.play_set.count()
        radio.save()

        self.stdout.write("Added play {}".format(play))

    def load_song(self, radio):
        try:
            self.stdout.write("\nLoading song for {}".format(radio.name))
            song = load_current_song(radio)
            if song:
                artist_name, title = song
                self.save(radio, artist_name, title)

        except LoaderError:
            self.stdout.write("Failed loading song :/")

    def handle(self, *args, **options):
        self.stdout.write("\n--- " + self.now + " " + "-" * 60)

        radio = options['radio']
        qs = Radio.objects.all()
        if radio:
            qs = qs.filter(slug=radio)

        for radio in qs:
            self.load_song(radio)
