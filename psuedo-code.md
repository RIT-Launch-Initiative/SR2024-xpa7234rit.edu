# camera script

```
//figure out how to get accelerometer data from both pi and flight computers

bufferTimer = 15 //number of seconds between buffers
sampleTimeDelay = .01 // how often we sample the sensors in seconds
bufferCounter = bufferTimer / sampleTimeDelay //how many samples before we make a new buffer
numberOfBuffers = 2
fileNumber = 1

start recording first buffer to file ("Recording" + fileNumber)
fileNumber++

while((pi accelerometer magnitude greater than 5) or (eggtimer accelerometer magnitude greater than 5))
{
  bufferCounter--
  if(bufferCounter <= 0)
  {
    stop recording newest buffer and save file to ("Recording" + fileNumber)
    
    if(fileNumber > numberOfBuffers)
    {
      delete file named "Recording" + (fileNumber - numberOfBuffers)
    }
    
    fileNumber++
    start new recording to a file named ("Recording" + fileNumber)
    bufferCounter = bufferTimer / sampleTimeDelay
  }
  time.sleep(sampleTimeDelay)
}
    
wait 15 minutes
stop recording the final file and save to (flightRecording)

```

#thermister script

```
//implement lookup table

sampleTimeDelay = .1 //how often data is sampled
sampleTimeAverage = 10 //number of seconds of data to average
upperTempLimit = ? //temp at which the heater should be turned off
lowerTempLimit = ? //temp at which the heater should be turned on
altitudeToDereefAt = 1500 //altitude to start melting the wire

numberOfSamplesToAverage = sampleTimeAverage / sampleTimeDelay
sampleData[numberOfSamplesToAverage] = {apogeeAltitude}; //set all altitude samples to the apogee altitude initially
oldestDataIndex = 0;

//on pad
while((pi accelerometer magnitude greater than 5) or (eggtimer accelerometer magnitude greater than 5))
{
  time.sleep(sampeTimeDelay)
}

//going up
hasDetectedApogee = 0
apogeeDetectPin = TBD
while(!get(apogeeDetectPin))
{
  time.sleep(sampleTimeDelay)
}



//going down but not dereefing yet
while(currentAltitude > altitudeToDereefAt)
{
  sampleData[oldestDataIndex] = current altitude from sensors
  oldestDataIndex++;
  currentAltitude = 0
  for(i = 0, i < numberOfSamples, i++)
  {
    currentAltitude += altitudeData[i] / numberOfSamples
  }

  voltage = sample(thermister)
  temp = convert voltage to temp via lookup table

  if(temp < lowerTempLimit)
  {
    turn on thermister
  }
  if(temp > upperTempLimit)
  {
    turn off thermister
  }
  time.sleep(sampleTimeDelay)
}

//dereefing
turn on thermister
time.sleep(60)
turn off thermister

```

