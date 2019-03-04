from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .serializers import TemperatureRecordSerializer
from .models import TemperatureSensor, TemperatureRecord
from .forms import SensorForm
from .permissions import IsOwnerOrReadOnly

def index(request):
    return HttpResponse("This is the temperature app.")

def current_temps(request):
    context = {"sensor_temps": []}
    for nextSensor in TemperatureSensor.objects.all():
        allTemps = TemperatureRecord.objects.filter(sensor__exact=nextSensor).order_by('-timeRecorded')
        if len(allTemps) > 0:
            context["sensor_temps"].append({"sensor": nextSensor.location, "temp": allTemps[0].temperature, "datetime": allTemps[0].timeRecorded})
        else:
            context["sensor_temps"].append({"sensor": nextSensor.location, "temp": "No recorded temperatures", "datetime": "None"})
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
                                   "owner": nextSensor.owner.username,
                                   "name": nextSensor.name})

    return render(request, 'temperature/sensors.html', context=context)

@login_required
def add_sensor(request):
    if request.method == 'POST':
        sensor_form = SensorForm(request.POST)
        if sensor_form.is_valid():
            sensor_form.save()
            return HttpResponseRedirect("/temperature/sensors/")
    else:
        sensor_form = SensorForm()

    return render(request, 'temperature/add_sensor_form.html', {'sensor_form': sensor_form})


## API views ##

class TemperatureRecordList(generics.ListCreateAPIView):
    queryset = TemperatureRecord.objects.all()
    serializer_class = TemperatureRecordSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    #def perform_create(self, serializer):
    #    print(serializer)
    #    sensor = TemperatureSensor.objects.get(name=serializer.data['sensorName'])
    #    serializer.save(sensor=sensor)

class TemperatureRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemperatureRecord.objects.all()
    serializer_class = TemperatureRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

