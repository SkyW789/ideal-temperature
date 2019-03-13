from django.core.management.base import BaseCommand, CommandError
from temperature.models import TemperatureSensor, TemperatureRecord
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "Removes old temperature records"

    def add_arguments(self, parser):
        parser.add_argument('record_age_days', 
                             type=int, 
                             help="Records older then this age in days will be thinned")
        parser.add_argument('new_interval_minutes', 
                             type=int, 
                             help="New record frequency in minutes applied to all records older than record_age_days")

    def handle(self, *args, **options):
        record_age_days = options['record_age_days']
        interval_minutes = options['new_interval_minutes']

        self.stdout.write("#### Starting the database cleaning - " + str(datetime.now()) + "#####")
        
        sensors = TemperatureSensor.objects.all()
        
        for next_sensor in sensors:
            temp_records = TemperatureRecord.objects.filter(sensor__id=next_sensor.id).filter(timeRecorded__lte=timezone.now()-timedelta(days=record_age_days)).order_by('-timeRecorded')
            
            self.stdout.write("Cleaning up " + next_sensor.name + ":")
            last_time = timezone.now()
            for next_record in temp_records:
                if last_time - next_record.timeRecorded < timedelta(hours=1):
                    self.stdout.write("Deleting: " + str(next_record.timeRecorded) + ": " + str(next_record.temperature))
                    next_record.delete()
                else:
                    last_time = next_record.timeRecorded

        self.stdout.write("Finished the database cleaning")

