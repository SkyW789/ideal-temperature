#!/usr/bin/python3

# Collect temperature data from all the sensors and store it in
# the database

import requests
import sys
from TempSensor import TempDatabase, TempDataPoint, TempSensor
from TempSensor import DatabaseNotFoundError, WriteTempError, TempGetError
from DataCollectionSettings import DB_FILE

try:
    tempConn = TempDatabase(DB_FILE)
except DatabaseNotFoundError:
    print("Error: " + DB_FILE + " does not exist")
    sys.exit()

sensors = tempConn.get_all_sensors()

for nextSensor in sensors:
    try:
        newTemp = nextSensor.get_current_temp()
    except TempGetError as e:
        print(e)
        continue
    print("Current temperature at " + nextSensor.location + " is " + str(newTemp.temp))
    try:
        tempConn.write_temp(newTemp)
    except WriteTempError as e:
        print(e)
        continue
