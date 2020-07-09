import time
import RPi.GPIO as GPIO
import FinalSensors as ss

GPIO.setwarnings(False)

#Set GPIO pin numbering
GPIO.setmode(GPIO.BCM)

#Intialize right side pins
GPIO.setup(27, GPIO.OUT) #1EN
GPIO.setup(2, GPIO.OUT)  #1A
GPIO.setup(3, GPIO.OUT)  #1B

#Initialize left side pins
GPIO.setup(22, GPIO.OUT) #2EN
GPIO.setup(4, GPIO.OUT)  #2A
GPIO.setup(17, GPIO.OUT) #2B

pwm_left = GPIO.PWM(22, 200)
pwm_right = GPIO.PWM(27,200)

pwm_left.start(40)
pwm_right.start(50)

''' Basic movements, configured for low speed, high precision '''
def move_Forward(t):
	GPIO.output(27, 1)
	GPIO.output(2, 0)
	GPIO.output(3, 1)
	GPIO.output(22, 1)
	GPIO.output(4, 1)
	GPIO.output(17, 0)
	time.sleep(t)
	GPIO.output(27, 0)
	GPIO.output(2, 0)
	GPIO.output(3, 0)
	GPIO.output(22, 0)
	GPIO.output(4, 0)
	GPIO.output(17, 0)
def move_Left(t):
	GPIO.output(27, 1)
	GPIO.output(2, 0)
	GPIO.output(3, 1)
	GPIO.output(22, 1)
	GPIO.output(4, 0)
	GPIO.output(17, 1)
	time.sleep(t)
	GPIO.output(27, 0)
	GPIO.output(2, 0)
	GPIO.output(3, 0)
	GPIO.output(22, 0)
	GPIO.output(4, 0)
	GPIO.output(17, 0)
def move_Right(t):
	GPIO.output(27, 1)
	GPIO.output(2, 1)
	GPIO.output(3, 0)
	GPIO.output(22, 1)
	GPIO.output(4, 1)
	GPIO.output(17, 0)
	time.sleep(t)
	GPIO.output(27, 0)
	GPIO.output(2, 0)
	GPIO.output(3, 0)
	GPIO.output(22, 0)
	GPIO.output(4, 0)
	GPIO.output(17, 0)
def stop():
	GPIO.output(27, 0)
	GPIO.output(2, 0)
	GPIO.output(3, 0)
	GPIO.output(22, 0)
	GPIO.output(4, 0)
	GPIO.output(17, 0)
def basic_Forward():
	GPIO.output(27, 1)
	GPIO.output(2, 0)
	GPIO.output(3, 1)
	GPIO.output(22, 1)
	GPIO.output(4, 1)
	GPIO.output(17, 0)
def basic_Left():
	GPIO.output(27, 1)
	GPIO.output(2, 0)
	GPIO.output(3, 1)
	GPIO.output(22, 1)
	GPIO.output(4, 0)
	GPIO.output(17, 1)
def basic_Right():
	GPIO.output(27, 1)
	GPIO.output(2, 1)
	GPIO.output(3, 0)
	GPIO.output(22, 1)
	GPIO.output(4, 1)
	GPIO.output(17, 0)
	
'''  - Maintain a certain distance from one of the side walls present 
	 - Allow a slow mode for navigation through turns, and a fast mode
	 for navigation in a straight line 
'''
def self_center(speed):
	stop()
	if not speed:
		if ss.right10Wall():
			if ss.right5Wall():
				move_Left(0.0003)
			else:
				move_Right(0.0003)
		elif ss.left10Wall():
			if ss.left5Wall():
				move_Right(0.0003)
			else:
				move_Left(0.0003)
	else:
		if ss.right10Wall():
			if ss.right5Wall():
				move_Left(0.0001)
			else:
				move_Right(0.0001)
		elif ss.left10Wall():
			if ss.left5Wall():
				move_Right(0.0001)
			else:
				move_Left(0.0001)
	basic_Forward()
				
"""	Move forward for an amount of time while self-center """
def go_Forward(t,speed):
	t = t/0.01
	i = 0
	while i < t:
		self_center(speed)
		time.sleep(0.01)
		self_center(speed)
		i += 1

""" A special case of go_Forward taking no time input """
def advance_Forward(speed):
	go_Forward(0.01,speed)
		
""" Move past the two wall pegs """
def skip_Forward():
	leftHit = False
	rightHit = False
	basic_Forward()
	while not leftHit or not rightHit:
		if not leftHit and ss.left10Wall():
			leftHit = True
			self_center(False)
		if not rightHit and ss.right10Wall():
			rightHit = True
			self_center(False)
	stop()
	
"""	Make a 180 turn """
def turn_180():
	if ss.left5Wall():				#turn till clear of front wall & close to hitting the wall at the end of the turn
		basic_Right()
		while ss.frontWall() or ss.left5Wall():
			pass
		stop()
		move_Left(0.02)
	else:
		basic_Left()
		while ss.frontWall() or ss.right5Wall():
			pass
		stop()
		move_Right(0.02)

		
""" Make right turn """
def advance_Right(): #one case for when there is a front wall, and another for when this is not
	if ss.frontWall():
		basic_Right()
		while ss.frontWall():
			pass
		while ss.left5Wall():
			pass
		stop()
		move_Left(0.02)
		basic_Forward()
		while not ss.right10Wall():
			pass
		stop()
	else:
		basic_Right()
		while not ss.frontWall():
			pass
		while ss.frontWall():
			pass
		while not ss.right10Wall():
			pass
		while ss.right10Wall():
			pass
		stop()
		move_Left(0.02)
		# without wall on your right (front wall before turning)
		# it will fail without this
		skip_Forward()
		
		
""" Same as advance_Right but for left """		
def advance_Left():
	if ss.frontWall():
		basic_Left()
		while ss.frontWall():
			pass
		while ss.right5Wall():
			pass
		stop()
		move_Right(0.1)
		basic_Forward()
		while not ss.left10Wall():
			pass
		stop()
	else:
		basic_Left()
		while not ss.frontWall():
			pass
		while ss.frontWall():
			pass
		while not ss.left10Wall():
			pass
		while ss.left10Wall():
			pass
		stop()
		move_Right(0.1)
		#without wall on your left (front wall before turning)
		#it will fail without this
		skip_Forward()
