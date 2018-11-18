from django import forms

class SensorForm(forms.Form):
    sensorType = forms.CharField(label='Sensor Type', max_length=25)
    sensorLocation = forms.CharField(label='Sensor Location', max_length=25)
    sensorURL = forms.CharField(label='Sensor URL', max_length=100)
