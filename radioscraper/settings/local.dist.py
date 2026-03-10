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

# Setup Sentry
# https://docs.sentry.io/platforms/python/integrations/django/
import sentry_sdk

sentry_sdk.init(
    dsn="...",
    environment="...",
    traces_sample_rate=0.1,
)
