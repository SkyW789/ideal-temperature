from django.core.management.base import BaseCommand, CommandError
from temperature.models import DoorSensor, DoorRecord
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "Removes old temperature records"

    def add_arguments(self, parser):
        parser.add_argument('record_age_days',
                             type=int,
                             help="Records older then this age in days will be thinned")

    def handle(self, *args, **options):
        record_age_days = options['record_age_days']

        self.stdout.write("#### Starting the door database cleaning - " + str(datetime.now()) + "#####")

        sensors = DoorSensor.objects.all()

        for next_sensor in sensors:
            records = DoorRecord.objects.filter(sensor__id=next_sensor.id).filter(time__lte=timezone.now()-timedelta(days=record_age_days)).order_by('-time')
            self.stdout.write("Cleaning up " + next_sensor.name + ":")
            for next_record in records:
                self.stdout.write("Deleting: " + str(next_record.time) + ": " + str(next_record.state))
                next_record.delete()

        self.stdout.write("Finished the door database cleaning")
