import time
from django.core.management.base import BaseCommand

from loaders.context import run_loaders
from radioscraper.utils.logger import get_logger

logger = get_logger(__name__)


class Command(BaseCommand):
    help = "For each defined radio, loads the current playing song and saves it to the database."

    def add_arguments(self, parser):
        parser.add_argument("radios", nargs="*", type=str)

    def handle(self, *args, **options):
        start = time.perf_counter()
        logger.info("Starting loaders...")
        summary = run_loaders(options["radios"])
        duration = time.perf_counter() - start
        counts = ", ".join([f"{result}: {count}" for result, count in summary.items()])
        logger.info(f"Loaders finished, duration={duration:.3f}s, {counts}")
