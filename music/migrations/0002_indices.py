# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 16:43
from __future__ import unicode_literals

from django.db import migrations
from radioscraper.postgres.operations import CreateImmutableUnaccent


# Index which improves artist name lookup greatly
create_index = """
    CREATE INDEX idx_artistname_upper_iunaccent_name
    ON music_artistname(upper(iunaccent(name)))
"""

delete_index = """
    DROP INDEX idx_artistname_upper_iunaccent_name
"""


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        CreateImmutableUnaccent(),
        migrations.RunSQL(create_index, delete_index),
    ]
