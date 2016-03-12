# import RPi.GPIO module
import RPi.GPIO as GPIO
# for use in delay
from time import sleep

# set GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)
z1_pin = 24
z2_pin = 23
z3_pin = 25
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
        print "\nZone 1 activated on GPIO: %d" %z1_pin
        sleep(delay)
        # car in zone 2
        GPIO.output(z1_pin, 0)
        GPIO.output(z2_pin, 1)
        GPIO.output(z3_pin, 0)
        print "\nZone 2 activated on GPIO: %d" %z2_pin
        sleep(delay)
        # car in zone 3
        GPIO.output(z1_pin, 0)
        GPIO.output(z2_pin, 0)
        GPIO.output(z3_pin, 1)
        print "\nZone 3 activated on GPIO: %d" %z3_pin
        sleep(delay)

# trap a CTRL+C keyboard interrupt
except KeyboardInterrupt:
    # resets all GPIO ports used by this program
    GPIO.cleanup()
