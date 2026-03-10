from .base import *  # noqa

ALLOWED_HOSTS = ["www.radioscraper.com"]

STATIC_ROOT = "/var/www/radioscraper"

# Much security
# See `./manage.py check --deploy`
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 60 * 60
SECURE_REFERRER_POLICY = "same-origin"
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

# Logging to systemd
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "journal": {
            "class": "systemd.journal.JournalHandler",
            "formatter": "simple",
            "SYSLOG_IDENTIFIER": "radioscraper",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["journal"],
            "level": "INFO",
            "propagate": False,
        },
        # Don't log http requests
        "django.server": {
            "handlers": ["journal"],
            "level": "WARNING",
            "propagate": False,
        },
        "radioscraper": {
            "handlers": ["journal"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
