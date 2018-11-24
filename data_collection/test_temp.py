#!/usr/bin/python3

from TempSensor import TempSensor, TempDataPoint
import pytest
from datetime import datetime

# Tests for TempSensor class
def test_initial_values_set():
    sensor = TempSensor(unit="f", address="test.com", 
                        location="Upstairs Hallway", index=2, 
                        sensorType="Pi")
    assert sensor.unit == "F"
    assert sensor.address == "test.com"
    assert sensor.location == "Upstairs Hallway"
    assert sensor.index == 2
    assert sensor.sensorType == "Pi"

def test_initial_values_set_tuple():
    sensorData = (1, "Test Location", "Test Sensor Type", "Test url")
    sensor = TempSensor(rawTupleData=sensorData)
    assert sensor.unit == "F"
    assert sensor.address == "Test url"
    assert sensor.location == "Test Location"
    assert sensor.index == 1
    assert sensor.sensorType == "Test Sensor Type"

def test_initial_values_set_tuple_exception():
    sensorData = (1, "testLocation", "Test Sensor Type")
    with pytest.raises(ValueError):
        TempSensor(rawTupleData=sensorData)

def test_address_set_false():
    sensor = TempSensor()
    assert sensor.address_set() == False

def test_address_set_true():
    sensor = TempSensor(address="hello.com")
    assert sensor.address_set() == True

def test_location_set_false():
    sensor = TempSensor()
    assert sensor.location_set() == False

def test_location_set_true():
    sensor = TempSensor(location="hallway")
    assert sensor.location_set() == True

def test_initial_unit_exception():
    with pytest.raises(ValueError):
        TempSensor(unit="d")

def test_initial_unit_valid():
    assert TempSensor(unit="c").unit == "C"

# Tests for TempDataPoint class
def test_initial_temp_data_point():
    tempValue = TempDataPoint()
    assert tempValue.temp == 0
    assert tempValue.unit == 'F'
    assert type(tempValue.time) is datetime
    assert type(tempValue.sensor) is TempSensor or tempValue.sensor is None

def test_convert_to_F():
    tempValue = TempDataPoint(temp=11, unit='C')
    tempValue.convert_to_F()
    assert tempValue.temp == 51.8
    assert tempValue.unit == 'F'

def test_convert_to_C():
    tempValue = TempDataPoint(temp=32, unit='F')
    tempValue.convert_to_C()
    assert tempValue.temp == 0
    assert tempValue.unit == 'C'


