import imutils
import cv2
import numpy as np
from time import sleep
import pandas as pd



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


def Coinfinder(img):

   cali_square_X = 150
   cali_square_Y = 0

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
   params.blobColor=255;

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
   
   ratio = max(arr)/30
   array_index = arr.index(max(arr))
   big_circle = cordinates[array_index]


   for keyPoint in keypoints:
      x, y ,s = keyPoint.pt[0] , keyPoint.pt[1], keyPoint.size
      shape = str(x)+" - "+str(y)

      ratio_x,ratio_y = 600/960 , 350/540 
      print("ratio")
      print(ratio_x,ratio_y)

      # if((x*ratio_y) > 300):
      #    X ,Y = 311-(x*ratio_y) , (y*ratio_x)
      # else:
      #    X ,Y = 307-(x*ratio_y) , (y*ratio_x)

      X ,Y = 300 - (x*ratio_y) , (y*ratio_x)

      print("X,Y in px")
      print(x,y)

      cord_text = str(int(Y))+","+str(int(X)) 
      #cord_text = str(s)
      center = (int(x), int(y))

      line_1x  ,line_1y  = x+(s/2) , y
      line_1x1 ,line_1y1 = x-(s/2) , y

      line_2x  ,line_2y  = x , y +(s/2)
      line_2x1 ,line_2y1 = x , y -(s/2)

      cv2.putText(img, cord_text, center, cv2.FONT_HERSHEY_SIMPLEX,.5, (0, 0, 255), 2)
      cv2.line(img, (int(line_1x1) ,int(line_1y1)), (int(line_1x), int(line_1y)),(255, 0, 255), 1)
      cv2.line(img, (int(line_2x1) ,int(line_2y1)), (int(line_2x), int(line_2y)),(255, 0, 255), 1)
      cv2.circle(img, center, 1, (0, 100, 100), 1)
      
      data = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
      cv2.imshow("cordinates", data)


def main():

   camera = cv2.VideoCapture("http://192.168.1.188:8080")
   while True:
      retval, frame = camera.read()

      img_width,img_height = int(frame.shape[1]/2) , int(frame.shape[0]/2)
   
      print("image widh")
      print(img_width,img_height)
      
      coords = pd.read_csv("edge_Points_for_detect.csv")

      coords = "[({}, {}), ({}, {}),({}, {}), ({}, {}) ]".format(coords['X'][0],coords['Y'][0],coords['X'][1],coords['Y'][1],coords['X'][2],coords['Y'][2],coords['X'][3],coords['Y'][3])
   
      #coords = "[(142, 104), (146, 521),(860, 515), (861, 100) ]"
      
      pts = np.array(eval(coords), dtype = "float32")

      frame = cv2.resize(frame ,(img_width,img_height))
      resiedimage =  four_point_transform(frame,pts)
      cv2.imshow("refframe",frame)
      cv2.imshow("resiedimage",resiedimage)
      #Coinfinder(frame)      
      
      Coinfinder(resiedimage)
      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   camera.release()
   cv2.destroyAllWindows()

main()