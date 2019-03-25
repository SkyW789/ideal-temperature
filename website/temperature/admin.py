from django.contrib import admin
from .models import TemperatureSensor, TemperatureRecord, GarageRecord

admin.site.register(TemperatureSensor)
admin.site.register(TemperatureRecord)
admin.site.register(GarageRecord)
