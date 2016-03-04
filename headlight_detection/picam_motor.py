# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera

import argparse
import cv2
import numpy as np
# Motor Import
import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setwarnings(False)
frequencyHertz=10
pwm = GPIO.PWM(11, frequencyHertz)
msPerCycle = 1000 / frequencyHertz

frameWidth = 320
frameHeight = 240

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
	# initialize the camera and grab a reference to the raw camera capture
	camera = PiCamera()
	camera.resolution = (frameWidth, frameHeight)
	camera.framerate = 5
	rawCapture = PiRGBArray(camera, size=(frameWidth, frameHeight))
	# allow the camera to warmup
	time.sleep(0.1)


# otherwise, load the video
else:
	camera = cv2.VideoCapture(args["video"])


## Function that removes all unwanted colors defined in the boundaries list from image
def removeUnwantedColor(originalImage,updateImage):
	"""Returns the original image without the unwanted colors"""
	
	# Define list of colors boundaries	
	boundaries = [	# Define all unwanted colors here
			([0,60,190],[190,190,255]),			# Red
			([170,150,0],[255,255,190]), 		# Green
			# ([85,170,210],[225,235,235]), 	# Yellow
			
			# Color White needs to be define here
			([245,245,245],[255,255,255])]	# White

	blurredImage = cv2.GaussianBlur(originalImage, (7, 7), 0)

	# Loop over the boundaries and eliminate the unwanted colors
	for (lower, upper) in boundaries[:-1]:
		# create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
		upper = np.array(upper, dtype = "uint8")

		# Find the colors within the specified boundaries and apply the mask
		mask = cv2.inRange(blurredImage, lower, upper)

		# Isolation of unwanted color
		unwantedColor = cv2.bitwise_and(originalImage, blurredImage, mask = mask)
		# grayscaleImage = cv2.cvtColor(unwantedColor, cv2.COLOR_BGR2GRAY)
		invert = cv2.bitwise_not(unwantedColor)

		updateImage = cv2.bitwise_and(updateImage, invert)
	return updateImage
	## end removeUnwantedColor



## Analyzing the picture's histogram
def getHistData(originalImage):
	"""Obtaining useful informations from the frame's histogram"""
	numOfBin = 32
	hist = cv2.calcHist([originalImage], [0], None, [numOfBin], [0, 256])
		
	# Get maxBinNum and maxPixel from grayscale histogram
	maxBinNum = 0
	maxPixel = 0
	threshPt = 240
	for x in range (0,len(hist)):
		if hist[x] > maxPixel:
			maxBinNum = x
			maxPixel = hist[x]
	
	# Set the optimal threshold value
	if maxBinNum <= 10:
		threshPt = maxBinNum * 14 + 75
	else:
		threshPt = 250
	return (threshPt,maxBinNum,maxPixel) 	## end getHistData
	


def getDistance(ptX,ptY,refPtX,refPtY):
	"""Returns the distance between the reference point and the target point"""
	distance = math.sqrt(math.pow((ptX-refPtX),2) + math.pow((ptY-refPtY),2))
	return distance

def getAngle(ptX,ptY,refPtX,refPtY):
	"""Returns the angle between the reference point and the target point"""
	distance = getDistance(ptX,ptY,refPtX,refPtY)
	if (ptX<=refPtX):
		rad = math.acos((refPtX-ptX)/distance)
	elif (ptX>refPtX):
		rad = math.asin((ptX-refPtX)/distance)+(math.pi/2)
	
	angle = (rad * 180) / math.pi 	# Convert radian to degree
	return angle


def moveMotor(angle):
	"""Sets the position of the servo motor"""
	pwmPosition = (math.floor(angle)/90) + 0.5
	dutyCyclepercentage = pwmPosition * 100 / msPerCycle
	pwm.start(dutyCyclepercentage)
	return


# Main Program
try:
	# capture frames from the camera
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array
		
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
		
		# Reference Point - (Location of Cyclist)
		refPtX = frameWidth/2
		refPtY = frameHeight
		
		# if we are viewing a video and we did not grab a
		# frame, then we have reached the end of the video
		if args.get("video") and not grabbed:
			break
		
		updateImage = image
		updateImage = removeUnwantedColor(image,updateImage)
		imageCopy = image.copy()
		gray = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2GRAY)
		(threshPt,maxBinNum,maxPixel) = getHistData(gray)

		if (maxBinNum > 10):
			# If the camera is in a bright settings, the motor will be set to a default position
			moveMotor(90)
			cv2.imshow("Frame", frame.array)

		else:
			mask = np.zeros((frameHeight, frameWidth, 3), dtype = "uint8")
			# ## Pentagon
			pts = np.array([[mask.shape[1]*(0.35),mask.shape[0]*(0.15)],[mask.shape[1]*(0.65),mask.shape[0]*(0.15)],[mask.shape[1]*(0.985),mask.shape[0]*(0.8)],[mask.shape[1]*(0.5),mask.shape[0]*(0.985)],[mask.shape[1]*(0.015),mask.shape[0]*(0.8)]], np.int32)
			pts = pts.reshape((-1,1,2))
			cv2.fillConvexPoly(mask,pts,(255,255,255),1)
			masked = cv2.bitwise_and(image, mask)
			# cv2.imshow("Masked", thresh)
			# cv2.waitKey(0)
			gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(gray, (9, 9), 0)
			(T, thresh) = cv2.threshold(blur, threshPt, 255, cv2.THRESH_BINARY)

			canny = cv2.Canny(thresh, 120, 170)
			(cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			whiteLight = image.copy()
			cv2.drawContours(whiteLight, cnts, -1, (0, 255, 0), 2)
			
			nearX = 0;
			nearY = 0;
			nearW = 0;
			nearH = 0;
			nearDistance = 5000
			
			for (i, c) in enumerate(cnts):
				(x, y, w, h) = cv2.boundingRect(c)
				distance = getDistance((x+w/2),(y+h/2),refPtX,refPtY)
				if ((y+h/2)>nearY):
					nearX = x
					nearY = y
					nearW = w
					nearH = h
					nearDistance = distance

				lightSource = image[y:y + h, x:x + w]

			if (nearX>0 or nearY>0) and nearDistance>10:
				cv2.rectangle(image,(nearX,nearY),(nearX+nearW,nearY+nearH),(0,255,0),2)
				cv2.line(image,(nearX+nearW/2,nearY+nearH),(refPtX,refPtY),(0,255,0))
				moveMotor(getAngle((nearX+nearW/2),(nearY+nearH/2),refPtX,refPtY))
			# frame = cv2.bitwise_and(frame, mask)
			cv2.imshow("Canny", canny)
			cv2.imshow("Frame", image)
			cv2.imshow("Gray", gray)
			cv2.imshow("Thresh", thresh)
			
		# if the 'q' key is pressed, stop the loop
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

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
	camera.release()
	cv2.destroyAllWindows()
	pwm.stop()
