from django.contrib import admin
from .models import Play, Radio


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ('id', 'radio', 'artist_name', 'title', 'timestamp')
    list_filter = ('radio',)


@admin.register(Radio)
class RadioAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'play_count', 'since', 'active')
    ordering = ('name',)

    def play_count(self, radio):
        return radio.plays().count()

    def since(self, radio):
        return radio.first_play().timestamp
