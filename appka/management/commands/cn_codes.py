import csv
import os

from django.db import transaction

from appka.models import Commodity, CNCode

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open("./data/cn_codes.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            header_string = reader.__next__()
            header = header_string[0].split(";")
            cncode_pos = header.index("cncode")
            commodity_pos = header.index("commodity")
            cncode_active_pos = header.index("cncode_active")

            data = []

            with transaction.atomic():
                for row in reader:
                    if len(data) > 10:
                        CNCode.objects.bulk_create(data)
                        data = []

                    row = row[0].split(";")

                    commodity = Commodity.objects.filter(commodity_id=row[commodity_pos]).first()

                    if not commodity:
                        raise Exception(f"Missing commodity [{row[commodity_pos]}]")

                    cn_code = CNCode()
                    cn_code.cncode_active = row[cncode_active_pos]
                    cn_code.cncode = row[cncode_pos]
                    cn_code.commodity = commodity

                    data.append(cn_code)
                    # cn_code.save()

                if len(data) > 0:
                    CNCode.objects.bulk_create(data)