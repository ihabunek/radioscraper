from .base import *  # noqa

ALLOWED_HOSTS = ['www.radioscraper.com']

ADMINS = [('Ivan Habunek', 'ivan@habunek.com')]

# Much security
# See `./manage.py check --deploy`
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 60 * 60
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(process)8d %(levelname)8s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'app': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local6',
            'formatter': 'default',
            'address': '/dev/log'
        },
        'loaders': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'local7',
            'formatter': 'default',
            'address': '/dev/log'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['app', 'mail_admins'],
            'level': 'ERROR'
        },
        'loaders': {
            'handlers': ['loaders', 'mail_admins'],
            'level': 'INFO',
        }
    },
}
