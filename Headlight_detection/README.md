# AnzenBike - Headlight detection
With the camera's wide angle view, we will apply image processing to detect car headlights in the dark. This functionality will be useful to orientate the servo motor and the lidar sensor towards the target object.

Using Raspberry Pi (type B)
Install by typing in terminal: 
- sudo pip install *package_name*

### Necessary packages to be imported
** Open CV Import **
- import argparse
- import cv2
- import numpy as np

** Motor Import **
- import RPi.GPIO as GPIO
- import time
- import math
