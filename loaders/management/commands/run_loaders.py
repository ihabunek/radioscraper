import logging

from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from django.core.management.base import BaseCommand
from loaders.loaders import load_current_song
from loaders.utils import add_play
from radio.models import Radio

logger = logging.getLogger(__name__)

TIMEOUT = 60


class Command(BaseCommand):
    help = 'For each defined radio, loads the current playing song and saves it to the database.'

    def add_arguments(self, parser):
        parser.add_argument('radio', nargs='?', type=str)

    def handle(self, *args, **options):
        logger.info("### RUNNING LOADERS ###")

        radio = options['radio']
        radios = Radio.objects.active().order_by('name')
        if radio:
            radios = radios.filter(slug=radio)

        try:
            with ThreadPoolExecutor() as executor:
                self.dispatch(executor, radios)
        except TimeoutError:
            logger.exception("Some loaders didn't make it. :(")

        logger.info("### DONE ###")

    def dispatch(self, executor, radios):
        futures = [executor.submit(load_current_song, radio) for radio in radios]
        for future in as_completed(futures, timeout=TIMEOUT):
            self.process_loader_result(*future.result())

    def process_loader_result(self, radio, song, failure):
        if song:
            artist_name, title = song
            created, play = add_play(radio, artist_name, title)
            logger.info("{}: {} {}".format(radio.slug, play, "(repeated)" if not created else ""))
        elif failure:
            logger.error("{}: {} failure: {}".format(radio.slug, failure.type, failure.error_message))
        else:
            logger.info("{}: nothing currently playing".format(radio.slug))
