from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = "*"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'radioscraper_test',
        'USER': 'ihabunek',
        'PASSWORD': 'starseed',
        'HOST': '127.0.0.1',
        'PORT': '5433',
    }
}
