import csv
from jobs.models import job, JobService
from reporting.models import Service
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, **options):
        with open('job_services.csv') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader)
            
            for line in reader:
                notif_no = line[1]
                try:
                    j = job.objects.get(notification_no=notif_no)
                    for i in range(22, 3, -2):
                        service_code = line[i]
                        service_quantity = line[i - 1]
                        if service_code:
                            try:
                                s = Service.objects.get(code=service_code)
                                JobService.objects.create(
                                    job=j, service=s, quantity=service_quantity
                                )
                                print(f'Created JobService for job {notif_no} and service {service_code} quantity {service_quantity}')
                            except Service.DoesNotExist:
                                print(f'Service: {service_code} does not exist')
                except job.DoesNotExist:
                    print(f'Job: {notif_no} does not exist')

                    