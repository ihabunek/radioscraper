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


class RequestData(models.Model):
    """
    Holds HTTP request data.
    """
    method = models.CharField(max_length=10)
    url = models.CharField(max_length=1000)
    post_data = JSONField(blank=True, null=True)

    def __repr__(self):
        return "Request('{}', '{}')".format(self.method, self.url)


class ResponseData(models.Model):
    """
    Holds HTTP response data.
    """
    status_code = models.PositiveSmallIntegerField()
    contents = models.TextField()

    def __repr__(self):
        return "Response({})".format(self.status_code)


class LoaderFailure(models.Model):
    """
    Contains the exception info which caused a loader to fail.
    """
    radio = models.ForeignKey('radio.Radio', on_delete=CASCADE)
    outage = models.ForeignKey(Outage, on_delete=SET_NULL, blank=True, null=True, related_name="failures")
    timestamp = models.DateTimeField(auto_now_add=True)
    request = models.ForeignKey(RequestData, on_delete=PROTECT, blank=True, null=True)
    response = models.ForeignKey(ResponseData, on_delete=PROTECT, blank=True, null=True)
    error_message = models.TextField(blank=True)
    stack_trace = models.TextField(blank=True)
