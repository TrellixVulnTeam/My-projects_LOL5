import imutils
import cv2
import numpy as np
from time import sleep
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *
import math

#Initializing UARM
swift = SwiftAPI()
sleep(3)
swift.set_buzzer()
swift.flush_cmd()

swift.set_position(-20, 150, 75, 80, relative=False, wait=True)


# UARM function
def armmove(x, y,toX ,toY):

   print("Comment to arm")
   print(x,y)
   speed =90
   swift.set_position(x, y, 70, speed, relative=False, wait=True)
   sleep(1)

   swift.set_position(x, y, 40, 10, relative=False, wait=True)
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
   #main()
   return;


def order_points(pts):
	
	rect = np.zeros((4, 2), dtype = "float32")
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect

def four_point_transform(image, pts):
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	maxWidth = 960
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	maxHeight = 540
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	return warped


coords = "[(142, 508), (861, 523),(870, 107), (151, 94) ]"
pts = np.array(eval(coords), dtype = "float32")

cam_coin_cor =[]
font = cv2.FONT_HERSHEY_SIMPLEX



def coindetectfunction(image):

	# horizontal_img = image.copy()
	# horizontal_img = cv2.flip( image, 0 )

	warped = four_point_transform(image, pts)
	# cv2.imshow("frame",warped)
	# cv2.waitKey(0)
	
	horizontal_img = warped.copy()
	warped = cv2.flip( warped, 0 )


	gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	gray = cv2.medianBlur(gray, 5)        

	rows = gray.shape[0]
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=120, param2=10,
                               minRadius=1, maxRadius=100)
	if circles is not None:

		coin_pos = []
		circles = np.uint16(np.around(circles))
		for i in circles[0, :]:
			center = (i[0], i[1])
			if(i[1] < 300 and i[2] < 20):
				X  = i[1] / 1.6 
				Y  = i[0] / 1.54285714 			
				radius1 = i[2] *2
				print("dia")
				print(radius1)
			

			# if(i[1] < 300 and i[2] < 20):			
			# 	X = i[1]+8

			# 	Y = 246 -i[0]
			# 	if(i[0] > 300):
			# 		X = i[1]+7
			# 		Y = 242 -i[0]
			# 	radius1 = i[2] *2
			# 	print("dia")
			# 	print(radius1)
			
				if math.isclose(radius1, 24.26, abs_tol=1.5):
					print("25 cent")
					armmove(X,Y ,-20 ,250 )	# X,Y --> coin coordinates and (3,4)argumests --> destination coordinates

				elif math.isclose(radius1, 21.21, abs_tol=1): 
					print("5 cent")
					armmove(X,Y ,-20 ,200 )   # X,Y --> coin coordinates and (3,4) argumests --> destination coordinates     

				elif math.isclose(radius1, 19.05, abs_tol=1): 
					print("10 cent")
					armmove(X,Y,-20 ,150 )    # X,Y --> coin coordinates and (3,4) argumests --> destination coordinates    

				elif math.isclose(radius1, 17.91, abs_tol=1.91):
					print("1 cent")
					armmove(X,Y ,-20 ,100 )   # X,Y --> coin coordinates and (3,4) argumests --> destination coordinates     
				else:
					print("no match")
					armmove(X,Y ,-20 ,300 )  # X,Y --> coin coordinates and (3,4) argumests --> destination coordinates

			main()
			cv2.circle(warped, center, 1, (0, 100, 100), 3)
			radius = i[2]
			cv2.circle(warped, center, radius, (255, 0, 255), 2)

			cor = str(int(i[1]))+","+str(int(250-i[0]))         
			cv2.putText(warped, cor ,(i[0], i[1]), font, 0.5,(120,0,0),1,cv2.LINE_AA)

	# cv2.imshow('Rotated',rotated)
	cv2.imshow('Flip',warped)
	cv2.waitKey(0)


def main():
   camera = cv2.VideoCapture("http://192.168.1.188:8080")
   #camera = cv2.VideoCapture(1)
   retval, frame = camera.read()


   img_width,img_height = int(frame.shape[1]/2) , int(frame.shape[0]/2)

   frame = cv2.resize(frame ,(img_width,img_height))
   # cv2.imshow("refframe",frame)
   # cv2.waitKey(0)

   # camera.release()
   # cv2.destroyAllWindows()
   
   coindetectfunction(frame)

main()
