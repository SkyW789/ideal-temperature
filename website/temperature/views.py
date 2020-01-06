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
from dateutil import parser
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

def chart(request):
    context = {
    "temp_sensors": [],
    "door_sensors": [],
    "light_sensors": []
    }
    for sensor in TemperatureSensor.objects.all():
        context['temp_sensors'].append({
                                    "location": sensor.location,
                                    "name": sensor.name
                                       })
    for sensor in DoorSensor.objects.all():
        context['door_sensors'].append({
                                    "location": sensor.location,
                                    "name": sensor.name
                                       })
    for sensor in DoorSensor.objects.all():
        context['light_sensors'].append({
                                    "location": sensor.location,
                                    "name": sensor.name
                                        })
    return render(request, "temperature/chart.html", context=context)

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

class TemperaturesBySensor(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Get the sensor
        if 'sensor' in request.query_params:
            sensor_name = request.query_params['sensor']
            sensor = TemperatureSensor.objects.get(name=sensor_name)
        else:
            sensor = TemperatureSensor.objects.all()[0]

        # Get the record count limit
        if 'record_count' in request.query_params:
            record_count = int(request.query_params['record_count'])
        else:
            record_count = 30

        # Initilize the query set and find all the temperature records associated
        # with the desired sensor
        temp_records = TemperatureRecord.objects.filter(sensor=sensor).order_by('timeRecorded')

        # Get the date range
        mountain_tz = pytz.timezone('America/Denver')
        if 'startDate' in request.query_params:
            start_date = parser.isoparse(request.query_params['startDate'])
        else:
            start_date = temp_records[0].timeRecorded
            print(start_date.utcoffset())
        if 'endDate' in request.query_params:
            end_date = parser.isoparse(request.query_params['endDate'])
        else:
            end_date = temp_records[len(temp_records)-1].timeRecorded
        if start_date.utcoffset() == None:
            start_date = start_date.replace(tzinfo=mountain_tz)
        if end_date.utcoffset() == None:
            end_date = end_date.replace(tzinfo=mountain_tz)

        # Reduce the query set to the desired date range
        temp_records = temp_records.filter(timeRecorded__gte=start_date.isoformat()).filter(timeRecorded__lte=end_date.isoformat())

        if len(temp_records) > record_count:
            interval = (end_date - start_date) / record_count
            time_point = start_date
            temp_list = []
            for record in temp_records:
                if record.timeRecorded >= time_point:
                    temp_list.append(record)
                    time_point = time_point + interval
        else:
            temp_list = temp_records

        temps = TemperatureRecordSerializer(temp_list, many=True)
        return Response(temps.data)
