from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Populate Artist.play_count field with current values."

    query = """
        UPDATE music_artist a
        SET play_count = (
            SELECT count(*)
              FROM radio_play
             WHERE artist_id = a.id
        )
    """

    def handle(self, *args, **options):
        start = datetime.now()

        with connection.cursor() as cursor:
            cursor.execute(self.query)

        duration = datetime.now() - start

        print("Artists updated: {}.".format(cursor.rowcount))
        print("Time taken: {}".format(duration))
