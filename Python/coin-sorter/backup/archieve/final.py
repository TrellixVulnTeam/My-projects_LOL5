import sys
import cv2
import numpy as np
import time
import math


############ UARM #########

import os
from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

speed = 20 # default speed for arm

# Restting arm position
# def reset(ispump):
# 	swift.set_position(150,0,150,speed,relative=False,wait=True) #Moves the Robot Arm to pos(150,0,150) i.e. Reset position
# 	sleep(1)

# 	swift.set_pump(ispump)			
# 	pos=swift.get_position()	

# #Moves the robot to position
# def setposition(ax,ay,az,ispump):
# 	mov_status = swift.set_position(ax , ay, az, speed, relative=False, wait=True)
# 	sleep(1)

# 	if(mov_status == True):
# 		pos=swift.get_position()
# 		swift.set_pump(ispump)
# 		sleep(1)				
# 		reset(not ispump)
# 	else:
# 		print("Robot Arm movement Unavailable.Kindly give valid coordinates")

swift = SwiftAPI()
swift.set_buzzer()
swift.flush_cmd() #Flushes the UARM buffer and makes it empty

def picQuarter(x,y):
   #sleep(3)
    
   #pos = swift.get_position() #Gets the current position of UARM 
   print("PIC QUARTER$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
   print(x)
   print(y)
   print("Moving to the position")
   
   swift.set_position(x, y, 70, 60, relative=False, wait=True)
   sleep(1)
   print("Moving head")
   
   swift.set_position(x, y, 40, 60, relative=False, wait=True)
   sleep(1)
   print("Pump on")
   swift.set_pump(True)
   sleep(1)
   
   print("Move head up")
   swift.set_position(x, y, 70, 60, relative=False, wait=True)
   sleep(1)
   
   swift.set_position(-20, 150, 55, 60, relative=False, wait=True)
   print("Pump off")
   sleep(1)
   
   swift.set_pump(False)
   swift.set_position(-20, 150, 75, 60, relative=False, wait=True)
   sleep(1)
   
   return;
   

# print("Current position of ARM is : {}".format(pos))
	
# setposition(x,y,z,ispump)



############ UARM #########






cap = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_SIMPLEX
reference_circle_diameter_mm = 60
px_to_mm = 3.7795275590551
reference_circle_diameter =  reference_circle_diameter_mm * px_to_mm #210 # pixel

#ref_circ_posi = [400,350] 
big_circle_position  = []
flag=True

def camera():
    biggest = 0
    big_X = 0
    big_Y = 0
    coinCount=0
        
    while True:
        print(coinCount)
        
        print("Camera Enabled")
        coord_lists = []

        lists = []
        result = []
        copper  = []
        coin_coord = []
        armcor =[]

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        rows = gray.shape[0]

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                   param1=100, param2=30,
                                   minRadius=1, maxRadius=100)

        if circles is not None:
            print("Found circles")
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                print("Circle => "+ str(i))
                center = (i[0], i[1])

                cv2.circle(frame, center, 1, (0, 100, 100), 3)
                radius = i[2]
                cv2.circle(frame, center, radius, (255, 0, 255), 1)

                if (radius > biggest):
                    biggest = radius 
                    biggestdia =radius *2

                    if(big_X == 0):
                        big_X =i[0]
                        big_Y =i[1]

                        big_circle_position = [ 400/big_X , 350/big_Y ]
                        print("STTTTT")
                        sleep(5)
                        print("reduming...")
                    
                lists.append(radius*2)
                               
                refX =  i[0]*big_circle_position[0]
                
                Y = refX
                #if(Y <= 300 ):
                Y = Y - 300
                X = i[1]*big_circle_position[1]
                z = 45
                ispump =True
                if(coinCount >0 ):
                   picQuarter(X , Y)

                print("Preparing lists")
                
                armcor.append([X ,Y])
                print(armcor)
                

                cor =str(int(X))+","+str(int(Y))
                corpx =str(int(i[0]))+","+str(int(i[1]))
                cv2.putText(frame, cor ,(i[0], i[1]), font, 0.5,(120,0,0),1,cv2.LINE_AA)

                coin_coord.append([X,Y])
         
                '''pixel = image_hsv[i[1],i[0]]

                lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

                if(lower[0] < 15 or lower[1] >80):
                    copper.append(True)
                else:
                    copper.append(False)'''
                copper.append(False)    
                cv2.circle(frame, center, radius, (255, 0, 255), 2)

        #if(flag):
            #for li in lists:
                #result.append(((li)/(biggestdia*2) * reference_circle_diameter)/px_to_mm)
            # robot(sorted(result, reverse=True))
            #skip_big= coin_coord
            #print(skip_big)
            #robot(result,copper,skip_big,frame)
        
        cv2.imshow("Output", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()  
            break
        print(coinCount)	
        
        # if( coinCount > 0 ):
        #     for  x in armcor:
        #         if(x[0] < 300):
        #            print("Running the arm")
        #            picQuarter(x[0],x[1]) 
        #            #sleep(2)
        #            print(x[0],x[1])       
        coinCount = coinCount +1  
        #break    

def robot(result,copper ,coin_coord,frame):
    print(coin_coord)
    flag=False
    sum = 0
    coins =[]
    for i in range(0,len(result)):
        if math.isclose(result[i], 24.26, abs_tol=2.25):
            sum += 25
            print("25 cente")
            coins.append("25c")
        elif math.isclose(result[i], 21.21, abs_tol=1.25): 
            sum += 5
            print("5 cente")
            coins.append("5c")        
        elif math.isclose(result[i], 19.05, abs_tol=1.50) and copper[i]: 
            sum += 1
            print("1 cente")
            coins.append("1c")
        elif math.isclose(result[i], 17.91, abs_tol=1.50) and not copper[i]:
            sum += 10
            print("10 cente")
            coins.append("1c")
        #print(result[i])
    print("total sum :"+str(sum))
    # for i in range(0,len(coins)):
    # 	cv2.putText(frame, coins[i] ,(100,100), font, 0.5,(120,0,0),1,cv2.LINE_AA)

    # camera()
    #time.sleep(1)
    
    flag=True
    i=0
    lists=[]

camera()



