#!/usr/bin/env python

import os
import glob
import time
from datetime import datetime
import RPi.GPIO as GPIO
from sensors import FlowMeter, OneWireTempSensor
#from secrets import MASTER_API_KEY, DEVICE_ID
from m2x.client import M2XClient
from m2x.utils import to_iso

# Initialize M2X Client, change MASTER_API_KEY and DEVICE_ID to yours
client = M2XClient(MASTER_API_KEY)
device = client.device(DEVICE_ID)
temp_stream = device.stream('temperature')
flow_stream = device.stream('water_use')

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# With only one temp sensor connected first sensor name in the list is 
# all you need, with more you need to figure out which one you want to use
sensor_names = OneWireTempSensor.find_temp_sensors()


# Initialize One Wire Temp Sensor
tempsensor = OneWireTempSensor(sensor_names[0])

# initialize flow meter
flowmeter = FlowMeter(tempsensor)


# Set up interreupt detection and call backs
def click(channel):
    currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    if flowmeter.enabled:
        flowmeter.update(currentTime)

GPIO.add_event_detect(22, GPIO.RISING, callback=click, bouncetime=20)

try:
    while True:
        currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)

        if (flowmeter.thisFlow > 0.1 and currentTime - flowmeter.lastClick > 10000):
            postTime = to_iso(datetime.utcnow())
            flow_stream.add_value(flowmeter.getThisFlow(), postTime)
            temp_stream.add_value(flowmeter.checkTempC(), postTime)
            flowmeter.thisFlow = 0.0

except KeyboardInterrupt:
    print "Stopping faucet monitor."
finally:
    GPIO.cleanup()

