import requests

DEFAULT_TIMEOUT = 30


def get(*args, **kwargs):
    if "timeout" not in kwargs:
        kwargs["timeout"] = DEFAULT_TIMEOUT

    response = requests.get(*args, **kwargs)
    response.raise_for_status()

    return response


async def post(*args, **kwargs):
    if "timeout" not in kwargs:
        kwargs["timeout"] = DEFAULT_TIMEOUT

    response = requests.post(*args, **kwargs)
    response.raise_for_status()

    return response
