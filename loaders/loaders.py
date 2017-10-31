from importlib import import_module
from requests import Session
from traceback import format_exc

from django.utils import timezone

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


def create_failure(radio, failure_type, request, response, ex=None, tb=None):
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
        response=create_response_data(response),
    )


def create_request_failure(radio, request, response):
    return create_failure(radio, LoaderFailure.TYPE_FETCH, request, response)


def create_parse_failure(radio, request, response, exception, traceback):
    return create_failure(radio, LoaderFailure.TYPE_PARSE, request, response, exception, traceback)


def get_loader(radio_slug):
    return import_module('loaders.implementations.{}'.format(radio_slug))


def load_current_song(radio):
    loader = get_loader(radio.slug)

    # Fetch data
    request = loader.form_request()
    session = Session()
    response = session.send(request.prepare())

    if response.status_code >= 400:
        failure = create_request_failure(radio, request, response)
        raise LoaderError(failure)

    # Parse data
    try:
        song = loader.parse_response(response)
    except Exception as ex:
        failure = create_parse_failure(radio, request, response, ex, format_exc())
        raise LoaderError(failure)

    # Close any open outages
    Outage.objects.filter(radio=radio, end__isnull=True).update(end=timezone.now())

    return song
