#!/usr/bin/python3

# Collect temperature data from all the sensors and store it in
# the database

import requests
from TempSensor import TempDatabase, TempDataPoint
from TempSensor import TempSensor
from TempSensor import DatabaseNotFoundError, WriteTempError
import sys

DB_FILE = "../website/db.sqlite3"

try:
    tempConn = TempDatabase(DB_FILE)
except DatabaseNotFoundError:
    print("Error: " + DB_FILE + " does not exist")
    sys.exit()

sensors = tempConn.get_all_sensors()

for nextSensor in sensors:
    newTemp = nextSensor.get_current_temp()
    print("Current temperature at " + nextSensor.location + " is " + str(newTemp.temp))
    try:
        tempConn.write_temp(newTemp)
    except WriteTempError as e:
        print(e)
        continue
