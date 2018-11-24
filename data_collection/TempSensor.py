#!/usr/bin/python3

import requests
from datetime import datetime, timedelta, date
import sqlite3
from django.utils import timezone
import os

class TempSensor():

    def __init__(self, unit='F', address=None, 
                 location=None, index=None, 
                 sensorType=None, rawTupleData=None):
        unit = unit.upper()
        if not unit == 'F' and not unit == 'C':
            raise ValueError("Supplied unit is not valid. Must be C or F")
        else:
            self.unit = unit
        if rawTupleData is None:
            self.address = address
            self.location = location
            self.index = index
            self.sensorType = sensorType
        else:
            if not type(rawTupleData) == tuple:
                raise ValueError("Supplied rawTupleData is not a Tuple")
            if not len(rawTupleData) == 4:
                raise ValueError("Supplied rawTubpleData is the wrong length")
            self.index = rawTupleData[0]
            self.location = rawTupleData[1]
            self.sensorType = rawTupleData[2]
            self.address = rawTupleData[3]

    def address_set(self):
        if self.address is None:
            return False
        else:
            return True

    def location_set(self):
        if self.location is None:
            return False
        else:
            return True
        
    def get_current_temp(self):
        maxTries = 3
        count = 0
        newTemp = 0
        while count < maxTries:
            try:
                r = requests.get(self.address)
                newTemp = float(r.text)
                if r.status_code == 200:
                    break
                else:
                    count += 1
            except (ValueError, ConnectionError) as e:
                count += 1
        return TempDataPoint(temp=newTemp, unit=self.unit, sensor=self)

class TempDataPoint():

    def __init__(self, temp=0, unit='F', time=datetime.utcnow(), sensor=None):
        self.temp = temp
        self.unit = unit
        self.time = time
        self.sensor = sensor

    def convert_to_C(self):
        if self.unit == "F":
            self.temp = (self.temp - 32) * (5/9)
            self.unit = "C"

    def convert_to_F(self):
        if self.unit == "C":
            self.temp = self.temp * 9/5 + 32
            self.unit = "F"

class DatabaseNotFoundError(Exception):
    pass

class WriteTempError(Exception):
    pass

class TempDatabase():

    def __init__(self, databaseFile):
        self.databaseFile = databaseFile
        if os.path.isfile(databaseFile):
            self.connection = sqlite3.connect(databaseFile)
        else:
            raise DatabaseNotFoundError("TempDatabase: the provided database does not exist")

    def write_temp(self, tempDataPoint):
        connCursor = self.connection.cursor()
        tempDataPoint.convert_to_F()
        if tempDataPoint.sensor is None:
            raise WriteTempError("Sensor is unknown")
        else:
            insertData = (tempDataPoint.temp, 
                          tempDataPoint.time,
                          tempDataPoint.sensor.index)
            connCursor.execute("INSERT INTO temperature_temperaturerecord (temperature, timeRecorded, sensor_id) VALUES (?, ?, ?)", insertData)
            self.connection.commit()

    def get_sensor_id_from_location(self, location):
        connCursor = self.connection.cursor()
        t = (location,)
        connCursor.execute("SELECT id FROM temperature_temperaturesensor WHERE location=?", t)
        results = connCursor.fetchone()
        if results is None:
            return None
        else:
            return results[0]

    def get_all_sensors(self):
        connCursor = self.connection.cursor()
        connCursor.execute("SELECT * FROM temperature_temperaturesensor")
        sensors = []
        for sensorArray in connCursor.fetchall():
            sensors.append(TempSensor(rawTupleData=sensorArray))
            
        return sensors

    def add_sensor(self, sensor):
        connCursor = self.connection.cursor()
        t = (sensor.location, sensor.sensorType, sensor.address)
        connCursor.execute("INSERT INTO temperature_temperaturesensor ('location', 'sensorType', 'url') VALUES(?, ?, ?)", t)
        self.connection.commit()
    
    def delete_old_temps(self, daysOlderThan):
        connCursor = self.connection.cursor()
        t = ("-" + str(daysOlderThan) + " days")
        oldDate = date.today() - timedelta(days=daysOlderThan)
        h = (oldDate,)
        connCursor.execute("DELETE FROM temperature_temperaturerecord WHERE timeRecorded < ?", h)
        self.connection.commit()
