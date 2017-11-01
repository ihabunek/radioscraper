from django.apps import AppConfig
from django.db.models import CharField, TextField
from django.utils.translation import ugettext_lazy as _

from .lookups import ImmutableUnaccent


class PostgresConfig(AppConfig):
    name = 'radioscraper.postgres'
    label = 'postgres_addons'
    verbose_name = _('PostgreSQL additions')

    def ready(self):
        CharField.register_lookup(ImmutableUnaccent)
        TextField.register_lookup(ImmutableUnaccent)
