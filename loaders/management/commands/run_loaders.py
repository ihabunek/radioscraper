import logging

from django.core.management.base import BaseCommand
from loaders.context import run_loaders

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'For each defined radio, loads the current playing song and saves it to the database.'

    def add_arguments(self, parser):
        parser.add_argument('radios', nargs='*', type=str)

    def handle(self, *args, **options):
        logger.info("--- RUNNING LOADERS -------------------------------------")
        run_loaders(options['radios'])
        logger.info("--- DONE ------------------------------------------------")
        logger.info("")
