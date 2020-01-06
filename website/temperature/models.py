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
    temperature = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    timeRecorded = models.DateTimeField('date and time recorded')
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.pk}: {self.sensor} {self.timeRecorded} {self.temperature}"

class DoorSensor(models.Model):
    location = models.CharField(max_length=50, default="unknown")
    sensorType = models.CharField(max_length=20, default="unknown")
    name = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class DoorRecord(models.Model):
    STATES= (
        ("O", "Open"),
        ("C", "Closed"),
    )
    state = models.CharField(max_length=1, choices=STATES)
    time = models.DateTimeField('date and time recorded')
    sensor = models.ForeignKey(DoorSensor, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.time) + " " + str(self.state)

class LightSensor(models.Model):
    location = models.CharField(max_length=50, default="unknown")
    sensorType = models.CharField(max_length=20, default="unknown")
    name = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class LightRecord(models.Model):
    STATES = (
        ("O", "On"),
        ("F", "Off"),
    )
    state = models.CharField(max_length=1, choices=STATES)
    time = models.DateTimeField('date and time recorded')
    sensor = models.ForeignKey(LightSensor, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.time) + " " + str(self.state)
