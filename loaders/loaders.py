from django.utils import timezone
from importlib import import_module
from requests import Session
from requests.exceptions import RequestException
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
    return ResponseData.objects.create(
        status_code=response.status_code,
        contents=response.content,
    )


def create_failure(radio, failure_type, request, response, ex, tb):
    error_message = "{}: {}".format(type(ex).__name__, str(ex)) if ex else ""

    # Create or continue an outage
    outage, created = Outage.objects.get_or_create(radio=radio, end__isnull=True, defaults={
        "start": timezone.now(),
    })

    outage.failure_count += 1
    outage.save(update_fields=["failure_count"])

    return LoaderFailure.objects.create(
        type=failure_type,
        radio=radio,
        outage=outage,
        error_message=error_message,
        stack_trace=tb or '',
        request=create_request_data(request),
        response=create_response_data(response) if response else None,
    )


def create_connect_failure(radio, request, ex, tb):
    return create_failure(radio, LoaderFailure.TYPE_CONNECT, request, None, ex, tb)


def create_request_failure(radio, request, response):
    return create_failure(radio, LoaderFailure.TYPE_FETCH, request, response, None, None)


def create_parse_failure(radio, request, response, ex, tb):
    return create_failure(radio, LoaderFailure.TYPE_PARSE, request, response, ex, tb)


def get_loader(radio_slug):
    return import_module('loaders.implementations.{}'.format(radio_slug))


def load_current_song(radio, timeout=20):
    """
    Loads currently playing song by the given radio.

    Returns a tuple of:
    - radio   - the given radio object, used to resolve futures
    - song    - the song playing as a tuple (artist_name, song_title),
                or None if failed to fetch or if nothing is currently playing
    - failure - if failed, a Failure object describing the issue
    """
    loader = get_loader(radio.slug)
    stream = getattr(loader, "stream", False)  # Whether to stream the response
    request = loader.form_request()

    with Session() as session:
        prepared = session.prepare_request(request)

        try:
            response = session.send(prepared, stream=stream, timeout=timeout)
        except RequestException as ex:
            failure = create_connect_failure(radio, request, ex, format_exc())
            return radio, None, failure

        if response.status_code >= 400:
            failure = create_request_failure(radio, request, response)
            return radio, None, failure

        try:
            song = loader.parse_response(response)
        except Exception as ex:
            failure = create_parse_failure(radio, request, response, ex, format_exc())
            return radio, None, failure

    # Close any open outages
    Outage.objects.filter(radio=radio, end__isnull=True).update(end=timezone.now())

    return radio, song, None
