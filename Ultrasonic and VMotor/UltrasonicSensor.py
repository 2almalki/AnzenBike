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

GPIO.setmode(GPIO.BCM)

#Motor Setup
GPIO.setup(24, GPIO.OUT) # GPIO 24 is set to be an output.
pwm = GPIO.PWM(24, 10)   # pwm is an object to control the pins
                         # 24 is the GPIO pin number.
                         # 10 is the frequency in Hz.
#100 readings
while (count<100):
 
    #Opening the serial ports to read the ultrasonic sensors
    serialPort=serial.Serial("/dev/ttyAMA0", 9600, timeout=2, stopbits=1, parity='N')
    if serialPort.isOpen()== False:
            serialPort.open()       
    else: 
            pass
    
    serialPort.flushInput()
    
    CV=serialPort.read(5)
    CV = int(CV.replace("R", "") )
    serialPort.flushInput()    
    print (CV)

    if(CV<30):
        pwm.start(50)
        pwm.ChangeDutyCycle(50)
    elif(CV>30):
        pwm.stop()

    #print "Distance in cm: %(distance)s" % {"distance": CV}
    #time.ctime()
    #time.strftime('%l:%M%p %Z on %b %d, %Y')
    
    #print "%(distance)s" % {"distance": CV}

    #n1 = dt.datetime.now()
    #print n1

    #Av.append(CV)
    Ac.append(count)
    count = count +1

pwm.stop()                # Turn PWM off
GPIO.cleanup()            # Always clean up at the end of programs.
