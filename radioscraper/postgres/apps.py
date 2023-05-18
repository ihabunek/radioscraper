from django.apps import AppConfig
from django.db.models import CharField, TextField

from .lookups import ImmutableUnaccent


class PostgresConfig(AppConfig):
    name = "radioscraper.postgres"
    label = "postgres_addons"
    verbose_name = "PostgreSQL additions"

    def ready(self):
        CharField.register_lookup(ImmutableUnaccent)
        TextField.register_lookup(ImmutableUnaccent)
