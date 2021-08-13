import aiohttp
import asyncio
import logging
import sys

from django.db import transaction
from django.utils import timezone
from importlib import import_module
from traceback import format_exception

from loaders.models import LoaderFailure, Outage
from radio.models import Radio
from radio.context import add_play

logger = logging.getLogger(__name__)

HTTP_TIMEOUT = 50
AWAIT_TIMEOUT = 60


def get_loader(radio_slug):
    return import_module(f"loaders.implementations.{radio_slug}")


def run_loaders(slugs=None):
    radios = Radio.objects.active().order_by('name')
    if slugs:
        radios = radios.filter(slug__in=slugs)
    radios = list(radios)

    results = asyncio.run(load_all(radios))
    for radio, song, exc_info in results:
        process_loader_result(radio, song, exc_info)


async def load_all(radios):
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        aws = [load_one(session, radio) for radio in radios]
        results = await asyncio.gather(*aws)

    return [(radio, song, exc) for radio, (song, exc) in zip(radios, results)]


async def load_one(session, radio):
    loader = get_loader(radio.slug)

    try:
        song = await asyncio.wait_for(loader.load(session), timeout=AWAIT_TIMEOUT)
        return song, None
    except:
        return None, sys.exc_info()


def process_loader_result(radio, song, exc_info):
    if song:
        artist_name, title = song
        created, play = handle_success(radio, artist_name, title)
        repeated = "(repeated)" if not created else ""
        logger.info(f"{radio.slug}: {play} {repeated}")
    elif exc_info:
        handle_failure(radio, exc_info)
        logger.error(f"{radio.slug} failed", exc_info=exc_info)
    else:
        logger.info(f"{radio.slug}: nothing currently playing")


@transaction.atomic
def handle_success(radio, artist_name, title):
    # Close any open outages
    Outage.objects.filter(radio=radio, end__isnull=True).update(end=timezone.now())

    return add_play(radio, artist_name, title)


@transaction.atomic
def handle_failure(radio, exc_info):
    # Create or continue an outage
    outage, created = Outage.objects.get_or_create(
        radio=radio,
        end__isnull=True,
        defaults={
            "start": timezone.now(),
        }
    )

    outage.failure_count += 1
    outage.save(update_fields=["failure_count"])

    ex = exc_info[1]
    error_message = str(ex) or ex.__class__.__name__
    stack_trace = "".join(format_exception(*exc_info))

    return LoaderFailure.objects.create(
        radio=radio,
        outage=outage,
        error_message=error_message,
        stack_trace=stack_trace,
    )
