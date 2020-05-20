from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL
from django.contrib.postgres.fields.jsonb import JSONField


class Outage(models.Model):
    """
    Created when a loder fails repeatedly.
    """
    radio = models.ForeignKey('radio.Radio', on_delete=CASCADE, related_name='outages')
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    failure_count = models.PositiveIntegerField(default=0)


class LoaderFailure(models.Model):
    """
    Contains the exception info which caused a loader to fail.
    """
    radio = models.ForeignKey('radio.Radio', on_delete=CASCADE)
    outage = models.ForeignKey(Outage, on_delete=SET_NULL, blank=True, null=True, related_name="failures")
    timestamp = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True)
    stack_trace = models.TextField(blank=True)
