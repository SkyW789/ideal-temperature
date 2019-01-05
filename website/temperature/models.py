from django.db import models
from django.contrib.auth.models import User

class TemperatureSensor(models.Model):
    location = models.CharField(max_length=50, default="unknown")
    sensorType = models.CharField(max_length=20, default="unknown")
    name = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class TemperatureRecord(models.Model):
    temperature = models.IntegerField(default=0)
    timeRecorded = models.DateTimeField('date and time recorded')
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.timeRecorded) + " " + str(self.temperature)
