import traceback

from django.core.management.base import BaseCommand
from radio.models import Radio


class Command(BaseCommand):
    help = 'For each defined radio recalculates the derived data (first_song, ' \
           'last_song, play_count).'

    def handle(self, *args, **options):
        for radio in Radio.objects.all():
            print("Processing {}".format(radio))
            radio.recalculate_derived_data()
            radio.save()
        print("Done")
