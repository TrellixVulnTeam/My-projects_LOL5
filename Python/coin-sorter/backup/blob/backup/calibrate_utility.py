import cv2
import json
import numpy as np
import csv
import pandas as pd
import os



def video_frame_capture():

	cap = cv2.VideoCapture("http://192.168.2.110:8080")
	ret, img = cap.read()
	test_frame = image_hsv = img =  cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
	# cv2.imshow("Test_Frmae", image_hsv)
	cv2.imshow("Frmae", img)
	cv2.waitKey(0)
	cap.release()
	cv2.destroyAllWindows()
	blob_detection(img,test_frame);
	# print(r_Max,r_Min)
	print(edge_Points_df)
	print(color_code_df)
	return edge_Points_df , color_code_df
	
def blob_detection(img,test_frame):
	global edge_Points_df, color_code_df
	color_code_df = pd.DataFrame()
	edge_Points_df = pd.DataFrame()
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
	
	# Detect blobs.
	keypoints = detector.detect(img)

	for keyPoint in keypoints:
		s = keyPoint.size
		arr.append(s)
	# dataframe_count  = 0
	if arr:
		ratio = max(arr)/24.26
		# count = 0
		for keyPoint in keypoints:
			x = keyPoint.pt[0]
			y = keyPoint.pt[1]
			s = keyPoint.size

			if int(s/ratio)>16 and int(s/ratio)<18:
				# print(s/ratio)
				# count = count + 1
				pixel= test_frame[int(y), int(x)]
				normal_List = np.array(pixel).tolist()
				color_code['R'] = int(normal_List[2])
				color_code['G'] = int(normal_List[1])
				color_code['B'] = int(normal_List[0])
				color_code_df = color_code_df.append(color_code, ignore_index=True)
			elif int(s/ratio)>=4 and int(s/ratio)<8:
				# print(int(s/ratio))
				print(x,"----",y)
				edge_Points['X'] =int(x)
				edge_Points['Y'] = int(y)
				edge_Points_df = edge_Points_df.append(edge_Points, ignore_index=True)
			shape = str(s/ratio)
			# cv2.putText(img, shape, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 3)
			im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
			resized_image = cv2.resize(im_with_keypoints, (990, 510)) 
			cv2.imshow("Keypoints", resized_image)
			# cv2.waitKey(0)
	

video_frame_capture()


