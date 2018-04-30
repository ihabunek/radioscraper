# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-01 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0007_play_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='artist_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='play',
            name='title',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]