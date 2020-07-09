import RPi.GPIO as GPIO
import spidev
import math

GPIO.setwarnings(False)

spi = spidev.SpiDev()
spi.open(0,0)

#Set GPIO pin numbering
GPIO.setmode(GPIO.BCM)

#Right 10cm sensor
GPIO.setup(18, GPIO.IN)

#Left 10cm Sensor
GPIO.setup(6, GPIO.IN)

#Right 5cm Sensor
GPIO.setup(5, GPIO.IN)

#Left 5cm Sensor
GPIO.setup(14, GPIO.IN)

#Front 10cm Sensor
GPIO.setup(15, GPIO.IN)

''' Sensor functions with comprehensive names for a more intuitive invocation '''
def frontWall():
	if GPIO.input(15) == 1:
		return False
	else: 
		return True

def right5Wall():
	if GPIO.input(5) == 1:
		return False
	else: 
		return True

def right10Wall():
	if GPIO.input(18) == 1:
		return False
	else: 
		return True

def left5Wall():
	if GPIO.input(14) == 1:
		return False
	else: 
		return True

def left10Wall():
	if GPIO.input(6) == 1:
		return False
	else: 
		return True
		
''' Taking analog sensors' raw values '''
def analogInput(channel):
	spi.max_speed_hz = 1350000
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data
	
''' Convert raw values into volts '''
def ConvertVolts(data):
	volts = (data*3.3)/float(1023)
	return volts
	
''' Convert volts into centimeters using formulas obtained through experiments with the analog sensors' outputs '''
def ConvertCentimetersL(volts):
	distance = 10.787*volts*volts*volts*volts*volts*volts - 78.596*volts*volts*volts*volts*volts + 233.55*volts*volts*volts*volts
	distance += -366.31*volts*volts*volts + 328.88*volts*volts - 172.83*volts + 51.625
	return distance
def ConvertCentimetersR(volts):
	distance = -27.839*volts*volts*volts*volts*volts*volts + 199.87*volts*volts*volts*volts*volts - 563.69*volts*volts*volts*volts
	distance += 772.73*volts*volts*volts - 495.49*volts*volts + 85.024*volts + 36.783
	return distance

''' - Process of removing outliers, and taking the average out of multiple data points.
	- This is to keep the centimeter output consistent since the sensors tend to produce numbers with 
	large differences from the average.
	- Consistency is achieved by generating multiple data points. The amount depends on how much accuracy and
	how much speed is needed at the moment of invocation. More accuracy ==>> Slower speed
	- The standard deviation is then calculated. Any data that is outside of two deviations range is removed
	from the final average calculation.
'''

def leftAnalog(numData):
	return inputProcessing(numData, 0)
	
def rightAnalog(numData):
	return inputProcessing(numData, 1)

def inputProcessing(numData, channel):
	dataSet = []
	total = 0
	for i in range(numData):
		inputData = ConvertVolts(analogInput(channel))
		dataSet.append(inputData)
		total += inputData
	mean = total/numData
	
	stdevSum = 0
	for i in range(numData):
		stdevSum += (dataSet[i] - mean)*(dataSet[i] - mean)
	stdev = math.sqrt(stdevSum/numData)
	margin = 2*stdev
	
	temp = numData
	for i in range(temp):
		if abs(dataSet[i] - mean) > margin:
			total -= dataSet[i]
			numData -= 1
	finalVoltage = total/numData
	if channel == 0:
		distance = ConvertCentimetersL(finalVoltage)
	else:
		distance = ConvertCentimetersR(finalVoltage)
	return distance
