import csv
from django.db import transaction

import chardet
from appka.models import Country
from django.core.management.base import BaseCommand

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        encoding = detect_encoding("./data/countries.csv")
        with open("./data/countries.csv", "r", encoding=encoding) as csvfile:
            reader = csv.reader(csvfile)
            header_string = reader.__next__()
            header = header_string[0].split("|")
            country_code_pos = header.index("country_code")
            country_pos = header.index("country")
            country_active_pos = header.index("country_active")

            data = []

            with transaction.atomic():
                for row in reader:
                    if len(data) > 10:
                        Country.objects.bulk_create(data)
                        data = []

                    row = row[0].split("|")

                    country = Country()
                    country.country_active = row[country_active_pos]
                    country.country = row[country_pos]
                    country.country_code = row[country_code_pos]

                    data.append(country)

                if len(data) > 0:
                    Country.objects.bulk_create(data)
