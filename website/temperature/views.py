from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
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
    template = loader.get_template("temperature/current_temps.html")
    return HttpResponse(template.render(context))

def sensors(request):
    if request.method == 'POST':
        for key in request.POST:
            TemperatureSensor.objects.get(id=request.POST[key])
        return HttpResponse(request.POST['1'])
    context = {"sensors": []}
    for nextSensor in TemperatureSensor.objects.all():
        context["sensors"].append({"id": nextSensor.id, "location": nextSensor.location, "type": nextSensor.sensorType, "url": nextSensor.url})

    return render(request, 'temperature/sensors.html', context=context)

def add_sensor(request):
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            sensorType = form.cleaned_data['sensorType']
            sensorLocation = form.cleaned_data['sensorLocation']
            sensorURL = form.cleaned_data['sensorURL']
            newSensor = TemperatureSensor(location=sensorLocation, sensorType=sensorType, url=sensorURL)
            newSensor.save()
            return HttpResponse("Sensor Type is " + sensorType)
    else:
        form = SensorForm()

    return render(request, 'temperature/add_sensor_form.html', {'form': form})


# TemperatureRecord.objects.filter(timeRecorded__gte=timezone.now() - timedelta(hours=20))
