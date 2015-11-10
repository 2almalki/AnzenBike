import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)

# Create a PWM control object
# 11 is the ouput pin
# 50 is the cycke frequency in Hertz
frequencyHertz=50
pwm = GPIO.PWM(12, frequencyHertz)


# Setting the position
left = 1.3
right = 1.8
center = 1.5

# Position Cycle
positionCycle = [left, center, right, center]


msPerCycle = 1000 / frequencyHertz

while True:

	for position in positionCycle:
		if position == center:
			time.sleep(.7)
		dutyCyclepercentage = position * 100 / msPerCycle
		print "Position: " + str(position)
		print "Duty Cycle: " + str(dutyCyclepercentage) + "%"
		print ""
		pwm.start(dutyCyclepercentage)
		time.sleep(.2)

pwm.stop()

GPIO.cleanup()