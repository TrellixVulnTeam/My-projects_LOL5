import cv2
import numpy as np;
import json
import pandas as pd
import numpy as np
import csv
import pandas as pd
import os


def video_frame_capture():

	cap = cv2.VideoCapture("http://192.168.1.188:8080")
	ret, img = cap.read()
	test_frame = image_hsv = img =  cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))#cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	cv2.imshow("Test_Frmae", image_hsv)
	cv2.imshow("Frmae", img)
	cv2.waitKey(0)
	cap.release()
	cv2.destroyAllWindows()
	blob_detection(img,test_frame);

	
def blob_detection(img,test_frame):

	params = cv2.SimpleBlobDetector_Params()

	# Change thresholds
	params.minThreshold = 10
	params.maxThreshold = 256
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
	arr = []

	color_code = {}
	
	edge_Points = {}
	edge_Points['X'] = []
	edge_Points['Y'] = []

	color_code['R'] = []
	color_code['G'] = []
	color_code['B'] = []
	fieldnames = ['R','G','B']
	edge_names = ['X','Y']

	# Detect blobs.
	keypoints = detector.detect(img)

	for keyPoint in keypoints:
		s = keyPoint.size
		arr.append(s)
	if arr:
		ratio = max(arr)/30
		count = 0
		for keyPoint in keypoints:
			# count = count +1
			x = keyPoint.pt[0]
			y = keyPoint.pt[1]
			# print(x,y)
			s = keyPoint.size

			if int(s/ratio)>16 and int(s/ratio)<18:
				count = count + 1
				pixel= test_frame[int(y), int(x)]
				normal_List = np.array(pixel).tolist()
				color_code['R']=normal_List[2]
				color_code['G'] = normal_List[1]
				color_code['B'] = normal_List[0]

				print(color_code)
			elif int(s/ratio)>=4 and int(s/ratio)<8:
				print(int(s/ratio))
				print(x,"----",y)
				edge_Points['X'] =int(x)
				edge_Points['Y'] = int(y)

				with open('edge_Points.csv', 'a') as files:
						writer = csv.DictWriter(files, delimiter=",",fieldnames=edge_names)
						writer.writeheader()
						writer.writerow(edge_Points)

				


			with open('color_codes.csv', 'a') as files:
					writer = csv.DictWriter(files, delimiter=",",fieldnames=fieldnames)
					writer.writeheader()
					writer.writerow(color_code)

			

			# try:
   #  				os.remove('color_codes.csv')
			# except OSError:
			#     pass
				# upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
				# lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
				# print(upper,"----",lower)
			shape = str(s/ratio)
			cv2.putText(img, shape, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 3)
			im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
			resized_image = cv2.resize(im_with_keypoints, (990, 510)) 
			cv2.imshow("Keypoints", resized_image)
			cv2.waitKey(0)


			
def remove_Duplicates():
	remov = pd.read_csv("edge_Points.csv",sep=',')
	remov = remov[remov.Y != 'Y']
	remov.to_csv("edge_Points_for_detect.csv",index=False,sep=',')
	remov = pd.read_csv("color_codes.csv",sep=',')
	remov = remov[remov.R != 'R']
	remov.to_csv("color_code_calibrate.csv",index=False,sep=',')


video_frame_capture()
remove_Duplicates()

