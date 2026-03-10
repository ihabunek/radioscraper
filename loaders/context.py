from __future__ import annotations

import asyncio
from collections import defaultdict
import sys
import time
from contextlib import asynccontextmanager
from enum import StrEnum, auto
from importlib import import_module
from traceback import format_exception
from types import SimpleNamespace

import aiohttp
from django.db import transaction
from django.utils import timezone

from loaders.models import LoaderFailure, Outage
from radio.context import add_play
from radio.models import Radio
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


def run_loaders(slugs=None) -> dict[LoaderResult, int]:
    radios = Radio.objects.filter(load=True).order_by("name")
    if slugs:
        radios = radios.filter(slug__in=slugs)
    radios = list(radios)

    summary: dict[LoaderResult, int] = defaultdict(lambda: 0)
    results = asyncio.run(load_all(radios))
    for radio, song, exc_info in results:
        result = process_loader_result(radio, song, exc_info)
        summary[result] += 1

    return summary

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


class LoaderResult(StrEnum):
    SONG_LOADED = auto()
    NOTHING_PLAYING = auto()
    ERROR = auto()


def process_loader_result(radio, song, exc_info) -> LoaderResult:
    if song:
        artist, title = song
        if not artist or not title:
            error = f"{radio.slug} loader returned an empty artist or title. artist={artist}, title={title}"
            logger.error(error)
            return LoaderResult.ERROR

        created, play = handle_success(radio, artist, title)
        repeated = "(repeated)" if not created else ""
        logger.info(f"{radio.slug}: {play} {repeated}")
        return LoaderResult.SONG_LOADED
    elif exc_info:
        handle_failure(radio, exc_info)
        logger.error(f"{radio.slug} failed", exc_info=exc_info)
        return LoaderResult.ERROR
    else:
        logger.info(f"{radio.slug}: nothing currently playing")
        return LoaderResult.NOTHING_PLAYING


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
        },
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
