# import RPi.GPIO module
import RPi.GPIO as GPIO

# set pins corresponding to each Zone
pin_in_lidar_z1 = 24
pin_in_lidar_z2 = 25
pin_in_ultra_z3 = 26

# set GPIO mode
GPIO.setmode(GPIO.BOARD)
# set pins as input in order to read status
GPIO.setup(pin_in_lidar_z1,GPIO.IN)
GPIO.setup(pin_in_lidar_z2,GPIO.IN)
GPIO.setup(pin_in_ultra_z3,GPIO.IN)

# global variable
z1 = False
z2 = False
z3 = False

try:
    # main loop
    # TODO - add taillight / laser lane implementation
    while True:
        z1 = GPIO.IN(pin_in_lidar_z1)
        z2 = GPIO.IN(pin_in_lidar_z2)
        z3 = GPIO.IN(pin_in_ultra_z3)

        if z3 == True:
            # something detected in Z3
            # do something
            print "\nZone 3 - detected"
        elif z2 == True:
            # nothing detected in Z3, something detected in Z2
            # do something
            print "\nZone 2 - detected"
        elif z3 == True:
            # nothing detected in Z3,Z2, something detected in Z1
            # do something
            print "\nZone 1 - detected"
        else:
            # nothing has been detected
            print "\nNothing detected"


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
    GPIO.cleanup() # this ensures a clean exit
