from rest_framework import serializers
from .models import TemperatureSensor, TemperatureRecord, GarageRecord
from django.contrib.auth.models import User

class TemperatureRecordSerializer(serializers.ModelSerializer):
    sensor = serializers.StringRelatedField(many=False)
    sensorName = serializers.CharField(max_length=25, write_only=True)
    class Meta:
        model = TemperatureRecord
        fields = ('id', 'temperature', 'timeRecorded', 'sensor', "sensorName")

    def create(self, validated_data):
        print("validated data = " + str(validated_data))
        validated_data['sensor'] = TemperatureSensor.objects.get(name=validated_data['sensorName'])
        validated_data.pop('sensorName', None)
        return TemperatureRecord.objects.create(**validated_data)

class GarageRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarageRecord
        fields = ('id', 'state', 'time')

