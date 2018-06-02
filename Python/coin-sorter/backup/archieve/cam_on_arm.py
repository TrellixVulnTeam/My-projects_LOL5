import cv2
import sys
import numpy as np

from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *

#Initializing opencv and camera
font = cv2.FONT_HERSHEY_SIMPLEX

#Initializing UARM
swift = SwiftAPI()
sleep(3)
swift.set_buzzer()
swift.flush_cmd()

side ="center"

# UARM function
def armmove(x, y):
   
   print("Comment to arm")
   print(x,y)

   swift.set_position(x, y, 70, 60, relative=False, wait=True)
   sleep(1)

   swift.set_position(x, y, 40, 60, relative=False, wait=True)
   sleep(1)

   swift.set_pump(True)
   sleep(1)

   swift.set_position(x, y, 70, 60, relative=False, wait=True)
   sleep(1)

   swift.set_position(-20, 150, 55, 60, relative=False, wait=True)
   sleep(1)

   swift.set_pump(False)
   sleep(1)
   swift.set_position(-20, 150, 75, 60, relative=False, wait=True)

   sleep(1)
   #main()
   return;


# Detect coin function
def coindetectfunction(filename):
    print("coindetectfunction")
    cam_coin_cor = []
    #filename ="/img/2018-04-06-122050.jpg"
    #src = cv2.imread(filename, cv2.IMREAD_COLOR)
    src =filename
    if src is None:
        print ('Error opening image!')
        return -1
     
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)    
    gray = cv2.medianBlur(gray, 5)
        
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=1, maxRadius=100)
       
    if circles is not None:
        j=0
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            
            Y = (320-i[0])*0.264583
            X = (240-i[1])*0.264583

            X = 110 + X
            Y = -5 - Y

            cam_coin_cor.append([X,Y])
            center = (i[0], i[1])
            cv2.circle(src, center, 1, (0, 100, 100), 3)
            radius = i[2]
            cv2.circle(src, center, radius, (255, 0, 255), 2)

            cor = str(int(cam_coin_cor[j][0]))+","+str(int(cam_coin_cor[j][1]))         
            cv2.putText(src, cor ,(i[0], i[1]), font, 0.5,(120,0,0),1,cv2.LINE_AA)
            j = j+1

        cv2.putText(src, "320,240" ,(320,240), font, 0.5,(120,0,0),1,cv2.LINE_AA)
        cv2.circle(src, (320,240), 1, (255, 0, 255), 2)
        print(cam_coin_cor)


        for ll in cam_coin_cor:
            if(ll[0] > 100 ):
               print(ll[0])
               armmove(ll[0]+15,ll[1])

    else:
        global side
        print("in cir")
        if( side == "center"):
    
            side = "right"
            swift.set_position(150, -150, 250, 60, relative=False, wait=True)
            sleep(1)
            main()
        
        elif(side =="right"):
    
            side = "left"
            swift.set_position(150, 150, 250, 60, relative=False, wait=True)
            sleep(1)            
            main()
    
        else:
    
            side = "center"
            swift.set_position(150, 0, 250, 60, relative=False, wait=True)
            sleep(1)            
            main()

    cv2.imshow("detected circles", src)
    cv2.waitKey(0)
    
    return 0

def main():
   camera = cv2.VideoCapture(1)
   retval, frame = camera.read()
   sleep(1)
   #camera = cv2.VideoCapture(1)
   #frame = capturimg()
   camera.release()
   cv2.destroyAllWindows()
   
   coindetectfunction(frame)


swift.set_position(150, 0, 250, 60, relative=False, wait=True)
sleep(1)

main()


