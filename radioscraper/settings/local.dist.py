# Choose prod or dev environment
from .dev import *  # noqa
# from .prod import *

# Set up database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# # Set up email for prod
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = ""
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = ""
# EMAIL_HOST_PASSWORD = ""
# EMAIL_SUBJECT_PREFIX = "[Radioscraper]"

# Setup Sentry
# https://docs.sentry.io/platforms/python/integrations/django/
import sentry_sdk

sentry_sdk.init(
    dsn="...",
    environment="...",
    traces_sample_rate=0.1,
)
