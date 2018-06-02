import imutils
import cv2
import numpy as np
import pandas as pd
import logging
import time, sys ,os
import termios 

from time import sleep
from threading import Thread
from uf.wrapper.swift_api import SwiftAPI
from uf.utils.log import *


## variable declartoin 
Arm_Flag = True
armOn = False

orginal_widht ,orginal_height  = 600 ,350 
image_widht ,image_height      = 960 ,540

ratio_x,ratio_y = orginal_widht/image_widht , orginal_height/image_height 
arm_speed = 30   # max 99
reference_circle = 24.26  #Reference circle diameter (mm) 
url ="http://192.168.2.110:8080"


if(armOn):
   ## Initializing the Uarm
   swift = SwiftAPI()
   sleep(2)
   swift.set_buzzer()
   swift.flush_cmd()

   ## set Uarm to left side 
   swift.set_position(0, 250, 100, 80, relative=False, wait=True)
   sleep(1)    


## logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('uarm.log')
handler.setLevel(logging.INFO)
logger.addHandler(handler)


## Arm move controller
def armmove(x, y,toX ,toY):
   global Arm_Flag ,arm_speed
   Arm_Flag = False
   print()   

   if(y  > 0):
      x= x + 15
      y = y - 40

   
   swift.set_position(x, y, 100, arm_speed, relative=False, wait=True)
   logger.info("X ---->{}     Y--->{}".format(x,y))
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
   Arm_Flag = True   


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



def armcontroller(coin):
   if(coin ==25):
      print("taking 25 cent")
      logger.info("taking 25 cents")
      thread = Thread(target = armmove, args = (Y, X, -20, 250))
      thread.start()
     
   elif(coin ==5):
      print("taking 5 cent")
      logger.info("taking 5 cents")
      thread = Thread(target = armmove, args = (Y, X, -20, 200))
      thread.start()
  
   elif(coin == 10):
      logger.info("taking 10 cents")
      print("taking 10 cent")
      thread = Thread(target = armmove, args = (Y, X, -20, 150))
      thread.start()
  
   elif(coin == 1):
      logger.info("taking 1 cent")
      print("taking 1 cent")
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

      print(r_Min , pixel[2] ,r_Max)
      print(g_Min , pixel[1] ,g_Max)
      print(b_Min , pixel[0] ,b_Max)
      print()

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
   test_frame = img.copy()
   coin  = 0

   global ratio_x, ratio_y ,Arm_Flag , edge_Points_df , color_code_df

   
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

   # Detect blobs.
   keypoints = detector.detect(img)


   for keyPoint in keypoints:
      x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size

      X, Y  = 310-(x*ratio_y) ,(y*ratio_x) 

      X, Y  = error_correction(X,Y)

      coin = coin_find_coin_by_size(keyPoint ,test_frame)

         
      if(Arm_Flag and armOn):
         armcontroller(coin)

      # cord_text = str(int(Y))+","+str(int(X))+"->"+str(coin)
      # cord_text = "->"+str(coin)

      
      ## Final Image display 
      cord_text = str(int(Y))+","+str(int(X))
      center = (int(x), int(y))
    
      line_1x  ,line_1y, line_1x1 ,line_1y1  = x+(s/2) , y ,x-(s/2) , y 
      line_2x  ,line_2y, line_2x1 ,line_2y1  = x , y +(s/2) ,x , y -(s/2)

      cv2.putText(img, cord_text, center, cv2.FONT_HERSHEY_SIMPLEX,.4, (255, 255, 1), 1)
      cv2.line(img, (int(line_1x1) ,int(line_1y1)), (int(line_1x), int(line_1y)),(255, 0, 255), 1)
      cv2.line(img, (int(line_2x1) ,int(line_2y1)), (int(line_2x), int(line_2y)),(255, 0, 255), 1)
      cv2.circle(img, center, 1, (0, 100, 100), 1)

      data = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
      cv2.imshow("cordinates", data)


