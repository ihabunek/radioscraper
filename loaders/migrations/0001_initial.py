# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 11:01
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('radio', '0005_radio_derived_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoaderFailure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('fetch', 'Fetch'), ('parse', 'Parse')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('error_message', models.TextField(blank=True)),
                ('stack_trace', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Outage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('failure_count', models.PositiveIntegerField(default=0)),
                ('radio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outages', to='radio.Radio')),
            ],
        ),
        migrations.CreateModel(
            name='RequestData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('GET', 'GET'), ('POST', 'POST')], max_length=10)),
                ('url', models.CharField(max_length=1000)),
                ('post_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResponseData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.PositiveSmallIntegerField()),
                ('contents', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='loaderfailure',
            name='outage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='failures', to='loaders.Outage'),
        ),
        migrations.AddField(
            model_name='loaderfailure',
            name='radio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='radio.Radio'),
        ),
        migrations.AddField(
            model_name='loaderfailure',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='loaders.RequestData'),
        ),
        migrations.AddField(
            model_name='loaderfailure',
            name='response',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='loaders.ResponseData'),
        ),
    ]
