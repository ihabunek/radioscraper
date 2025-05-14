from django.contrib import admin
from music.models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'names',
    )
    ordering = ('name',)
