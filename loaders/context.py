from contextlib import asynccontextmanager
from types import SimpleNamespace
import aiohttp
import asyncio
import sys
import time

from django.db import transaction
from django.utils import timezone
from importlib import import_module
from traceback import format_exception

import sentry_sdk

from loaders.models import LoaderFailure, Outage
from radio.models import Radio
from radio.context import add_play
from radioscraper.utils.logger import get_logger

logger = get_logger(__name__)

HTTP_TIMEOUT = 50
AWAIT_TIMEOUT = 60


@asynccontextmanager
async def client_session():
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT)
    async with aiohttp.ClientSession(
        timeout=timeout,
        trace_configs=[logger_trace_config()],
        # Ignore invalid SSL certificates
        connector=aiohttp.TCPConnector(ssl=False),
    ) as session:
        yield session


def get_loader(radio_slug):
    return import_module(f"loaders.implementations.{radio_slug}")


def run_loaders(slugs=None):
    radios = Radio.objects.filter(load=True).order_by('name')
    if slugs:
        radios = radios.filter(slug__in=slugs)
    radios = list(radios)

    results = asyncio.run(load_all(radios))
    for radio, song, exc_info in results:
        process_loader_result(radio, song, exc_info)


async def load_all(radios):
    async with client_session() as session:
        aws = [load_one(session, radio) for radio in radios]
        results = await asyncio.gather(*aws)

    return [(radio, song, exc) for radio, (song, exc) in zip(radios, results)]


async def load_one(session, radio):
    loader = get_loader(radio.slug)

    try:
        song = await asyncio.wait_for(loader.load(session), timeout=AWAIT_TIMEOUT)
        return song, None
    except Exception:
        return None, sys.exc_info()


def process_loader_result(radio, song, exc_info):
    if song:
        artist, title = song
        if not artist or not title:
            error = f"{radio.slug} loader returned an empty artist or title. artist={artist}, title={title}"
            logger.error(error)
            sentry_sdk.capture_message(error)
            return

        created, play = handle_success(radio, artist, title)
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

def logger_trace_config() -> aiohttp.TraceConfig:
    async def on_request_start(
        session: aiohttp.ClientSession,
        context: SimpleNamespace,
        params: aiohttp.TraceRequestStartParams,
    ):
        context.start = time.monotonic()
        logger.debug(f"--> {params.method} {params.url}")

    async def on_request_redirect(
        session: aiohttp.ClientSession,
        context: SimpleNamespace,
        params: aiohttp.TraceRequestRedirectParams,
    ):
        logger.debug(f"--> redirected to {params.method} {params.url}")

    async def on_request_end(
        session: aiohttp.ClientSession,
        context: SimpleNamespace,
        params: aiohttp.TraceRequestEndParams,
    ):
        elapsed = round(1000 * (time.monotonic() - context.start))
        logger.debug(f"<-- {params.method} {params.url} HTTP {params.response.status} {elapsed}ms")

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    trace_config.on_request_redirect.append(on_request_redirect)
    return trace_config
