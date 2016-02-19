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
  * SDA: GPIO 02
  * SCL: GPIO 03
- Zone indicator:
  * Red (Zone 3): PIN 29, GPIO 05
  * Yellow (Zone 2): PIN 31, GPIO 06
  * Green (Zone 1): PIN 33, GPIO 13
- LED Tailight: PIN 7 , GPIO 04
- Laser Lane: PIN 36 , GPIO 16

### Necessary packages to be imported
Using Raspberry Pi (type B)
Install by typing in terminal: 
- sudo pip install *package_name*

** Open CV Import **
- import argparse
- import cv2
- import numpy as np

** Motor Import **
- import RPi.GPIO as GPIO
- import time
- import math
