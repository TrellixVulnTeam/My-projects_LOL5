#!/usr/bin/python3
# import imutils
import cv2
import numpy as np
import pandas as pd
import logging
import time, sys ,os ,glob
# import termios 

from time import sleep
from threading import Thread
from uf.wrapper.swift_api import SwiftAPI 
from uf.utils.log import *
import datetime


file = open("Arm_Flag.txt","w")
file.write("True")
file.close()


# Arm_Flag = True
armOn = True

orginal_widht ,orginal_height  = 600 ,350 
image_widht ,image_height      = 960 ,540

ratio_x,ratio_y = orginal_widht/image_widht , orginal_height/image_height 
arm_speed = 30   # max 99
reference_circle = 24.26  #Reference circle diameter (mm) 
gurl ="http://192.168.2.120:8080"
url_img = "imge.png"



if(armOn):
   # print"Initializing Uarm")
   swift = SwiftAPI()
   sleep(2)
# swift.set_buzzer()
   swift.flush_cmd()

## print"set Uarm position to leftside to start calibration")
## set Uarm to left side 
# SwiftAPI().set_buzzer()
   swift.set_position(0, 250, 100, 80, relative=False, wait=True)
   sleep(1)    


# swift.set_position(0, 250, 100, 80, relative=False, wait=True)
# sleep(1)    


## Arm move controller
def armmove(x, y,toX ,toY):
   # swift = SwiftAPI()
   # sleep(2)


   # global Arm_Flag ,arm_speed
   global arm_speed
   file = open("Arm_Flag.txt","w")
   file.write("False")
   file.close() 
   # Arm_Flag = False

   ## print"X ---->{}     Y--->{}".format(x,y))
   ## print)   
   
   swift.set_position(x, y, 100, arm_speed, relative=False, wait=True)
   sleep(1) 

   swift.set_position(x, y, 40, 5, relative=False, wait=True)
   sleep(1)

   swift.set_pump(True)
   sleep(1)

   swift.set_position(x, y, 100, arm_speed, relative=False, wait=True)
   sleep(1)

   swift.set_position(toX, toY, 100, arm_speed, relative=False, wait=True)
   sleep(1)

   swift.set_pump(False)
   sleep(1)
   file = open("Arm_Flag.txt","w")
   file.write("True")
   file.close()
   # Arm_Flag = True   


def armcontroller(coin, X, Y):
   if(coin ==25):
      ## print"taking 25 cent")
      thread = Thread(target = armmove, args = (Y, X, -20, 250))
      thread.start()
     
   elif(coin ==5):
      ## print"taking 5 cent")
      thread = Thread(target = armmove, args = (Y, X, -20, 200))
      thread.start()
  
   elif(coin == 10):
      ## print"taking 10 cent")
      thread = Thread(target = armmove, args = (Y, X, -20, 150))
      thread.start()
  
   elif(coin == 1):
      ## print"taking 1 cent")
      thread = Thread(target = armmove, args = (Y, X, -20, 100))
      thread.start()



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

def coin_by_size(keyPoint,test_frame):
   global ratio_y
   coin = 0


   x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size
   
   if int(s*ratio_y)>16 and int(s*ratio_y)<19:

      pixel= test_frame[int(y), int(x)]
      # normal_List = np.array(pixel).tolist()
      r_code = pixel[2]
      g_code = pixel[1]
      b_code = pixel[0]

      r_Max =  color_code_df['R'].max()+20
      r_Min =  color_code_df['R'].min()-20
      g_Max =  color_code_df['G'].max()+20
      g_Min =  color_code_df['G'].min()-20
      b_Max =  color_code_df['B'].max()+30
      b_Min =  color_code_df['B'].min()-10

      
      if (r_Min <= r_code <= r_Max) and (g_Min <= g_code <= g_Max) and (b_Min <=  b_code <= b_Max) :                
         coin = 10
      else:
         coin = 1

   elif int(s*ratio_y)>=20 and int(s*ratio_y)<=22:
      coin = 5
      
   elif int(s*ratio_y)>=23 and int(s*ratio_y)<=26:
      coin = 25

   return coin 



def Coinfinder(img):
   total = 0
   coin  = 0
   # cent_10 = 0
   # cent_1  = 0
   # cent_5  = 0
   # cent_25 = 0


   global ratio_x, ratio_y ,Arm_Flag , edge_Points_df ,color_code_df,armOn
   test_frame = img.copy()
   
   color_code_df = pd.read_csv("color_code_df.csv")
   keypoints = blob_function(img,False)

   for keyPoint in keypoints:

      x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size
      X, Y  = 310-(x*ratio_y) ,(y*ratio_x) 
      X, Y  = error_correction(X,Y)
      coin = coin_by_size(keyPoint ,test_frame)

      # if(coin == 10):
      #    cent_10 += 1    	
      # if(coin == 1):
      #    cent_1 += 1    	
      # if(coin == 5):
      #   cent_5 += 1    	
      # if(coin == 25):
      #   cent_25 += 1    	
  
      file = open("Arm_Flag.txt", "r") 
      Arm_Flag = file.read() 
      # print(Arm_Flag)
      file.close()

      # if(Arm_Flag and armOn):
      if(Arm_Flag == "True"):
         armcontroller(coin, X, Y)

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
      # cv2.imshow("image1",data)
      # print(coin)
      total += 1 
      # print(coin)
      # break
   # print(total , cent_10, cent_1 , cent_5, cent_25)
      # cv2.waitKey(0)
   # cv2.imshow("image1",data)
   # cv2.imwrite("url_img.png",data)
   # return url_img
   return data


