from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, permissions
from datetime import datetime
import pytz
from .serializers import TemperatureRecordSerializer, GarageRecordSerializer
from .models import TemperatureSensor, TemperatureRecord, GarageRecord
from .forms import SensorForm
from .permissions import IsOwnerOrReadOnly

def index(request):
    return HttpResponse("This is the temperature app.")

def current_temps(request):
    context = {"sensor_temps": []}
    mountain_tz = pytz.timezone('America/Denver')
    for nextSensor in TemperatureSensor.objects.all():
        allTemps = TemperatureRecord.objects.filter(sensor__exact=nextSensor).order_by('-timeRecorded')
        if len(allTemps) > 0:
            datetime_str = allTemps[0].timeRecorded.astimezone(
                    tz=pytz.timezone('America/Denver')).strftime('%B %d, %Y, %I:%M %p %Z')
            context["sensor_temps"].append({"sensor": nextSensor.location, 
                                            "temp": allTemps[0].temperature, 
                                            "datetime": datetime_str})
        else:
            context["sensor_temps"].append({"sensor": nextSensor.location, 
                                            "temp": "No recorded temperatures", 
                                            "datetime": "None"})
    return render(request, 'temperature/current_temps.html', context=context)

def current_garage(request):
    mountain_tz = pytz.timezone('America/Denver')
    garage_records = GarageRecord.objects.all().order_by('-time')
    if len(garage_records) > 0:
        latest_garage_state = garage_records[0].get_state_display()
        latest_garage_time = garage_records[0].time.astimezone(tz=mountain_tz).strftime('%B %d, %Y, %I:%M %p %Z')
    else:
        latest_garage_state = "No record"
        latest_garage_time = "N/A"
    context = {"state": latest_garage_state, "time": latest_garage_time}
    return render(request, 'temperature/current_garage.html', context=context)

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

class GarageRecordList(generics.ListCreateAPIView):
    queryset = GarageRecord.objects.all()
    serializer_class = GarageRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class GarageRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GarageRecord.objects.all()
    serializer_class = GarageRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
