from django.contrib import admin
from .models import Play, Radio


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'radio',
        'artist_name',
        'title',
        'timestamp',
    )

    list_filter = ('radio',)


@admin.register(Radio)
class RadioAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'play_count',
        'since',
        'active',
        'load',
        'offline',
    )

    readonly_fields = (
        'first_play',
        'last_play',
        'play_count',
    )

    ordering = ('name',)

    def since(self, radio):
        return radio.first_play.timestamp if radio.first_play else None
