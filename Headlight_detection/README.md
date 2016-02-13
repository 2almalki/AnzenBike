# AnzenBike - Headlight detection
With the camera's wide angle view, we will apply image processing to detect car headlights in the dark. This functionality will be useful to orientate the servo motor and the lidar sensor towards the target object.

Use Raspberry Pi (type B)

### Necessary packages to be imported
import numpy as np
** Open CV Import
- import argparse
- import cv2
- import numpy as np

** Motor Import
- import RPi.GPIO as GPIO
- import time
- import math