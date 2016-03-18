# AnzenBike
Safety Bike System

Each folder represents a step in the project. 
These steps will be combined into one project at the end. 
This ensures that each step will be tested independantly before everything gets intergrated together.

## Pin Layout
- Vibrating motor: PIN 18, GPIO 24
- Ultrasonic Sensor: PIN 10, GPIO 15
- Motor (Lidar): PIN 11, GPIO 17
- LIDAR:
  * SDA: PIN 3, GPIO 2
  * SCL: PIN 5, GPIO 3
- Zone indicator:
  * Red (Zone 3):			PIN 13, GPIO 27 
  * Yellow (Zone 2):		PIN 16, GPIO 23
  * Green (Zone 1):			PIN 18, GPIO 24
- LED Tailight: 		  PIN  33, GPIO 13
- Laser Lane: 			  PIN  35, GPIO 19

### Necessary packages to be imported
Using Raspberry Pi (type B)
Install by typing in terminal: 
- sudo pip install *package_name*

** Open CV Import **
- Install Open CV using this [guide](http://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/)
- import argparse
- import numpy as np

** Motor Import **
- import RPi.GPIO as GPIO
- import time
- import math
