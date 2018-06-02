#SORTER.PY
#AUTHOR - MANOJ
#DATE: 16 April 2018

print("Importing libraries")
import sys
import cv2
import numpy as np
import math
import os
import imutils


from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
print("Importing libraries finished")

print("Initializing variables")
print("Setting font for the camera output")
font = cv2.FONT_HERSHEY_SIMPLEX
print("Setting blur values")
blurValue = [10,10]
print("Setting blur type, M=> median blur A=> average blur")
blurType = "A" 

calibrationCircle = [0, 0, 0]
calibrationDefaultRadius = 30  # IN MM
calibrationDefaultXRange = 350  # IN MM
calibrationDefaultYRange = 100  # IN MM
copper  = 0


#Initializing UARM
print("Started initializing UARM")
swift = SwiftAPI()
sleep(3)
swift.set_buzzer()
swift.flush_cmd()

print("Moving UARM to the default position")
swift.set_position(-20, 150, 75, 80, relative=False, wait=True)

print("Initializing variables finished")



def findarmpoint_using_circle():

    camera = cv2.VideoCapture(1)
    retval, img = camera.read() 
    camera.release()
    cv2.destroyAllWindows()

    #green = [(82, 123, 175),(102, 143, 255)] #upper lower range for green color

    green1 = [(64, 125, 195),(84, 145, 279)] 
    
    dot_colors = [green1]

    cv2.imshow("orginal",img)
    cv2.waitKey(0)

    blur= cv2.medianBlur(img, 7) 

    image_hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    for lower, upper in dot_colors:
        output = img.copy()

        mask = cv2.inRange(image_hsv,lower,upper) 

        cv2.imshow("mask",mask)
        cv2.waitKey(0)
        circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,param1=20,param2=8,
                                   minRadius=0,maxRadius=100)    
        index = 0
        if circles is not None:

            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:

                cv2.circle(output, (x, y), r, (255, 0, 255), 1)

                #print ( "(x,y) = " + str(x) + ', ' + str(y))
                armpoint = [x,y]
            cv2.imshow("final",output)
            cv2.waitKey(0)
            return armpoint



def ShapeDetector(c):
    shape = ""
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    if len(approx) == 5:
        shape = "pentagon"
    else:
        shape = "no"
    return shape


def findarmpoint():

    camera = cv2.VideoCapture(1)
    retval, img = camera.read() 
    camera.release()
    cv2.destroyAllWindows()


    resized = imutils.resize(img, width=300)
    ratio = img.shape[0] / float(resized.shape[0])

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    blurred= cv2.medianBlur(gray, 5) 

    #blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # cv2.imshow("blurred" ,blurred)
    # cv2.waitKey(0)
    thresh = cv2.threshold(blurred, 180, 245, cv2.THRESH_BINARY)[1]

    cv2.imshow("thresh" ,thresh)
    cv2.waitKey(0)


    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:

        M = cv2.moments(c)
        if(M["m00"] != 0):
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
            shape = ShapeDetector(c)

            if(shape == "pentagon"):
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                
                cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
                cv2.putText(img, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                     0.5, (255, 255, 255), 2)

                # show the output image
                cv2.imshow("Image", img)
                cv2.waitKey(0)
                armpoint = [cX, cY]
                return armpoint



def gettingCirclesFromFrame(image):
    frameWidth = image.shape[0]
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, frameWidth / 10, param1=100, param2=30, minRadius=1, maxRadius=100)
    return circles



def detectCoints(frame):
    print("Started detecting coins in the frame")
    print("Converting image to Grayscale")
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print("Image has been converted to Grayscales")

    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # cv2.imshow("image_hsv",image_hsv)
    # cv2.waitKey(0)

    global blurValue, blurType
    print("Current blur type "+ blurType)
    if(blurType == "M"):
        print("Adding median blur to the grayscale image")
        image = cv2.medianBlur(image, blurValue[0])
    elif(blurType == "A"):
        print("Adding average blur value to the grayscale image")
        image = cv2.blur(image,(blurValue[0],blurValue[1]))
        

    print("Get the frame size (H x W)")
    frameSize = image.shape
    print(frameSize)

    circles = gettingCirclesFromFrame(image)
    print("Circles coordinations [X, Y, r]")
    print(circles)
    
    global calibrationCircle
    if(calibrationCircle[0] > 0):
        print("----------------Calibration circle coordinates are [X, Y, r]")
        print(calibrationCircle)
    targetCircle =[0, 0, 0]

    for i in circles[0, :]:
        center = (i[0], i[1])

        # IF THE GLOBAL VARIABLE CALIBRATIONCIRCL VALUE IS EQUAL TO THE CURRENT CIRCLE, SKIP FROM THE CALCULATION
        if(i[2] > calibrationCircle[2]-2 and calibrationCircle[2] >0 ):
            print("Skipping calibration circle from the detection")
        else:
            
            global copper
            pixel = image_hsv[int(i[1]),int(i[0])]
            
            lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

            if(lower[0] < 15 or lower[1] >80):
                copper = 1
                print("Copper true ####################")
            else:
                copper = 0
                print("Copper False ################")
                
            targetCircle = i
            return targetCircle

        cv2.circle(image, center, 1, (0, 100, 100), 1)
        cv2.circle(image, center, i[2], (0, 100, 100), 1)
    #cv2.imshow('Frame',image)
    return targetCircle
    

