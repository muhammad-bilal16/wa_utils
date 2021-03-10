import csv
from reporting.models import Service
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, **options):
        with open('rates_data.csv') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            
            for line in reader:
                line[-1] = float(line[-1])
                line[-2] = float(line[-2])

                rate_data = {}
                for i in range(len(headers)):
                    rate_data[headers[i]] = line[i]

                Service.objects.create(**rate_data)