# Generated by Django 5.1 on 2024-08-15 11:55

import django.db.models.functions.text
import radioscraper.postgres.lookups
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_artist_play_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistname',
            name='search',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.functions.text.Lower(radioscraper.postgres.lookups.ImmutableUnaccent('name')), output_field=models.CharField(db_index=True, max_length=255)),
        ),
    ]
