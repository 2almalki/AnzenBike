# import the necessary packages
import argparse
import cv2
import numpy as np
# Motor Import
import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12,GPIO.OUT)
frequencyHertz=50
pwm = GPIO.PWM(12, frequencyHertz)
msPerCycle = 1000 / frequencyHertz

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help = "path to the (optional) video file")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])


## Function that removes all unwanted colors defined in the boundaries list from image
def removeUnwantedColor(originalImage,updateImage):
    # Define list of colors boundaries
    
    boundaries = [  # Define all unwanted colors here
            ([0,60,190],[190,190,255]),     # Red
            ([170,150,0],[255,255,190]),    # Green
            ([85,170,210],[225,235,235]),   # Yellow
            
            # Color White needs to be define here
            ([245,245,245],[255,255,255])]  # White

    blurredImage = cv2.GaussianBlur(originalImage, (7, 7), 0)

    # Loop over the boundaries and eliminate the unwanted colors
    for (lower, upper) in boundaries[:-1]:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        # Find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(blurredImage, lower, upper)

        # Isolation of unwanted color
        unwantedColor = cv2.bitwise_and(originalImage, blurredImage, mask = mask)
        unwantedColor = cv2.GaussianBlur(unwantedColor, (3, 3), 0)
        grayscaleImage = cv2.cvtColor(unwantedColor, cv2.COLOR_BGR2GRAY)
        # invert = cv2.bitwise_not(grayscaleImage)
        invert = cv2.bitwise_not(unwantedColor)

        # updateImage = cv2.bitwise_and(updateImage, invert)
        updateImage = cv2.bitwise_and(updateImage, invert)

    return updateImage
    ## end removeUnwantedColor



## Analyzing the picture's histogram
def getHistData(originalImage):
    numOfBin = 32
    hist = cv2.calcHist([originalImage], [0], None, [numOfBin], [0, 256])
    # hist = np.bincount(image.ravel(),minlength=256)
    
    # Print out the histogram values
    # print hist," \n",len(hist)
    
    # Get maxBinNum and maxPixel from grayscale histogram
    maxBinNum = 0
    maxPixel = 0
    threshPt = 240
    for x in range (0,len(hist)):
        # print(x,") ",hist[x])
        if hist[x] > maxPixel:
            maxBinNum = x
            maxPixel = hist[x]
    
    # print "Most Pixels are in bin",maxBinNum
    # print hist[maxBinNum]
    
    # Set the optimal threshold value
    if maxBinNum <= 10:
        threshPt = maxBinNum * 14 + 135
    else:
        threshPt = 250
    
    # print ("threshPt = " ,threshPt)

    return (threshPt,maxBinNum,maxPixel)
    ## end getHistData


def getDistance(ptX,ptY,refPtX,refPtY):
    distance = math.sqrt(math.pow((ptX-refPtX),2) + math.pow((ptY-refPtY),2))
    return distance

def getAngle(ptX,ptY,refPtX,refPtY):
    distance = getDistance(ptX,ptY,refPtX,refPtY)
    if (ptX<=refPtX):
        rad = math.acos((refPtX-ptX)/distance)
    elif (ptX>refPtX):
        rad = math.asin((ptX-refPtX)/distance)+(math.pi/2)

    # Convert radian to degree
    angle = (rad * 180) / math.pi

    return angle


def moveMotor(angle):

    position = (math.floor(angle)/90) + 0.5
    dutyCyclepercentage = position * 100 / msPerCycle
    pwm.start(dutyCyclepercentage)
    
    # print ""
    # print "position", position
    # print "Angle: ", angle
    # print "Duty Cycle: ", dutyCyclepercentage, "%"
    return


# Main Program
if __name__ == "__main__":
    # count = 10
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        
        r = 320.0 / frame.shape[1]
        dim = (320,int(frame.shape[0] * r))
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        
        # Get the frame size
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        # print "Hight:", frameHeight
        # print "Width:", frameWidth

        # Reference Point - (Location of Cyclist)
        refPtX = frameWidth/2
        refPtY = frameHeight
        # print "refPtX:",refPtX," refPtY:",refPtY
        
        # if we are viewing a video and we did not grab a
        # frame, then we have reached the end of the video
        if args.get("video") and not grabbed:
            break
        
        updateImage = frame
        image = removeUnwantedColor(frame,updateImage)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (threshPt,maxBinNum,maxPixel) = getHistData(gray)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        (T, thresh) = cv2.threshold(blur, threshPt, 255, cv2.THRESH_BINARY)
        
        mask = np.zeros((frameHeight, frameWidth, 3), dtype = "uint8")
        pts = np.array([[mask.shape[1]*(0.35),mask.shape[0]*(0.15)],[mask.shape[1]*(0.65),mask.shape[0]*(0.15)],[mask.shape[1]*(0.985),mask.shape[0]*(0.985)],[mask.shape[1]*(0.015),mask.shape[0]*(0.985)]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.fillConvexPoly(mask,pts,(255,255,255),1)
        thresh = cv2.bitwise_and(image, mask)
        cv2.imshow("Masked", thresh)
        cv2.waitKey(0)

        canny = cv2.Canny(thresh, 120, 170)
        (cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        whiteLight = frame.copy()
        cv2.drawContours(whiteLight, cnts, -1, (0, 255, 0), 2)
        
        nearX = 0;
        nearY = 0;
        nearW = 0;
        nearH = 0;
        nearDistance = 5000
        
        for (i, c) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            distance = getDistance((x+w/2),(y+h/2),refPtX,refPtY)
            if ((y+h/2)>nearY and (x>80) and (x+w)<frameWidth-80):
            # if (distance>nearDistance and (x>100) and (x+w)<frameWidth-100):
                nearX = x
                nearY = y
                nearW = w
                nearH = h
                # print "Update"
                # print x+w/2,"-",y+h/2
            lightSource = frame[y:y + h, x:x + w]
        
        if nearX>0 or nearY>0:
            cv2.rectangle(frame,(nearX,nearY),(nearX+nearW,nearY+nearH),(0,255,0),2)
            cv2.line(frame,(nearX+nearW/2,nearY+nearH),(refPtX,refPtY),(0,255,0))
            moveMotor(getAngle((nearX+nearW/2),(nearY+nearH/2),refPtX,refPtY))
        cv2.imshow("Frame", frame)
                
        # if the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
    pwm.stop()
    GPIO.cleanup()
