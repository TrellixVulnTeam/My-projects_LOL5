#! /usr/bin/env python3
import sys,os
from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
import numpy as np
import cv2


sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

 # default speed for arm

def findarmpoint():

    camera = cv2.VideoCapture(1)
    retval, img = camera.read() 
    camera.release()
    cv2.destroyAllWindows()

    green = [(82, 123, 175),(102, 143, 255)] #upper lower range for green color
    green1=   [(60, 148, 205), (96, 168, 285)]

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
                                   minRadius=0,maxRadius=60)    
        index = 0
        if circles is not None:

            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:

                cv2.circle(output, (x, y), r, (255, 0, 255), 1)

                print ( "(x,y) = " + str(x) + ', ' + str(y))
                armpoint = [x,y]
            cv2.imshow("final",output)
            cv2.waitKey(0)
            
            arm_X = 100 - ((x - 165.5) / 1.2)
            print("ARM Y Value ====> "+str(arm_X))
            arm_Y = 350 - ((y - 66.5) / 1.2)
            print("ARM X Value ====> "+str(arm_Y))




# Restting arm position
def reset():
   speed = 30
   x= 0
   y = 300
   X =x
   Y = y

   # print("Moving to the position")
   # print(x,y)
   # X = 2 + (1.003 * x) + (0.018 * y)
   # Y = 0.46667- (0.02267 * x) + (1.046 * y)
   # Z = 53.53 - (0.03667 * x )
   # print(X,Y)

   swift.set_position(X,Y,50,speed,relative=False,wait=True)
   sleep(1)

   swift.set_position(X-100,Y-50,50,speed,relative=False,wait=True)
   sleep(1)
   
   

   # swift.set_position(X,Y+100,100,speed,relative=False,wait=True)
   # sleep(1)

   # swift.set_position(X -40 ,Y+100 ,100,speed,relative=False,wait=True)
   # sleep(1)

   # swift.set_position(X +50, Y +200 ,100,speed,relative=False,wait=True)
   # sleep(1)

   #findarmpoint()


   swift.set_position(X,Y,48,90,relative=False,wait=True)
   sleep(5)
   swift.set_position(X,Y,70,speed,relative=False,wait=True)
   


def picQuarter(x,y):
    
   print("PIC QUARTER$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
   print(x ,y)
   print("Moving to the position")
   swift.set_position(x, y, 70, 60, relative=False, wait=True)
   sleep(1)
   print("Moving head")
   swift.set_position(x, y, 50, 60, relative=False, wait=True)
   sleep(1)
   print("Pump on")
   swift.set_pump(True)
   sleep(1)
   print("Move head up")
   swift.set_position(x, y, 70, 60, relative=False, wait=True)
   sleep(1)
   swift.set_position(-20, 150, 55, 60, relative=False, wait=True)
   sleep(1)
   print("Pump off")
   swift.set_pump(False)
   swift.set_position(-20, 150, 75, 60, relative=False, wait=True)
   sleep(1)
   return;



# INITIALIZING 
swift = SwiftAPI()
sleep(3)
swift.set_buzzer()
swift.flush_cmd()


#Moves the robot to position
# x = 0
# y= -300

#picQuarter(x,y)
reset()

