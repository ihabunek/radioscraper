from datetime import datetime


def timestamp_ms():
    """
    Returns current timestamp in milliseconds.
    """
    return int(datetime.now().timestamp() * 1000)
