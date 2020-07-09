import RPi.GPIO as GPIO
import spidev
import math

GPIO.setwarnings(False)

spi = spidev.SpiDev()
spi.open(0, 0)

# Set GPIO pin numbering
GPIO.setmode(GPIO.BCM)

# Right 10cm sensor
GPIO.setup(18, GPIO.IN)

# Left 10cm Sensor
GPIO.setup(6, GPIO.IN)

# Right 5cm Sensor
GPIO.setup(5, GPIO.IN)

# Left 5cm Sensor
GPIO.setup(14, GPIO.IN)

# Front 10cm Sensor
GPIO.setup(15, GPIO.IN)

# Return whether there is a wall within range of the front 10cm digital sensor
def front_wall():
	if GPIO.input(15) == 1:
		return False
	else:
		return True

# Return whether there is a wall within range of the right 5cm digital sensor
def right_wall_close():
	if GPIO.input(5) == 1:
		return False
	else:
		return True

# Return whether there is a wall within range of the right 10cm digital sensor
def right_wall_far():
	if GPIO.input(18) == 1:
		return False
	else:
		return True

# Return whether there is a wall within range of the left 5cm digital sensor
def left_wall_close():
	if GPIO.input(14) == 1:
		return False
	else:
		return True

# Return whether there is a wall within range of the left 10cm digital sensor
def left_wall_far():
	if GPIO.input(6) == 1:
		return False
	else:
		return True

# Return the distance between the left analog sensor and the wall it is facing
def left_analog(num):
	return averaging_inputs(num, 0)

# Return the distance between the right analog sensor and the wall it is facing
def right_analog(num):
	return averaging_inputs(num, 1)

# Gather a user-specified number of raw inputs from a user-specified channel
# Convert them to voltages
# Eliminate the outliers which exceed two standard deviations
# Take the average of the remaining data points, convert it to centimeters
# Return the distance
#
# NOTE: more data points ==> higher accuracy ==> slower speed
def averaging_inputs(num, channel):
	data_set = []
	total = 0
	for i in range(num):
		input_data = convert_volts(analog_input(channel))
		data_set.append(input_data)
		total += input_data
	mean = total/num

	stdev_sum = 0
	for i in range(num):
		stdev_sum += (data_set[i]-mean) * (data_set[i]-mean)
	stdev = math.sqrt(stdev_sum/num)
	margin = 2*stdev

	temp = num
    for i in range(temp):
		if abs(data_set[i]-mean) > margin:
			total -= data_set[i]
			num -= 1
	if channel == 0:
		return convert_cm_left(total/num)
	else:
		return convert_cm_right(total/num)

# Convert volts into centimeters for left analog sensor using formulas
# obtained through experiments with left analog sensor outputs
def convert_cm_left(volts):
	return (
			10.787*volts*volts*volts*volts*volts*volts
			- 78.596*volts*volts*volts*volts*volts
			+ 233.55*volts*volts*volts*volts
			- 366.31*volts*volts*volts
			+ 328.88*volts*volts
			- 172.83*volts
			+ 51.625
	)

# Convert volts into centimeters for right analog sensor using formulas
# obtained through experiments with right analog sensor outputs
def convert_cm_right(volts):
	return (
			- 27.839*volts*volts*volts*volts*volts*volts
			+ 199.87*volts*volts*volts*volts*volts
			- 563.69*volts*volts*volts*volts
			+ 772.73*volts*volts*volts
			- 495.49*volts*volts
			+ 85.024*volts
			+ 36.783
	)

# Convert raw inputs into volts
def convert_volts(data):
	volts = data*3.3 / float(1023)
	return volts

# Gather raw inputs from analog sensor channels
def analog_input(channel):
	spi.max_speed_hz = 1350000
	adc = spi.xfer2([1,(8+channel) << 4, 0])
	data = ((adc[1] & 3) << 8) + adc[2]
	return data
