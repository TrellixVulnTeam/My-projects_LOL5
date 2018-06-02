#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
import json
import pandas as pd

cap = cv2.VideoCapture("http://192.168.1.188:8080")

while True:

	ret, img = cap.read()

	# Read image
	test_frame = image_hsv = img #cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	# img = cv2.imread("/tmp/coins-7.png",0)
	ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV) # Working
	ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
	ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
	ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()

	# Change thresholds
	params.minThreshold = 10
	params.maxThreshold = 256



	# Filter by Area.
	# params.filterByArea = True
	# params.minArea = 100
	# params.maxArea=150

	# Filter by Circularity
	params.filterByCircularity = True
	params.minCircularity = 0.8

	# Filter by Convexity
	params.filterByConvexity = True
	params.minConvexity = 0.87
	   
	# Filter by Inertia
	params.filterByInertia = True
	params.minInertiaRatio = 0.1

	params.filterByColor=True
	params.blobColor=255;

	# Create a detector with the parameters
	ver = (cv2.__version__).split('.')
	if int(ver[0]) < 3 :
		detector = cv2.SimpleBlobDetector(params)
	else : 
		detector = cv2.SimpleBlobDetector_create(params)

	count = 0

	# ratio = 1.251333

	arr = []

	# Detect blobs.
	keypoints = detector.detect(img)

	for keyPoint in keypoints:
		# count = count +1
		# print(keyPoint)
		# x = keyPoint.pt[0]
		# y = keyPoint.pt[1]


		# print(x,y)
		s = keyPoint.size
		arr.append(s)
		# print(s,"------",s/ratio)
		# shape = str(x)+" - "+str(y)
		# # cv2.putText(img, shape, (in
	if arr:
		ratio = max(arr)/30
		color_codes = pd.read_csv('color_code_calibrate.csv')
		# print(color_codes)
		for keyPoint in keypoints:
			count = count +1
			# print(keyPoint)
			x = keyPoint.pt[0]
			y = keyPoint.pt[1]
			# print(x,y)
			s = keyPoint.size
			if int(s/ratio)>16 and int(s/ratio)<19:
				# print(s/ratio)
				# print(x,y)
				pixel= test_frame[int(y), int(x)]
				# print(pixel)

				normal_List = np.array(pixel).tolist()
				r_code = normal_List[2]
				g_code = normal_List[1]
				b_code = normal_List[0]
				r_Max = color_codes['R'].max()+10
				r_Min = color_codes['R'].min()-10
				g_Max = color_codes['G'].max()+10
				g_Min =	color_codes['G'].min()-10
				b_Min =	color_codes['B'].min()-10
				b_Max =	color_codes['B'].max()+10
				
				if r_Min <= r_code <=r_Max and g_Min <= g_code <=g_Max and b_Min <= b_code <=b_Max: 
					print("One Dime",int(s/ratio))
				else:
					print("One Cent",float(s/ratio),pixel)
			elif int(s/ratio)>=20 and int(s/ratio)<=22:
				print("5 Cents",int(s/ratio))
			elif int(s/ratio)>=23 and int(s/ratio)<=26:
				print("25 Cents",int(s/ratio))


				# upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
				# lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
				# print(upper,"----",lower)
			# arr.append(s)
			# print(s/ratio)
			# shape = str(int(x))+" - "+str(int(y)) + "==="+ str(float(s/ratio))
			shape = str(s/ratio)
			cv2.putText(img, shape, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 3)
			im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
			resized_image = cv2.resize(im_with_keypoints, (990, 510)) 
			cv2.imshow("Keypoints", resized_image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		# 
cap.release()
cv2.destroyAllWindows()