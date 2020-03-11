# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-03-11 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loaders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loaderfailure',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='loaders.RequestData'),
        ),
        migrations.AlterField(
            model_name='loaderfailure',
            name='type',
            field=models.CharField(choices=[('connect', 'Connect'), ('fetch', 'Fetch'), ('other', 'Other'), ('parse', 'Parse')], max_length=10),
        ),
    ]
