from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import TemperatureSensor, TemperatureRecord
from .forms import SensorForm

def index(request):
    return HttpResponse("This is the temperature app.")

def current_temps(request):
    context = {"sensor_temps": []}
    for nextSensor in TemperatureSensor.objects.all():
        allTemps = TemperatureRecord.objects.filter(sensor__exact=nextSensor).order_by('-timeRecorded')
        if len(allTemps) > 0:
            context["sensor_temps"].append({"sensor": nextSensor.location, "temp": allTemps[0].temperature})
        else:
            context["sensor_temps"].append({"sensor": nextSensor.location, "temp": "No recorded temperatures"})
    return render(request, 'temperature/current_temps.html', context=context)

@login_required
def sensors(request):
    if request.method == 'POST':
        for key in request.POST:
            if "sensor" in key:
                TemperatureSensor.objects.get(id=request.POST[key]).delete()
        return HttpResponseRedirect("/temperature/sensors/")
    context = {"sensors": []}
    for nextSensor in TemperatureSensor.objects.all():
        context["sensors"].append({"id": nextSensor.id, 
                                   "location": nextSensor.location, 
                                   "type": nextSensor.sensorType, 
                                   "url": nextSensor.url,
                                   "name": "sensor-" + str(nextSensor.id)})

    return render(request, 'temperature/sensors.html', context=context)

@login_required
def add_sensor(request):
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            sensorType = form.cleaned_data['sensorType']
            sensorLocation = form.cleaned_data['sensorLocation']
            sensorURL = form.cleaned_data['sensorURL']
            newSensor = TemperatureSensor(location=sensorLocation, sensorType=sensorType, url=sensorURL)
            newSensor.save()
            return HttpResponseRedirect("/temperature/sensors/")
    else:
        form = SensorForm()

    return render(request, 'temperature/add_sensor_form.html', {'form': form})