def findTarget():
    print("Initializing the camera")
    print("Opening camera ID: 1 (0->Default camera 1-> External USB camera)")
    print("Capturing single frame from the camera")
    camera = cv2.VideoCapture(1)
    retval, frame = camera.read() 
    print("Show the single captured frame")
    #cv2.imshow('Frame',frame)
          
    print("Releasing CV2 memory and stop camera")
    camera.release()
    cv2.destroyAllWindows()  
    targetCircle = detectCoints(frame)
    print("The value of target circle")
    print(targetCircle)
    return targetCircle

def ratioConversion(calibrationCircle):
	calibrationRadius = calibrationCircle[2] #IN PIXEL
	ratio = calibrationRadius / calibrationDefaultRadius #PIXEL / MM
	print("The current ratio between PIXEL and MM is => "+str((ratio)))
	return ratio


def getCoinValue (dia):
    print("========================================= ")
    print(dia)

    coinValue = 0;
    if math.isclose(dia, 24.26, abs_tol=2) and copper == 0:
        coinValue = 25
        
    elif math.isclose(dia, 21.21, abs_tol=2) and copper == 0: 
        coinValue = 5
        
    elif math.isclose(dia, 19.05, abs_tol=2) and copper == 1: 
        coinValue = 1
        
    elif math.isclose(dia, 17.91, abs_tol=2) and copper == 0:
        coinValue = 10
    elif (dia < 17.91) and copper == 0:
        coinValue = 10
    return coinValue

def armmove(X, Y,toX ,toY):
   print("Comment to arm +++++++++++++++++++++++++++++++++")
   print(X ,Y)
   speed =90
   x  =  X
   y  =  Y

   print(x,y)
 

   swift.set_position(x, y, 100, speed, relative=False, wait=True)
   pos = swift.get_position()
   sleep(1)    
   
   arm_point = findarmpoint()

   print("ARM_POINT ))))))))))))))))))))))))))")


   if(arm_point):

       print (arm_point[0])
       print (arm_point[1])

       global calibrationDefaultYRange , calibrationDefaultXRange ,calibrationCircle

       convertionRatio = ratioConversion(calibrationCircle)

       arm_Y = calibrationDefaultYRange - ((arm_point[0] - calibrationCircle[0]) / convertionRatio)
       print("ARM Y Value ====> "+str(arm_Y))
       arm_X = calibrationDefaultXRange - ((arm_point[1] - calibrationCircle[1]) / convertionRatio)
       print("ARM X Value ====> "+str(arm_X))

       sleep(1)
       x = x + (x - arm_X) 
       y = y + (y - arm_Y) + 11


       print("AFTER CORRCTION ^^^^^^^^^^^^^^^^^^^^^^")
       print(x,y)


       swift.set_position(x, y, 100, 20, relative=False, wait=True)
       sleep(1)

       swift.set_position(x, y, 40, 20, relative=False, wait=True)
       sleep(1)

       swift.set_pump(True)
       sleep(1)

       swift.set_position(x, y, 70, speed, relative=False, wait=True)
       sleep(1)

       swift.set_position(toX, toY, 55, speed, relative=False, wait=True)
       sleep(1)

       swift.set_pump(False)
       sleep(1)
       swift.set_position(toX, toY, 75, speed, relative=False, wait=True)
       #TODO => After completion of the code, move runprocess to main() inside while loop
   runProcess()
   return;

def getCoinToPostion(coinValue):
    if(coinValue == 10):
        return [-20, 100]
    elif(coinValue == 1):
        return [-20, 150]
    elif (coinValue == 5):
        return [-20, 200]
    elif (coinValue == 25):
        return [-20, 250]

def armController(dia, targetX, targetY):
    coinValue = getCoinValue(dia)
    print("Detected coin value is: " + str(coinValue))
    if(coinValue <= 0):
    	print("Invalid coin value fonund")
    	return
    targetPosition = getCoinToPostion(coinValue)
    print("Target position identified: ==")
    print(targetPosition)
    armmove(targetX, targetY, targetPosition[0], targetPosition[1])


def runProcess():
    global calibrationCircle
    convertionRatio = ratioConversion(calibrationCircle)

    print("Changing the blur type and the blur value")
    print("Setting blur values")
    global blurValue, blurType
    blurValue = [11,10]
    print("Setting blur type, M=> median blur A=> average blur")
    blurType = "M" 
    targetCircle = findTarget()

    print("Started calculating coordinations in MM")
    
    targetY = calibrationDefaultYRange - ((targetCircle[0] - calibrationCircle[0]) / convertionRatio)
    print("Y Value ====> "+str(targetY))

    targetX = calibrationDefaultXRange - ((targetCircle[1] - calibrationCircle[1]) / convertionRatio)
    print("X Value ====> "+str(targetX))



    radius = targetCircle[2] / convertionRatio
    print("Radius ==> "+str(radius))

    dia = radius * 2

    print("Diameter ==> "+str(dia))

    if(radius > 0):
        print("Calling Arm controller to pick the coin")
        armController(dia, targetX, targetY)
    runProcess()

def main():
    print("Main function initiated")
    print("Calibration values at beginning")

    global calibrationCircle
    print("Finding calibration circle")
    calibrationCircle = findTarget()
    print("Calibration values are")
    print(calibrationCircle)

    print("========================= Waiting for the coins to be placed in the plane ===========================")
    sleep(2)
    runProcess()


print("Started executing main function")

main()
