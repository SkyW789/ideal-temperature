from django.contrib import admin
from .models import TemperatureSensor, TemperatureRecord

admin.site.register(TemperatureSensor)
admin.site.register(TemperatureRecord)