## Strightend the image using four points
def order_points(pts):
   rect = np.zeros((4, 2), dtype = "float32")
   s = pts.sum(axis = 1)
   rect[0] = pts[np.argmin(s)]
   rect[2] = pts[np.argmax(s)]
   diff = np.diff(pts, axis = 1)
   rect[1] = pts[np.argmin(diff)]
   rect[3] = pts[np.argmax(diff)]
   return rect


## Strightend the image using four points
def four_point_transform(image, pts):
   ## print"using edge points Strightend the image")
   rect = order_points(pts)
   (tl, tr, br, bl) = rect
   widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
   widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
   maxWidth = max(int(widthA), int(widthB))
   maxWidth = image_widht
   heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
   heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
   maxHeight = max(int(heightA), int(heightB))
   maxHeight = image_height
   dst = np.array([
      [0, 0],
      [maxWidth - 1, 0],
      [maxWidth - 1, maxHeight - 1],
      [0, maxHeight - 1]], dtype = "float32")

   M = cv2.getPerspectiveTransform(rect, dst)
   warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
   warped = cv2.flip( warped, 0 )

   return warped



def main(url):

   ## Initializing cameara 
   ## print"Initializing camera for coin detection")
   # global url
   camera = cv2.VideoCapture(url)
   edge_Points_df =pd.read_csv("edge_Points_df.csv")
   edge_Points_df['X'] = edge_Points_df['X'].astype(int)
   edge_Points_df['Y'] = edge_Points_df['Y'].astype(int)
   # print(edge_Points_df)
   while True:
      ## getting frame from camera
      retval, frame = camera.read()

      ## getting four edge points from csv 
      coords = "[({}, {}), ({}, {}),({}, {}), ({}, {}) ]".format(edge_Points_df['X'][0],edge_Points_df['Y'][0],edge_Points_df['X'][1],edge_Points_df['Y'][1],edge_Points_df['X'][2],edge_Points_df['Y'][2],edge_Points_df['X'][3],edge_Points_df['Y'][3]) 
      pts = np.array(eval(coords), dtype = "float32")

      ## resizing the  frame 
      ## print"Resizing the frame")
      img_width,img_height = int(frame.shape[1]/1.33333333) , int(frame.shape[0]/1.33333333)
      # img_width,img_height = int(frame.shape[1]/2) , int(frame.shape[0]/2)
      frame = cv2.resize(frame ,(img_width,img_height))
      ## cut the image using four points 
      resiedimage =  four_point_transform(frame,pts)
      ## print("resiedimage")
      ## send the frame to find the co-ordinates and coin
      data =  Coinfinder(resiedimage)
      # sleep(1)
      data_mob = cv2.resize(data,(int(data.shape[1]/2),int(data.shape[0]/2)))
      cv2.imshow("url_img",data)
      # cv2.imwrite("url_img_mob.png",data_mob)
      # cv2.imwrite("url_img.png",data)
      
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break
   
   ## release the camera and destroy cv2 window
   camera.release()
   cv2.destroyAllWindows()
      # break
   # print(resiedimage)
   return 200 



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
         resized_image = cv2.resize(im_with_keypoints, (990, 510)) 
      
   ts = time.time()
   st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d%H:%M:%S')
   url_img = "utility_image"+st+".png"
   for filename in glob.glob("utility_image*"):
      os.remove(filename)
   edge_Points_df.to_csv("edge_Points_df.csv",index=False)
   color_code_df.to_csv("color_code_df.csv" ,index=False)
   cv2.imwrite(url_img ,resized_image)
   # print(len(edge_Points_df.index))
   return len(edge_Points_df.index)
   
def utility_capture(url):
   global gurl
   gurl =url
   cap = cv2.VideoCapture(url)
   sleep(1)
   ret, img = cap.read()
   # test_frame = img =  cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
   test_frame = img =  cv2.resize(img,(int(img.shape[1]/1.33333333),int(img.shape[0]/1.33333333)))
   # test_frame = img
   cap.release()
   cv2.destroyAllWindows()

   count = blob_detection(img,test_frame);

   return 200 , url_img, count



utility_capture("http://192.168.1.103:8080/")

main("http://192.168.1.103:8080/")