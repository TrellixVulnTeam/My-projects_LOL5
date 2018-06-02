import imutils
import cv2
import numpy as np
import pandas as pd
from time import sleep
from threading import Thread
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *


Arm_Flag = True

swift = SwiftAPI()
sleep(2)
swift.set_buzzer()
swift.flush_cmd()

swift.set_position(0, 250, 100, 80, relative=False, wait=True)
sleep(1)    




def armmove(x, y,toX ,toY):
   global Arm_Flag 
   Arm_Flag = False

   print("X ---->{}     Y--->{}".format(x,y))
   print()
   speed = 40   

   if(y  > 0):
      x= x+12
      y = y-12
   
   
   swift.set_position(x, y, 100, speed, relative=False, wait=True)
   sleep(1)    

   swift.set_position(x, y, 40, 5, relative=False, wait=True)
   sleep(1)

   swift.set_pump(True)
   sleep(1)

   swift.set_position(x, y, 100, speed, relative=False, wait=True)
   sleep(1)

   swift.set_position(toX, toY, 100, speed, relative=False, wait=True)
   sleep(1)

   swift.set_pump(False)
   sleep(1)
   Arm_Flag = True   



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

   horizontal_img = warped.copy()
   warped = cv2.flip( warped, 0 )

   return warped


def Coinfinder(img ,test_frame):

   coin  = 0

   params = cv2.SimpleBlobDetector_Params()

   params.minThreshold = 10
   params.maxThreshold = 256

   # Filter by Area.
   params.filterByArea = True
   params.minArea = 100

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
   params.blobColor=255

   # Create a detector with the parameters
   ver = (cv2.__version__).split('.')
   if int(ver[0]) < 3 :
      detector = cv2.SimpleBlobDetector(params)
   else : 
      detector = cv2.SimpleBlobDetector_create(params)


   arr = []
   cordinates= []

   # Detect blobs.
   keypoints = detector.detect(img)

   for keyPoint in keypoints:
      x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size
      arr.append(s)
      cordinates.append([x,y])

   if arr:
      color_codes = pd.read_csv('color_code_calibrate.csv')
      
      ratio = max(arr)/30
      array_index = arr.index(max(arr))
      big_circle = cordinates[array_index]


      for keyPoint in keypoints:
         x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size
         shape = str(x)+" - "+str(y)
         
         print(s)

         ratio_x,ratio_y = 600/960 , 350/540 

         # print("ratio of X and Y")
         # print(ratio_x,ratio_y)

         Y , X =  (y*ratio_x) , 310-(x*ratio_y) ,
         # X = X + ratio_y

         if(Y < 30):
            Y = Y -2
         if(Y > 50):
            Y = Y +2
         if(Y > 100):
            Y = Y +3
         if(Y > 150):
            Y = Y +3
         if(Y > 200):
            Y = Y -2
         if(Y > 250):
            Y = Y +2
         if(Y < 300):
            Y = Y +2


         if(X < 160):
            X = X - 5
         
         if(X > 200):
            X = X - 5
         
         if(X < 0):
            X = X + 4
         if(X < -150):
            X = X + 3
         if(X < -250):
            X = X + 3


         # print((x*ratio_y)/25)
         # print("X,Y in px")
         # print(x,y)

         if int(s/ratio)>16 and int(s/ratio)<19:

               pixel= test_frame[int(y), int(x)]
               normal_List = np.array(pixel).tolist()
               r_code = normal_List[2]
               g_code = normal_List[1]
               b_code = normal_List[0]
               r_Max = color_codes['R'].max()+10
               r_Min = color_codes['R'].min()-10
               g_Max = color_codes['G'].max()+10
               g_Min =  color_codes['G'].min()-10
               b_Min =  color_codes['B'].min()-10
               b_Max =  color_codes['B'].max()+10
               
               if r_Min <= r_code <=r_Max and g_Min <= g_code <=g_Max and b_Min <= b_code <=b_Max: 
                  coin = 10
               else:
                  coin = 1
         elif int(s/ratio)>=20 and int(s/ratio)<=22:
            coin = 5
            
         elif int(s/ratio)>=23 and int(s/ratio)<=26:
            coin = 25
            
         elif int(s/ratio)>=28 and int(s/ratio)<=32:
            #print("Refence circle")
            coin = 30
         

         global Arm_Flag
         if(Arm_Flag):
            if(coin ==25):
               print("taking 25 cent")
               thread = Thread(target = armmove, args = (Y, X, -20, 250))
               thread.start()
            elif(coin ==5):
               print("taking 5 cent")
               thread = Thread(target = armmove, args = (Y, X, -20, 200))
               thread.start()
            elif(coin == 10):
               print("taking 10 cent")
               thread = Thread(target = armmove, args = (Y, X, -20, 150))
               thread.start()
            elif(coin == 1):
               print("taking 1 cent")
               thread = Thread(target = armmove, args = (Y, X, -20, 100))
               thread.start()

         cord_text = str(int(Y))+","+str(int(X))+"->"+str(coin)
         #cord_text = str(s)
         #cord_text = str(coin)
         center = (int(x), int(y))

         line_1x  ,line_1y  = x+(s/2) , y
         line_1x1 ,line_1y1 = x-(s/2) , y

         line_2x  ,line_2y  = x , y +(s/2)
         line_2x1 ,line_2y1 = x , y -(s/2)

         cv2.putText(img, cord_text, center, cv2.FONT_HERSHEY_SIMPLEX,.4, (255, 255, 1), 1)
         cv2.line(img, (int(line_1x1) ,int(line_1y1)), (int(line_1x), int(line_1y)),(255, 0, 255), 1)
         cv2.line(img, (int(line_2x1) ,int(line_2y1)), (int(line_2x), int(line_2y)),(255, 0, 255), 1)
         cv2.circle(img, center, 1, (0, 100, 100), 1)

         data = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

         cv2.imshow("cordinates", data)


def main():

   #camera = cv2.VideoCapture("http://192.168.1.188:8080")
   # camera = cv2.VideoCapture("http://127.0.0.1:4747/mjpegfeed?1980x1080")

   camera = cv2.VideoCapture("http://192.168.2.110:8080")

   
   
   while True:
      retval, frame = camera.read()

      img_width,img_height = int(frame.shape[1]/2) , int(frame.shape[0]/2)
   
      # print("image widh")
      # print(img_width,img_height)
      
      coords = pd.read_csv("edge_Points_for_detect.csv")

      coords = "[({}, {}), ({}, {}),({}, {}), ({}, {}) ]".format(coords['X'][0],coords['Y'][0],coords['X'][1],coords['Y'][1],coords['X'][2],coords['Y'][2],coords['X'][3],coords['Y'][3])
   
      #coords = "[(142, 104), (146, 521),(860, 515), (861, 100) ]"
      
      pts = np.array(eval(coords), dtype = "float32")

      frame = cv2.resize(frame ,(img_width,img_height))
      resiedimage =  four_point_transform(frame,pts)
      test_frame = image_hsv = resiedimage

      cv2.imshow("refframe",frame)
      cv2.imshow("resiedimage",resiedimage)
      #Coinfinder(frame)      
      
      Coinfinder(resiedimage ,test_frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   camera.release()
   cv2.destroyAllWindows()

main()