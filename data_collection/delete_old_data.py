#!/usr/bin/python3

from TempSensor import DatabaseNotFoundError, WriteTempError
import TempSensor
import sys

DB_FILE = "../website/db-test.sqlite3"

try:
    tempConn = TempSensor.TempDatabase(DB_FILE)
except DatabaseNotFoundError:
    print("Error: " + DB_FILE + " does not exist")
    sys.exit()

tempConn.delete_old_temps(10)
