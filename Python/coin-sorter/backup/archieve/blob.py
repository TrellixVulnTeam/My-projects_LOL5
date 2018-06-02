#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;
from scipy import ndimage
import imutils



def ratio_find(img):

	cali_square_X = 300
	cali_square_Y = 200
	cali_square_X = 150
	cali_square_Y = 0

	cordinates =[]
	ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV) # Working
	ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
	ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
	ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

	cv2.imshow("rotated", img)

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

	arr = []

	# Detect blobs.
	keypoints = detector.detect(img)

	for keyPoint in keypoints:

		x = keyPoint.pt[0]
		y = keyPoint.pt[1]

		s = keyPoint.size

		arr.append(s)
		cordinates.append([x,y])
	
	#print(arr)
	
	
	ratio = max(arr)/30

	array_index = arr.index(max(arr))
	
	print(cordinates[array_index])
	big_circle = cordinates[array_index]
	Big_circle_X = big_circle[0]
	Big_circle_Y = big_circle[1]
	print("Ratio")
	print(ratio)

	for keyPoint in keypoints:
		count = count +1
		# print(keyPoint)
		x = keyPoint.pt[0]
		y = keyPoint.pt[1]

		# print(x,y)
		s = keyPoint.size

		#print(s,"------",s/ratio)
		shape = str(x)+" - "+str(y)



		targetX = cali_square_X - ((y - Big_circle_Y) / ratio)

		print("X Value ====> "+str(targetX))

		targetY = cali_square_Y - ((x - Big_circle_X) / ratio)
		
		print("Y Value ====> "+str(targetY))
		
		print("-----------------------------------")

		cord = str(int(targetX))+","+str(int(targetY)) 
		cv2.putText(img, cord, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,.5, (17, 255, 255), 2)

		im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imshow("cordinates", im_with_keypoints)





def detect(c):
	# initialize the shape name and approximate the contour
	shape = "unidentified"
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.04 * peri, True)

	if len(approx) == 4:
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)
		print("with,height")
		shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

	return shape



def main():

	cap = cv2.VideoCapture("http://192.168.1.188:8080")

	while True:

		ret, image = cap.read()
		
		print(image.shape)
		
		img_width,img_height = int(image.shape[1]/2) , int(image.shape[0]/2)

		image = cv2.resize(image ,(img_width,img_height))
		rotated = image

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (1,1), 0)
		thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
		
		#cv2.imshow("thresh",thresh)

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		# loop over the contours
		for c in cnts:
			M = cv2.moments(c)
			if(M["m00"] != 0 ):

				cX = int((M["m10"] / M["m00"]) )
				cY = int((M["m01"] / M["m00"]) )
				area = cv2.contourArea(c)

				shape = detect(c)

				if( (area > 2000) and (shape == "square")):
					print("Center of square in px")
					print(cX,cY)


					rect = cv2.minAreaRect(c)
					print("angledifferents")
					print(rect [2])
					if(-(rect [2]) < 45):
						rotated = ndimage.rotate(image, rect [2])
					else:
						angle = -(-(rect [2]) - 90)
						rotated = ndimage.rotate(image, angle)


					ratio_find(rotated )
		
					c = c.astype("float")
					c = c.astype("int")
		
					cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
					cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
					cv2.circle(image, (cX, cY), 1, (255, 0, 255), 1)

				# show the output image
			cv2.imshow("Image", image)
			#cv2.imshow("rotate", rotated)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


	cap.release()
	cv2.destroyAllWindows()

main()