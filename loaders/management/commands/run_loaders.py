import logging

from django.core.management.base import BaseCommand
from django.utils import timezone as tz

from radio.models import Radio
from loaders.loaders import load_current_song
from loaders.utils import add_play
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TIMEOUT = 60


class Command(BaseCommand):
    help = 'For each defined radio, loads the current playing song and saves it to the database.'

    def __init__(self, *args, **kwargs):
        self.now = "{:%Y-%m-%d %H:%M:%S}".format(tz.now())
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('--debug', action='store_true')
        parser.add_argument('radio', nargs='?', type=str)

    def handle(self, *args, **options):
        if options['debug']:
            logging.getLogger().setLevel(logging.DEBUG)

        logger.info("-" * 50)
        logger.info("--- {:%Y-%m-%d %H:%M:%S} -- running loaders -------".format(tz.now()))
        logger.info("-" * 50)

        radio = options['radio']
        radios = Radio.objects.active().order_by('name')
        if radio:
            radios = radios.filter(slug=radio)

        try:
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(load_current_song, radio) for radio in radios]
                for future in as_completed(futures, timeout=TIMEOUT):
                    self.process_loader_result(*future.result())
        except TimeoutError:
            logger.error("Some loaders didn't make it. :(")

    def process_loader_result(self, radio, song, failure):
        if song:
            artist_name, title = song
            created, play = add_play(radio, artist_name, title)
            logger.info("{}: {} {}".format(radio.slug, play, "(repeated)" if not created else ""))
        elif failure:
            logger.error("{}: {} failure: {}".format(radio.slug, failure.type, failure.error_message))
        else:
            logger.info("{}: nothing currently playing".format(radio.slug))
