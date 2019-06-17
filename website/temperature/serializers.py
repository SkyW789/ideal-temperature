from rest_framework import serializers
from .models import TemperatureSensor, TemperatureRecord, DoorSensor, DoorRecord, LightSensor, LightRecord
from django.contrib.auth.models import User

class TemperatureRecordSerializer(serializers.ModelSerializer):
    sensor = serializers.StringRelatedField(many=False)
    sensorName = serializers.CharField(max_length=25, write_only=True)
    class Meta:
        model = TemperatureRecord
        fields = ('id', 'temperature', 'timeRecorded', 'sensor', "sensorName")

    def create(self, validated_data):
        validated_data['sensor'] = TemperatureSensor.objects.get(name=validated_data['sensorName'])
        validated_data.pop('sensorName', None)
        return TemperatureRecord.objects.create(**validated_data)

class DoorRecordSerializer(serializers.ModelSerializer):
    sensor = serializers.StringRelatedField(many=False)
    sensorName = serializers.CharField(max_length=25, write_only=True)
    class Meta:
        model = DoorRecord
        fields = ('id', 'state', 'time', 'sensor', 'sensorName')

    def create(self, validated_data):
        validated_data['sensor'] = DoorSensor.objects.get(name=validated_data['sensorName'])
        validated_data.pop('sensorName', None)
        return DoorRecord.objects.create(**validated_data)

class LightRecordSerializer(serializers.ModelSerializer):
    sensor = serializers.StringRelatedField(many=False)
    sensorName = serializers.CharField(max_length=25, write_only=True)
    class Meta:
        model = LightRecord
        fields = ('id', 'state', 'time', 'sensor', 'sensorName')

    def create(self, validated_data):
        validated_data['sensor'] = LightSensor.objects.get(name=validated_data['sensorName'])
        validated_data.pop('sensorName', None)
        return LightRecord.objects.create(**validated_data)
