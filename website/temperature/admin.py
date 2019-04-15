from django.contrib import admin
from .models import TemperatureSensor, TemperatureRecord, GarageRecord, DoorSensor, DoorRecord

admin.site.register(TemperatureSensor)
admin.site.register(TemperatureRecord)
admin.site.register(DoorSensor)
admin.site.register(DoorRecord)
admin.site.register(GarageRecord)