def main():
   ## Initializing cameara 
   global url
   camera = cv2.VideoCapture(url)
   
   while True:
      ## getting frame from camera
      retval, frame = camera.read()

      ## getting four edge points from csv 
      coords = "[({}, {}), ({}, {}),({}, {}), ({}, {}) ]".format(edge_Points_df['X'][0],edge_Points_df['Y'][0],edge_Points_df['X'][1],edge_Points_df['Y'][1],edge_Points_df['X'][2],edge_Points_df['Y'][2],edge_Points_df['X'][3],edge_Points_df['Y'][3]) 
      pts = np.array(eval(coords), dtype = "float32")

      ## resizing the  frame 
      img_width,img_height = int(frame.shape[1]/2) , int(frame.shape[0]/2)
      frame = cv2.resize(frame ,(img_width,img_height))

      ## cut the image using four points 
      resiedimage =  four_point_transform(frame,pts)
      
      ## send the frame to find the co-ordinates and coin
      Coinfinder(resiedimage)
      
      ## break the loop to exit and stop the Uarm
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break
   
   ## release the camera and destroy cv2 window
   camera.release()
   cv2.destroyAllWindows()



## find key press
def getkey():
   TERMIOS = termios
   fd = sys.stdin.fileno()
   old = termios.tcgetattr(fd)
   new = termios.tcgetattr(fd)
   new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
   new[6][TERMIOS.VMIN] = 1
   new[6][TERMIOS.VTIME] = 0
   termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
   c = None
   try:
      c = os.read(fd, 1)
   finally:
      termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
   return c


def utility_capture():
   global url

   cap = cv2.VideoCapture(url)
   ret, img = cap.read()
   test_frame = img =  cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
   cap.release()
   cv2.destroyAllWindows()
   blob_detection(img,test_frame);
   return edge_Points_df , color_code_df
   
def blob_detection(img,test_frame):
   global edge_Points_df, color_code_df, reference_circle
   arr = []
   color_code = {}   
   edge_Points = {}
 
   color_code_df = pd.DataFrame()
   edge_Points_df = pd.DataFrame()
  
   params = cv2.SimpleBlobDetector_Params()

   # Change thresholds
   params.minThreshold = 10
   params.maxThreshold = 256
   
   # Filter by circularty  
   params.filterByCircularity = True
   params.minCircularity = 0.8

   # Filter by Convexity
   params.filterByConvexity = True
   params.minConvexity = 0.87
      
   # Filter by Inertia
   params.filterByInertia = True
   params.minInertiaRatio = 0.1

   # Filter by color
   params.filterByColor=True
   params.blobColor=255;

   ## Create a detector with the parameters
   ver = (cv2.__version__).split('.')
   if int(ver[0]) < 3 :
      detector = cv2.SimpleBlobDetector(params)
   else : 
      detector = cv2.SimpleBlobDetector_create(params)
   
   keypoints = detector.detect(img)
   
   ##  find maximum diameter in image for reference 
   for keyPoint in keypoints:
      s = keyPoint.size
      arr.append(s)
   
   ##  find x,y and dia meter in px 
   if arr:
      ratio = max(arr)/reference_circle

      for keyPoint in keypoints:
         x, y, s = keyPoint.pt[0] ,keyPoint.pt[1] , keyPoint.size
         
         if int(s/ratio)>16 and int(s/ratio)<19:         
            pixel= test_frame[int(y), int(x)]         
            color_code['R'], color_code['G'], color_code['B'] = int(pixel[2]) , int(pixel[1]) ,int(pixel[0])            
            color_code_df = color_code_df.append(color_code, ignore_index=True)

         elif int(s/ratio)>=4 and int(s/ratio)<8:
            edge_Points['X'], edge_Points['Y'] =int(x) ,int(y)
            edge_Points_df = edge_Points_df.append(edge_Points, ignore_index=True)
         
         im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
         resized_image = cv2.resize(im_with_keypoints, (990, 510)) 
      
      ## Show image
      cv2.imshow("Keypoints", resized_image)
      ## Destroy cv2 window
      cv2.waitKey(0)
      cv2.destroyAllWindows()



def utility():
   print(" press 'y' for continue ,\n press 'n' to re-run utility")
   k = getkey().decode()
   print(k)
   if(k == "y"):
      print("Executing main function")
      main()
   if(k == "n"):
      print("no")
      edge_Points_df , color_code_df = utility_capture()
      print(edge_Points_df)
      print(color_code_df)
      utility()


edge_Points_df , color_code_df = utility_capture()
print(edge_Points_df)
print(color_code_df)
utility()



