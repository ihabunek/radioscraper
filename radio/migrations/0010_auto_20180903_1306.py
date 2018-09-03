# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-03 11:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('radio', '0009_play_timestamp_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radio',
            name='first_play',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='radio.Play'),
        ),
        migrations.AlterField(
            model_name='radio',
            name='last_play',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='radio.Play'),
        ),
    ]