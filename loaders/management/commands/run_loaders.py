import logging
from django.core.management.base import BaseCommand

from loaders.context import run_loaders


class Command(BaseCommand):
    help = "For each defined radio, loads the current playing song and saves it to the database."

    def add_arguments(self, parser):
        parser.add_argument("radios", nargs="*", type=str)
        parser.add_argument("--debug", action="store_true", help="Enable debug level logging")

    def handle(self, *args, **options):
        if options["debug"]:
            logging.basicConfig(level=logging.DEBUG)
        run_loaders(options["radios"])
