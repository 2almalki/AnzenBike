# import RPi.GPIO module
import RPi.GPIO as GPIO
# for use in delay
from time import sleep

# set GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)
z1_pin = 24
z2_pin = 25
z3_pin = 26
delay = 0.5

# set up output GPIO pins
GPIO.setup(z1_pin, GPIO.OUT)
GPIO.setup(z2_pin, GPIO.OUT)
GPIO.setup(z3_pin, GPIO.OUT)

try:
    while True:
        # simulates a car in z1, z2, z3 with half second
        # delay between transitioning into each zone
        # car in zone 1
        GPIO.output(z1_pin, 1)
        GPIO.output(z2_pin, 0)
        GPIO.output(z3_pin, 0)
        sleep(delay)
        # car in zone 2
        GPIO.output(z1_pin, 0)
        GPIO.output(z2_pin, 1)
        GPIO.output(z3_pin, 0)
        sleep(delay)
        # car in zone 3
        GPIO.output(z1_pin, 0)
        GPIO.output(z2_pin, 0)
        GPIO.output(z3_pin, 1)
        sleep(delay)

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()                 # resets all GPIO ports used by this program