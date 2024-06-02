import csv
from django.db import transaction

import chardet
from appka.models import Commodity
from django.core.management.base import BaseCommand

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        encoding = detect_encoding("./data/commodity.csv")
        with open("./data/commodity.csv", "r", encoding=encoding) as csvfile:
            reader = csv.reader(csvfile)
            header_string = reader.__next__()
            header = header_string[0].split("|")
            commodity_id_pos = header.index("commodity_id")
            commodity_pos = header.index("commodity")
            commodity_active_pos = header.index("commodity_active")

            data = []

            with transaction.atomic():
                for row in reader:
                    if len(data) > 10:
                        Commodity.objects.bulk_create(data)
                        data = []

                    row = row[0].split(",")

                    commodity = Commodity()
                    commodity.commodity_active = row[commodity_active_pos]
                    commodity.commodity = row[commodity_pos]
                    commodity.commodity_id = row[commodity_id_pos]

                    data.append(commodity)

                if len(data) > 0:
                    Commodity.objects.bulk_create(data)
