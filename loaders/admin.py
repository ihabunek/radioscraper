from django.contrib import admin
from loaders.models import Outage, LoaderFailure


@admin.register(Outage)
class OutageAdmin(admin.ModelAdmin):
    list_display = (
        'radio',
        'start',
        'end',
        'failure_count',
    )
    list_filter = ('radio',)
    ordering = ('start',)


@admin.register(LoaderFailure)
class LoaderFailureAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'type',
        'radio_name',
        'error_message',
    )
    list_filter = ('type', 'radio',)
    ordering = ('-timestamp',)

    def radio_name(self, failure):
        return failure.radio.name
