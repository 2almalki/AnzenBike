import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)

# Create a PWM control object
# 12 is the ouput pin
# 50 is the cycke frequency in Hertz
frequencyHertz=50
pwm = GPIO.PWM(12, frequencyHertz)


nextPos =''
quit = 'q'
quitLoop = False;

# Setting the position
offset = 1
center = 1.5
left = center-offset
right = center+offset

# Position Cycle
positionCycle = [left, center, right, center]


msPerCycle = 1000 / frequencyHertz

while True:

	for position in positionCycle:
		while ~quitLoop:

			userInput = raw_input("Press enter to go to the next position: ")
			if nextPos == userInput.lower():
				break
			elif userInput.lower() == quit:
				quitLoop = true;
				break

			# if the 'n' key is pressed, move the motor to next position
			#if 0xFF == ord("n"):
				#break


		# if position == center:
		# 	time.sleep(.7)
		dutyCyclepercentage = position * 100 / msPerCycle
		print "Position: " + str(position)
		print "Duty Cycle: " + str(dutyCyclepercentage) + "%"
		print ""
		pwm.start(dutyCyclepercentage)
		# time.sleep(.2)

		if quitLoop:
			break

	if quitLoop:
		break
	

	# if the 'q' key is pressed, stop the loop
	if 0xFF == ord("q"):
		break

pwm.stop()

GPIO.cleanup()

