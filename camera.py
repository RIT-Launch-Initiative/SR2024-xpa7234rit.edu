import time
from picamera import PiCamera
from gpiozero import OutputDevice
import serial, csv
import threading
import adafruit_icm20x, board
import os, math


# camera script

# gpio 2 SDA
# gpio 3 SCL

# figure out how to get accelerometer data from both pi and flight computers

# init gpio, serial and i2c
smoke = OutputDevice(5) # gpio pin to activate smoke flare / payload
ser = serial.Serial( # serial connection to read accelerometer data from quark
    port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 9600, # TODO: determine baud rate for quark
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
i2c = board.I2C() # i2c connection to read accelerometer data from icm 20649
icm = adafruit_icm20x.ICM20649(i2c) # accelerometer object


# init constants 
BUFF_DURATION: float = 15.0 # time between buffers (seconds)
SAMPLE_INTERVAL: float = .01 # how often we sample the sensors (seconds)
BUFFER_COUNTER_MAX: int = math.ceil(BUFF_DURATION / SAMPLE_INTERVAL) # how many samples before we make a new buffer
BUFF_COUNT: int = 2 # number of buffers to keep before boost
POST_BOOST_DURATION: float = 15*60 # time to record after boost (seconds)

# init variables
buffer_counter: int = BUFFER_COUNTER_MAX # variable to decrement to 0 before making a new buffer
file_number: int = 1 # file number

# init camera
camera = PiCamera()
camera.resolution = (1024, 768) # (2592, 1944)
camera.framerate = 60

# begin recording first buffer
camera.start_recording('%d.h264'%file_number.zfill(4))

file_number+=1 # increment file number for next buffer

# wait for boost
while(not(IMU_read() and quark_read())): # if either IMU acceleration magnitude > 5, then break loop
    buffer_counter-=1 # count down to next buffer
    # when buffer_counter reaches 0, stop recording current buffer and start a new one
    if(buffer_counter <= 0):
        # stop recording current buffer and start a new buffer
        camera.split_recording('%d.h264' % file_number.zfill(4))
		# delete oldest buffer if we have more than BUFF_COUNT buffers
        if(file_number > BUFF_COUNT):
            # delete oldest buffer
            os.remove('%d.h264' % (file_number-1).zfill(4))
        file_number+=1 # increment file number for next buffer
        buffer_counter = BUFFER_COUNTER_MAX # reset buffer counter
    time.sleep(SAMPLE_INTERVAL) # wait for next sample
    
# boost detected
    
# launch smoke flare / payload
smoke.on()
    
# wait 15 minutes
camera.wait_recording(POST_BOOST_DURATION)
# stop recording the final file and save to (flightRecording)
camera.stop_recording()


