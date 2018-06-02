#!/usr/bin/python3
import json
import cgi, cgitb
import cv2
import numpy as np
import pandas as pd
import time ,os
from time import sleep

print("Content-type: application/json")
print()

form = cgi.FieldStorage()
urlq = form.getvalue('url')



referenceCircle = 30  #Reference circle diameter (mm) 

#Function to detect the blobs
def blob_function(img):
   params = cv2.SimpleBlobDetector_Params()

   params.minThreshold = 10
   params.maxThreshold = 256

   # Filter by Circularity
   params.filterByCircularity = True
   params.minCircularity = 0.8

   # Filter by Area.
   params.filterByArea = True
   params.minArea = 14


   # Filter by Convexity
   params.filterByConvexity = True
   params.minConvexity = 0.87
      
   # Filter by Inertia
   params.filterByInertia = True
   params.minInertiaRatio = 0.1

   params.filterByColor=True
   params.blobColor=255

   # Create a detector with the parameters
   ver = (cv2.__version__).split('.')
   if int(ver[0]) < 3 :
      detector = cv2.SimpleBlobDetector(params)
   else : 
      detector = cv2.SimpleBlobDetector_create(params)

   # Detect blobs.
   keypoints = detector.detect(img)
   return keypoints


def blob_detection(img,test_frame):
   ## Using the frame find the coins and edges using blob detection
   global edgePointsdf, colorCodedf, referenceCircle
   arr = []
   colorCode = {}   
   edgePoints = {}
   colorCodedf = pd.DataFrame()
   edgePointsdf = pd.DataFrame()
   keypoints = blob_function(img)

   ##  find maximum diameter in image for reference 
   for keyPoint in keypoints:
      s = keyPoint.size
      arr.append(s)
   
   ##  find x,y and diameter in px 
   if arr:
      ratio = max(arr)/referenceCircle

      for keyPoint in keypoints:
         x, y, s = keyPoint.pt[0] ,keyPoint.pt[1] , keyPoint.size
         # print(s/ratio)
         if int(s/ratio)>15 and int(s/ratio)<19:         
            pixel= test_frame[int(y), int(x)]         
            colorCode['R'], colorCode['G'], colorCode['B'] = int(pixel[2]) , int(pixel[1]) ,int(pixel[0])            
            colorCodedf = colorCodedf.append(colorCode, ignore_index=True)

         elif int(s/ratio)>=3 and int(s/ratio)<7:
            edgePoints['X'], edgePoints['Y'] =int(x) ,int(y)
            edgePointsdf = edgePointsdf.append(edgePoints, ignore_index=True)
         
         imWithKeypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
         resizedImage = cv2.resize(imWithKeypoints, (960, 540)) 

   #Remove old files if exist during recalibration      
   try:
     os.remove("../config/EdgePoints_df.csv")
     os.remove("../config/ColorCode_df.csv")
     os.remove("../config/util_img.png")
   except OSError:
      pass

   edgePointsdf.to_csv("../config/EdgePoints_df.csv",index=False)
   colorCodedf.to_csv("../config/ColorCode_df.csv" ,index=False)
   cv2.imwrite("../config/util_img.png" ,resizedImage)
   #returns the count of edge points
   return len(edgePointsdf.index)
   
#Captures the image from camera
def camera_capture(url):
   cap = cv2.VideoCapture(url)
   sleep(1)
   ret, img = cap.read()
   testFrame = img =  cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
   # testFrame = img =  cv2.resize(img,(int(img.shape[1]/1.33333333),int(img.shape[0]/1.33333333)))
   # testFrame = img
   cap.release()
   cv2.destroyAllWindows()

   count = blob_detection(img,testFrame);
   response={}
   response["status"] = 200
   response["count"] = count
   print(json.dumps(response))

camera_capture(urlq)

#camera_capture("http://192.168.2.112:8080")
