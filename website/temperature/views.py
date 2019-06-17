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
from .serializers import TemperatureRecordSerializer, DoorRecordSerializer, LightRecordSerializer
from .models import TemperatureSensor, TemperatureRecord, DoorSensor, DoorRecord, LightSensor, LightRecord
from .forms import SensorForm
from .permissions import IsOwnerOrReadOnly

def index(request):
    return HttpResponse("This is the temperature app.")

def current_status(request):
    context = {
        "sensor_temps": [],
        "sensor_doors": [],
        "sensor_lights": []
    }
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

    for nextSensor in DoorSensor.objects.all():
        allStates = DoorRecord.objects.filter(sensor__exact=nextSensor).order_by('-time')
        if len(allStates) > 0:
            datetime_str = allStates[0].time.astimezone(tz=mountain_tz).strftime('%B %d, %Y, %I:%M %p %Z')
            context["sensor_doors"].append({"sensor"    : nextSensor.location,
                                            "state"     : allStates[0].get_state_display(),
                                            "datetime"  : datetime_str})
        else:
            context["sensor_doors"].append({"sensor"    : nextSensor.location,
                                            "state"     : "No record",
                                            "datetime"  : "None"})

    for nextSensor in LightSensor.objects.all():
        allStates = []
        allStates = LightRecord.objects.filter(sensor__exact=nextSensor).order_by('-time')
        if len(allStates) > 0:
            datetime_str = allStates[0].time.astimezone(tz=mountain_tz).strftime('%B %d, %Y, %I:%M %p %Z')
            context['sensor_lights'].append({"sensor"   : nextSensor.location,
                                             "state"    : allStates[0].get_state_display(),
                                             "datetime" : datetime_str})

        else:
            context['sensor_lights'].append({"sensor"   : nextSensor.location,
                                             "state"    : "No record",
                                             "datetime" : "None"})

    return render(request, "temperature/current_state.html", context=context)

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
    # Defines the associated sensor model. Required for use
    # with the IsOwnerOrReadOnly permission class
    sensor_class = TemperatureSensor

class TemperatureRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemperatureRecord.objects.all()
    serializer_class = TemperatureRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class DoorRecordList(generics.ListCreateAPIView):
    queryset = DoorRecord.objects.all()
    serializer_class = DoorRecordSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    # Defines the associated sensor model. Required for use
    # with the IsOwnerOrReadOnly permission class
    sensor_class = DoorSensor

class DoorRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoorRecord.objects.all()
    serializer_class = DoorRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class LightRecordList(generics.ListCreateAPIView):
    queryset = LightRecord.objects.all()
    serializer_class = LightRecordSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    # Defines the associated sensor model. Required for use
    # with the IsOwnerOrReadOnly permission class
    sensor_class = LightSensor

class LightRecordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LightRecord.objects.all()
    serializer_class = LightRecordSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
