from django.contrib import admin
from .models import TemperatureSensor, TemperatureRecord, DoorSensor, DoorRecord, LightSensor, LightRecord

admin.site.register(TemperatureSensor)
admin.site.register(TemperatureRecord)
admin.site.register(DoorSensor)
admin.site.register(DoorRecord)
admin.site.register(LightSensor)
admin.site.register(LightRecord)
