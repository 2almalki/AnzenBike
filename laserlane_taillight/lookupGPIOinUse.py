# import RPi.GPIO module
import RPi.GPIO as GPIO
import time

# set pins corresponding to each Zone
pin_in_lidar_z1 = 22
pin_in_lidar_z2 = 16
pin_in_lidar_z3 = 12
pin_out_LED = 3
pin_out_LASER = 5

# set GPIO mode
GPIO.setmode(GPIO.BOARD)
# set pins as input in order to read status
GPIO.setup(pin_in_lidar_z1,GPIO.IN)
GPIO.setup(pin_in_lidar_z2,GPIO.IN)
GPIO.setup(pin_in_lidar_z3,GPIO.IN)
# output LED and Laser
GPIO.setup(pin_out_LED,GPIO.OUT)
GPIO.setup(pin_out_LASER,GPIO.OUT)

# variables
flash_speed = 0

# function to find which zone is active
def closest_zone():
    # TODO: implement logging instead of print
    if GPIO.input(pin_in_lidar_z3):
        # something detected in Z3
        print "\nZone 3 - detected"
        return 0.125
    elif GPIO.input(pin_in_lidar_z2):
        # nothing detected in Z3, something detected in Z2
        print "\nZone 2 - detected"
        return 0.17
    elif GPIO.input(pin_in_lidar_z1):
         # nothing detected in Z3,Z2, something detected in Z1
         print "\nZone 1 - detected"
         return 0.25
    else:
        print "\nNothing detected"
        return 0

try:
    # main loop
    while True:
        flash_speed = closest_zone()  # update to the most recent zone detectd

        # turn on LED / Laser
        if flash_speed < 0.25: #in z2,3
            GPIO.output(pin_out_LED, True)
            GPIO.output(pin_out_LASER,True)
        else:
            GPIO.output(pin_out_LED, True)
            GPIO.output(pin_out_LASER,False)

        time.sleep(flash_speed)

        #turn off laser/taillight
        GPIO.output(pin_out_LED, False)
        GPIO.output(pin_out_LASER,False)

        time.sleep(flash_speed)

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
    GPIO.cleanup() # clean exit
