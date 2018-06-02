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



reference_circle = 24.26  #Reference circle diameter (mm) 

def blob_function(img,is_utility):
   params = cv2.SimpleBlobDetector_Params()

   params.minThreshold = 10
   params.maxThreshold = 256

   # Filter by Circularity
   params.filterByCircularity = True
   params.minCircularity = 0.8

   # Filter by Area.
   params.filterByArea = True
   if(is_utility):
      params.minArea = 14
   else:
      params.filterByArea = True
      params.minArea = 30


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
   ## print"using the frame find the coins and edges using blob detection")
   global edge_Points_df, color_code_df, reference_circle ,url_img
   arr = []
   color_code = {}   
   edge_Points = {}
   color_code_df = pd.DataFrame()
   edge_Points_df = pd.DataFrame()
   keypoints = blob_function(img,True)

   ##  find maximum diameter in image for reference 
   for keyPoint in keypoints:
      s = keyPoint.size
      arr.append(s)
   
   ##  find x,y and dia meter in px 
   if arr:
      ratio = max(arr)/reference_circle

      for keyPoint in keypoints:
         x, y, s = keyPoint.pt[0] ,keyPoint.pt[1] , keyPoint.size
         # print(s/ratio)
         if int(s/ratio)>15 and int(s/ratio)<19:         
            pixel= test_frame[int(y), int(x)]         
            color_code['R'], color_code['G'], color_code['B'] = int(pixel[2]) , int(pixel[1]) ,int(pixel[0])            
            color_code_df = color_code_df.append(color_code, ignore_index=True)

         elif int(s/ratio)>=4 and int(s/ratio)<8:
            edge_Points['X'], edge_Points['Y'] =int(x) ,int(y)
            edge_Points_df = edge_Points_df.append(edge_Points, ignore_index=True)
         
         im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
         resized_image = cv2.resize(im_with_keypoints, (960, 540)) 
      
   try:
     os.remove("edge_Points_df.csv")
     os.remove("color_code_df.csv")
     os.remove("util_img.png")
   except OSError:
      pass

   edge_Points_df.to_csv("edge_Points_df.csv",index=False)
   color_code_df.to_csv("color_code_df.csv" ,index=False)
   cv2.imwrite("util_img.png" ,resized_image)
   # print(len(edge_Points_df.index))
   return len(edge_Points_df.index)
   
def utility_capture(url):
   global gurl
   gurl =url
   cap = cv2.VideoCapture(url)
   sleep(1)
   ret, img = cap.read()
   test_frame = img =  cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
   # test_frame = img =  cv2.resize(img,(int(img.shape[1]/1.33333333),int(img.shape[0]/1.33333333)))
   # test_frame = img
   cap.release()
   cv2.destroyAllWindows()

   count = blob_detection(img,test_frame);
   response={}
   response["status"] = 200
   response["count"] = count
   print(json.dumps(response))

utility_capture(urlq)

# utility_capture("http://192.168.1.100:8080")