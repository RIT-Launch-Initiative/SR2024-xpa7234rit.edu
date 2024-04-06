import os, math, time
from gpiozero import InputDevice
import csv
import adafruit_lps2x
import board

# thermistor script

# implement lookup table

# init constants
SAMPLE_INTERVAL: float = .1 # how often data is sampled (seconds)
ROLLING_AVERAGE_DURATION: float = 10 # number of seconds of data to average
TEMP_UPPER_LIMIT: float = 200 # temp at which the heater should be turned off (celsius)
TEMP_LOWER_LIMIT: float = 180 # temp at which the heater should be turned on (celsius)
ALTITUDE_DISREEF: float = 1500 # altitude to start melting the wire (ft)
ROLLING_AVERAGE_SAMPLES: int = math.ceil(ROLLING_AVERAGE_DURATION / SAMPLE_INTERVAL) # number of samples to average

# init gpio, i2c
apogee_detect = InputDevice(4) # gpio pin to detect apogee from quark
heater = OutputDevice(6) # gpio pin to activate heater
# TODO: choose correct gpio pin for thermister and correct inputdevice
thermistor = InputDevice(7) # gpio pin to read thermister
i2c = board.I2C() # i2c connection to read accelerometer data from icm 20649
#icm = adafruit_icm20x.ICM20649(i2c) # accelerometer object
lps = adafruit_lps2x.LPS25(i2c) # barometer / altimeter object


# init variables
#sample_data=[apogeeAltitude]*ROLLING_AVERAGE_SAMPLES # set all altitude samples to the apogee altitude initially
#oldestDataIndex = 0

# wait for boost
# while(not IMU_read() or not quark_read()):
#   time.sleep(sampleTimeDelay)

# redundant check for boost
# wait for apogee
while(not apogee_detect.is_active): # wait until quark sends apogee signal
  time.sleep(SAMPLE_INTERVAL)

# apoogee reached

current_altitude = lps.altitude # get altitude from lps sensor

# descent, but not disreefing yet
# start warming up heater
while(current_altitude > ALTITUDE_DISREEF): # while we are above the disreef altitude
    # read thermister
    voltage = thermistor.value # read voltage from thermister
    # TODO: convert voltage to temperature
    temp = temp(voltage) # convert voltage to temp via lookup table

    # check if we need to turn on or off the heater
    # by trying to maintain a temperature range
    if(temp < TEMP_LOWER_LIMIT):
        heater.on() # turn on heater 
    if(temp > TEMP_UPPER_LIMIT):
        heater.off() # turn off heater
    time.sleep(SAMPLE_INTERVAL)
    # update altitude for next iteration
    current_altitude = lps.altitude

# disreefing altitude reached
heater.on() # turn on heater fully
# wait for deployment
time.sleep(20)
heater.off() # turn off heater
