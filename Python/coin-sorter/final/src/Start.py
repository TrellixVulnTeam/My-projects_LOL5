#!/usr/bin/python3
import json
import cgi, cgitb
import cv2
import numpy as np
import pandas as pd
import time, sys ,os ,glob

#Application type 
print("Content-type: application/json")
print()

form = cgi.FieldStorage()
urlq = form.getvalue('url')

#Image resizing
originalWidth,originalHeight  = 600 ,350 
imageWidth,imageHeight      = 960 ,540

#Finding the ratio
ratioX,ratioY = originalWidth/imageWidth , originalHeight/imageHeight 



## Straightend the image using four points
def order_points(pts):
   rect = np.zeros((4, 2), dtype = "float32")
   s = pts.sum(axis = 1)
   rect[0] = pts[np.argmin(s)]
   rect[2] = pts[np.argmax(s)]
   diff = np.diff(pts, axis = 1)
   rect[1] = pts[np.argmin(diff)]
   rect[3] = pts[np.argmax(diff)]
   return rect


# Strightend the image using four points
def four_point_transform(image, pts):
   rect = order_points(pts)
   (tl, tr, br, bl) = rect
   widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
   widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
   maxWidth = max(int(widthA), int(widthB))
   maxWidth = imageWidth
   heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
   heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
   maxHeight = max(int(heightA), int(heightB))
   maxHeight = imageHeight
   dst = np.array([
      [0, 0],
      [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1],
      [0, maxHeight - 1]], dtype = "float32")

   M = cv2.getPerspectiveTransform(rect, dst)
   warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
   warped = cv2.flip( warped, 0 )
   #returns the image with frame points as boundaries
   return warped 

#Finds and returns coinsize 
def coin_by_size(keyPoint,test_frame):
   global ratioY
   coin = 0

   x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size
   
   if int(s*ratioY)>16 and int(s*ratioY)<19:

      pixel= test_frame[int(y), int(x)]
      # normal_List = np.array(pixel).tolist()
      rCode = pixel[2]
      gCode = pixel[1]
      bCode = pixel[0]

      rMax =  colorCodedf['R'].max()
      rMin =  colorCodedf['R'].min()
      gMax =  colorCodedf['G'].max()
      gMin =  colorCodedf['G'].min()
      bMax =  colorCodedf['B'].max()
      bMin =  colorCodedf['B'].min()

      
      if (rMin <= rCode <= rMax) and (gMin <= gCode <= gMax) and (bMin <=  bCode <= bMax) :                
         coin = 10
      else:
         coin = 1

   elif int(s*ratioY)>=20 and int(s*ratioY)<=22:
      coin = 5
      
   elif int(s*ratioY)>=23 and int(s*ratioY)<=26:
      coin = 25

   return coin 


#Function to correct the errors
def error_correction(X,Y):
   if(Y > 30):
      Y +=  3
   if(Y > 140):
      Y +=  3
   if(Y > 190):
      Y +=  3
   if(Y > 240):
      Y +=  2
   if(Y > 290):
      Y +=  3
  
   if(X > 150):
      X -= 2
   if(X > 200):
      X -= 1
   if(X > 250):
      X -= 3
   if(X < 0):
      X += 2 
   if(X < -100):
      X += 1
   if(X < -150):
      X += 2
   if(X < -200):
      X += 1
   if(X < -250):
      X += 3

   return X, Y


#detect keypoint and then circling it
def coin_finder(img):
   coin  = 0
   global ratioX, ratioY , edgePointsdf ,colorCodedf
   test_frame = img.copy()   
   colorCodedf = pd.read_csv("../config/ColorCode_df.csv")
   keypoints = blob_function(img)
   try:
   	 os.remove("../config/Coordinates.txt")
   except OSError:
   	 pass

   f= open("../config/Coordinates.txt","w+")
   for keyPoint in keypoints:
      x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size
      X, Y  = 310-(x*ratioY) ,(y*ratioX) 
      X, Y  = error_correction(X,Y)
      coin = coin_by_size(keyPoint ,test_frame)  
      # combining x,y and coin values
      co_coin = str(X)+","+str(Y)+","+str(coin)
      # writing co_coin to file
      f.write(co_coin)
      f.write('\n')

      ## Final Image display 
      cord_text = str(int(Y))+","+str(int(X))+"->"+str(coin)
      center = (int(x), int(y))
    
      line_1x  ,line_1y, line_1x1 ,line_1y1  = x+(s/2) , y ,x-(s/2) , y 
      line_2x  ,line_2y, line_2x1 ,line_2y1  = x , y +(s/2) ,x , y -(s/2)

      cv2.putText(img, cord_text, center, cv2.FONT_HERSHEY_SIMPLEX,.4, (255, 255, 1), 1)
      cv2.line(img, (int(line_1x1) ,int(line_1y1)), (int(line_1x), int(line_1y)),(255, 0, 255), 1)
      cv2.line(img, (int(line_2x1) ,int(line_2y1)), (int(line_2x), int(line_2y)),(255, 0, 255), 1)
      cv2.circle(img, center, 1, (0, 100, 100), 1)
      data = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   f.close() 
   return data


#function to detect blobs
def blob_function(img):
   params = cv2.SimpleBlobDetector_Params()

   params.minThreshold = 10
   params.maxThreshold = 256

   # Filter by Circularity
   params.filterByCircularity = True
   params.minCircularity = 0.8

   # Filter by Area.
   params.filterByArea = True
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



def main(url):
   #Video Capture
   camera = cv2.VideoCapture(url)
   _, originalImg = camera.read()

   #getting the RGB values from CSV file
   colorCodedf = pd.read_csv("../config/ColorCode_df.csv")
   #getting the edges values
   edgePointsdf =pd.read_csv("../config/EdgePoints_df.csv")
   edgePointsdf['X'] = edgePointsdf['X'].astype(int)
   edgePointsdf['Y'] = edgePointsdf['Y'].astype(int)

   # getting four edge points from csv 
   coords = "[({}, {}), ({}, {}),({}, {}), ({}, {}) ]".format(edgePointsdf['X'][0],edgePointsdf['Y'][0],edgePointsdf['X'][1],edgePointsdf['Y'][1],edgePointsdf['X'][2],edgePointsdf['Y'][2],edgePointsdf['X'][3],edgePointsdf['Y'][3]) 
   pts = np.array(eval(coords), dtype = "float32")

   # resizing the frame 
   imgWidth,imgHeight = int(originalImg.shape[1]/2) , int(originalImg.shape[0]/2)
   # imgWidth,imgHeight = int(originalImg.shape[1]/1.33333333) , int(originalImg.shape[0]/1.33333333)
   frame = cv2.resize( originalImg,(imgWidth,imgHeight))

   # cut the image using four points 
   resizedimage =  four_point_transform(frame,pts)
   # cv2.imwrite("resizedimage.png" , resizedimage)
   
   ## send the frame to find the co-ordinates and coin
   data =  coin_finder(resizedimage)
   cv2.imwrite("../config/Coin.png" , data)
   camera.release()
   cv2.destroyAllWindows()


   response={}
   response["status"] = 200
   response["msg"] = "coins detecde"
   print(json.dumps(response))

#Main function call
main(urlq)

#main("http://192.168.2.112:8080")

