# Software code that checks the sensors for distance and outputs according duty cycle

import wave
import time
import serial
import string
import pygame
import subprocess
#import matplotlib
import RPi.GPIO as GPIO

import datetime as dt

count = 0;	# number of data points taken during collectin interval
max=250;	# maximum distance for motor vibration
dec = 62.5;	# decremental value for duty cycle ranges
Av = []
Ac = []
startFlag = 0; 	# starts the motor if equal to 1 and stops the motor if equal to 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Motor Setup
GPIO.setup(24, GPIO.OUT) # GPIO 24 is set to be an output.
pwm = GPIO.PWM(24, 10)   # pwm is an object to control the pins
                         # 24 is the GPIO pin number.
                         # 10 is the frequency in Hz.

GPIO.setup(18, GPIO.OUT)


#Opening the serial ports to read the ultrasonic sensors
serialPort=serial.Serial("/dev/ttyAMA0", 9600, timeout=2, stopbits=1, parity='N')

#100 readings
#while (count<1000):

previousReading = 765;

try:
    while True:

	    if serialPort.isOpen()== False:
	            serialPort.open()       
	    else: 
	            pass
	    
	    serialPort.flushInput()
	    
	    CV=serialPort.read(5)
	    
	    if(CV==""):
		CV=int("1000")
	    else:
		CV = int(CV.replace("R", "") )
	
	    serialPort.flushInput()    
	    print (CV)

	    if(CV<(previousReading-2)):
	    	GPIO.output(18,1)
			if(CV<50):
			    pwm.start(5)
			    pwm.ChangeDutyCycle(100)			
			elif(CV<100):
			    pwm.start(5)
			    pwm.ChangeDutyCycle(75)
			elif(CV<150):
			    pwm.start(5)
			    pwm.ChangeDutyCycle(50)
	    else:
	        pwm.stop()
	        GPIO.output(18,0)

	    previousReading = CV

	    #print "Distance in cm: %(distance)s" % {"distance": CV}
	    #time.ctime()
	    #time.strftime('%l:%M%p %Z on %b %d, %Y')
	    
	    #print "%(distance)s" % {"distance": CV}
	
	    #n1 = dt.datetime.now()
    	    #print n1

    #Av.append(CV)
    #Ac.append(count)
    #count = count +1

except KeyboardInterrupt:
    pwm.stop()                # Turn PWM off
    GPIO.cleanup()            # Always clean up at the end of programs.
