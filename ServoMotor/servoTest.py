import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

# Create a PWM control object
# 11 is the ouput pin
# 50 is the cycke frequency in Hertz
frequencyHertz=150
pwm = GPIO.PWM(11, frequencyHertz)


# Setting the position
left = 1.1
right = 1.9
center = 1.5

# Position Cycle
positionCycle = [left, right]


msPerCycle = 1000 / frequencyHertz

while True:

	for position in positionCycle:
		if position == center:
			time.sleep(2.7)
		dutyCyclepercentage = position * 100 / msPerCycle
		print "Position: " + str(position)
		print "Duty Cycle: " + str(dutyCyclepercentage) + "%"
		print ""
		pwm.start(dutyCyclepercentage)
		time.sleep(1.5)

pwm.stop()

GPIO.cleanup()
