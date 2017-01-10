import requests

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from datetime import datetime


class Command(BaseCommand):
    help = 'Loads history of plays from radio student (incomplete!)'

    def process_row(self, row):
        timestamp = row.find(class_='play_ts').text
        timestamp = datetime.strptime(timestamp, "%d.%m.%Y %H:%M:%S")

        song = row.find(class_='title').text.split('-', 1)
        song = [x.strip() for x in song]

        if len(song) == 2:
            print (timestamp, song)

    def process_page(self, page):
        print("Page {}".format(page))

        url = 'http://www.radiostudent.hr/slusas/page/{}/'.format(page)
        html = requests.get(url).text

        bs = BeautifulSoup(html, "html.parser")
        tbody = bs.find(id="the-list")
        rows = tbody.find_all('tr')

        print("Found {} rows".format(len(rows)))

        for row in rows:
            self.process_row(row)

    def handle(self, *args, **options):
        for page in range(5835, 0, -1):
            self.process_page(page)
            return
