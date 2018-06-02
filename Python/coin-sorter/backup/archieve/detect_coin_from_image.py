#! /usr/bin/env python3

import sys
import cv2
import numpy as np
import math

import sys,os
from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *


font = cv2.FONT_HERSHEY_SIMPLEX
def main():

    coord_lists = []
    lists = []
    result = []
    copper  = []
    cor = []
    biggest = 0
    #reference_circle_diameterin_mm = 226.771654 #210 # pixel
    reference_circle_diameterin_mm = 24.26 # in mm
    px_to_mm = 3.7795275590551
    reference_circle_diameter = px_to_mm *reference_circle_diameterin_mm
        
    flag=True

    
    default_file =  "IMG9375.jpg"
    filename =default_file
    src = cv2.imread(filename, cv2.IMREAD_COLOR)
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1
       
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)    
    gray = cv2.medianBlur(gray, 5)  
    image_hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=50, param2=5,
                               minRadius=1, maxRadius=100)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            cv2.circle(src, center, 1, (0, 100, 100), 1)
            
            radius = i[2]
            cor.append(i)

            print(i)
            cor1= str(i[2])

            cv2.circle(src, center, radius, (255, 0, 255), 2)
            

            cv2.putText(src, cor1 ,(i[0], i[1]), font, 0.5,(120,0,0),1,cv2.LINE_AA)

            cv2.circle(src, center, radius, (255, 0, 255), 2)
            

            if (radius > biggest):
                    biggest = radius
                    biggestdia =radius*2
                    print(biggestdia)

            lists.append(radius*2)
            pixel = image_hsv[i[1],i[0]]
            lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])

            
            if(lower[0] < 15 or lower[1] >80):
                copper.append(True)
            else:
                copper.append(False)
    if(flag):
        for li in lists:
            result.append((((li)/biggestdia) * reference_circle_diameter)/px_to_mm)
        #robot(result,copper ,cor ,src)
    
    
    cv2.imshow("detected circles", src)
    cv2.waitKey(0)
    
def robot(result,copper ,cor ,src):
    coin    =[]
    flag=False
    sum = 0
    
    for i in range(0,len(result)):
        print(result[i])
        if math.isclose(result[i], 24.26, abs_tol=2.25):
            sum += 25
            print("25 cente")
            coin.append("25 cente")
        elif math.isclose(result[i], 21.21, abs_tol=1.25): 
            sum += 5
            print("5 cente")
            coin.append("5 cente")        
        elif math.isclose(result[i], 19.05, abs_tol=1.50) and copper[i]: 
            sum += 1
            print("1 cente")
            coin.append("1 cente")
        elif math.isclose(result[i], 17.91, abs_tol=1.50) and not copper[i]:
            sum += 10
            print("10 cente")
            coin.append("10 cente")
        #print(result[i])
    print("total sum :"+str(sum))
    # camera()
    #time.sleep(1)
    flag=True
    i=0
    lists=[]
    # for i in cor:
    #     cv2.putText(src, coin ,(i[0], i[1]), font, 0.5,(120,0,0),1,cv2.LINE_AA)


    return 0
if __name__ == "__main__":
    main()