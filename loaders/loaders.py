import sys

from django.utils import timezone
from importlib import import_module
from traceback import format_exc

from loaders.models import LoaderFailure, Outage, RequestData, ResponseData


class LoaderError(Exception):
    def __init__(self, failure):
        super().__init__("Loader failure")
        self.failure = failure


def create_request_data(request):
    return RequestData.objects.create(
        method=request.method,
        url=request.url,
    )


def create_response_data(response):
    ct = response.headers.get("content-type")
    safe = any([
        ct.startswith("text"),
        ct.startswith("application/json"),
    ])

    # Read response content only for text content types
    if safe:
        contents = response.content[:16384]
    else:
        contents = f"Stripped. Content type: {ct}"

    return ResponseData.objects.create(
        status_code=response.status_code,
        contents=contents,
    )


def create_failure(radio, ex, tb):
    # Create or continue an outage
    outage, created = Outage.objects.get_or_create(
        radio=radio,
        end__isnull=True,
        defaults={
            "start": timezone.now(),
        }
    )

    request = getattr(ex, "request", None)
    response = getattr(ex, "response", None)

    request_data = create_request_data(request) if request else None
    response_data = create_response_data(response) if response else None

    outage.failure_count += 1
    outage.save(update_fields=["failure_count"])

    return LoaderFailure.objects.create(
        radio=radio,
        outage=outage,
        error_message=str(ex),
        stack_trace=tb,
        request=request_data,
        response=response_data,
    )


def get_loader(radio_slug):
    return import_module('loaders.implementations.{}'.format(radio_slug))


def load_current_song(radio, timeout=20):
    """
    Loads currently playing song by the given radio.

    Returns a tuple of:
    - radio    - the given radio object, used to resolve futures
    - song     - the song playing as a tuple (artist_name, song_title),
                 or None if failed to fetch or if nothing is currently playing
    - exc_info - if failed, the exception info
    """
    loader = get_loader(radio.slug)

    try:
        song = loader.load()
    except Exception as ex:
        create_failure(radio, ex, format_exc())
        return radio, None, sys.exc_info()

    # Close any open outages
    Outage.objects.filter(radio=radio, end__isnull=True).update(end=timezone.now())

    return radio, song, None
