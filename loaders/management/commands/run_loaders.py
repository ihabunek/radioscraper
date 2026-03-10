from django.core.management.base import BaseCommand

from loaders.context import run_loaders


class Command(BaseCommand):
    help = "For each defined radio, loads the current playing song and saves it to the database."

    def add_arguments(self, parser):
        parser.add_argument("radios", nargs="*", type=str)

    def handle(self, *args, **options):
        run_loaders(options["radios"])
