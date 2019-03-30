#!/usr/bin/python3

from TempHelper import DoorDataPoint, Comm
import ClientDataDoor

from gpiozero import Button, LED
from time import sleep
import sys
import logging

def send_state_message(data_point):
    global led
    led.on()

    web_comm = Comm(ClientDataDoor.username, 
                    ClientDataDoor.password, 
                    ClientDataDoor.url)
    result = web_comm.send(data_point)
    if not result[0]:
        logging.error("Error: " + result[1])

    led.off()

def door_closed():
    logging.info("The door is closed")
    data_point = DoorDataPoint("C")
    send_state_message(data_point)

def door_opened():
    logging.info("The door is open")
    data_point = DoorDataPoint("O")
    send_state_message(data_point)


# Setup logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename=ClientDataDoor.log_file)

# Define GPIO objects
led = LED(ClientDataDoor.led_gpio)
door_sensor = Button(ClientDataDoor.button_gpio)

# Define event triggers
door_sensor.when_pressed = door_closed
door_sensor.when_released = door_opened

logging.info("### Starting ###")

while True:
    if door_sensor.is_pressed:
        door_closed()
    else:
        door_opened()
    sleep(ClientDataDoor.send_interval)
