from django import forms
from django.contrib.auth.models import User
from .models import TemperatureSensor

class SensorForm(forms.ModelForm):
    class Meta:
        model = TemperatureSensor
        fields = ['name', 'location', 'sensorType', 'owner']

