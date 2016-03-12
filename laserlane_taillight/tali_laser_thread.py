# import RPi.GPIO module
import RPi.GPIO as GPIO
import time
import threading
from threading import Thread

# set pins corresponding to each Zone
pin_in_lidar_z1 = 18
pin_in_lidar_z2 = 16
pin_in_lidar_z3 = 22
pin_out_LED = 33
pin_out_LASER = 35

# set GPIO mode
GPIO.setmode(GPIO.BOARD)
# set pins as input in order to read status
GPIO.setup(pin_in_lidar_z1, GPIO.IN)
GPIO.setup(pin_in_lidar_z2, GPIO.IN)
GPIO.setup(pin_in_lidar_z3, GPIO.IN)
# output LED and Laser
GPIO.setup(pin_out_LED, GPIO.OUT)
GPIO.setup(pin_out_LASER, GPIO.OUT)

# variables
flash_speed = 0


# function to find which zone is active
def closest_zone():
    # TODO: implement logging instead of print
    global flash_speed
    while True:
        if GPIO.input(pin_in_lidar_z3):
            # something detected in Z3
            # print "\nZone 3 - detected"
            flash_speed = 0.125
        elif GPIO.input(pin_in_lidar_z2):
            # nothing detected in Z3, something detected in Z2
            # print "\nZone 2 - detected"
            flash_speed = 0.17
        elif GPIO.input(pin_in_lidar_z1):
            # nothing detected in Z3,Z2, something detected in Z1
            # print "\nZone 1 - detected"
            flash_speed = 0.25
        else:
            # print "\nNothing detected"
            flash_speed = 0


def taillight_flash():
    while True:
        # turn on LED / Laser
        GPIO.output(pin_out_LED, True)
        # sleep for flash time
        time.sleep(flash_speed)
        # turn off laser/taillight
        GPIO.output(pin_out_LED, False)
        time.sleep(flash_speed)


def laser_flash():
    while True:
        # flash laser in z2, solid in z1
        if 0.15 <= flash_speed <= 0.23:
            # in z2
            GPIO.output(pin_out_LASER, True)
            time.sleep(flash_speed)
            GPIO.output(pin_out_LASER, False)
            time.sleep(flash_speed)
        elif 0.10 <= flash_speed <= 0.14:
            # in z1
            GPIO.output(pin_out_LASER, True)
        else:
            # not in z1 or z2
            GPIO.output(pin_out_LASER, False)

try:
    # main
    Thread(target=closest_zone()).start()
    Thread(target=taillight_flash()).start()
    Thread(target=laser_flash()).start()

except KeyboardInterrupt:
    # code you want to run before the program
    # exits when you press CTRL+C
    print "\n\n Keyboard interrupt detected"

# except:
    # catches ALL other exceptions including errors.
    # won't get any error messages for debugging
    # so only use it once your code is working
    # print "Other error or exception occurred!"

finally:
    print "\n Cleanup GPIO"
    GPIO.cleanup()  # clean exit
