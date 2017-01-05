import os

__all__ = ['ENV_BOOL', 'ENV_STR', 'ENV_LIST']


def ENV_BOOL(name, default):  # noqa
    """
    Get a boolean value from environment variable.
    If the environment variable is not set or value is not one or "true" or
    "false", the default value is returned instead.
    """

    if name not in os.environ:
        return default
    if os.environ[name] == 'true':
        return True
    elif os.environ[name] == 'false':
        return False
    else:
        return default


def ENV_STR(name, default):  # noqa
    """
    Get a string value from environment variable.
    If the environment variable is not set, the default value is returned
    instead.
    """

    return os.environ.get(name, default)


def ENV_LIST(name, separator, default):  # noqa
    """
    Get a list of string values from environment variable.
    If the environment variable is not set, the default value is returned
    instead.
    """

    if name not in os.environ:
        return default
    return os.environ[name].split(separator)
