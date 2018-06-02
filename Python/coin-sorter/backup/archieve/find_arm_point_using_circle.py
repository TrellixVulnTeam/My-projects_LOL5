import cv2
import numpy as np


green = [(82, 123, 175),(102, 143, 255)]

dot_colors = [green]

img = cv2.imread('./img/2018-04-18-103534.jpg')   
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
        cv2.imshow("final",output)
        cv2.waitKey(0)