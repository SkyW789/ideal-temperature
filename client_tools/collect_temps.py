#!/usr/bin/env python

# Collects temperature data on a raspberry pi and sends
# it to the server.

from TempHelper import TempDataPoint, TempComm
import ClientData

url = ClientData.url
username = ClientData.username
password = ClientData.password
sensorPath = ClientData.sensorPath
sensorName = ClientData.sensorName

print("Begin")

try:
    with open(sensorPath, 'r') as f:
        tempRaw = f.read()
    tempF = round(float(tempRaw.split('\n')[1].split(' ')[-1].split('=')[1]) / 1000 * 9 / 5 + 32)
except FileNotFoundError:
    print("Error: Unable to get temperature")
    sys.exit()

print("tempF = " + str(tempF))
dataPoint = TempDataPoint(tempF, sensorName)

comm = TempComm(username, password, url)
result = comm.sendTemp(dataPoint)
if not result[0]:
    print("Error: " + result[1])

print("Finished")
