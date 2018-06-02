import numpy as np
import cv2
import os
import time 
import datetime
cap = cv2.VideoCapture("http://192.168.1.188:8080")
# cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture(0)

while True:
	# Opening the link
	#cap.open("http://192.168.1.188:8080/video")                    
	i = 0
	# Capture frame-by-frame
	ret, frame = cap.read()

	print("Started printing image")

	#print(frame)
	# Display the resulting frame

	cv2.imshow('Mobile IP Camera',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	# ts = time.time()
	# st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	# cv2.imwrite("img"+str(st)+".jpg" ,frame)


	# # Clear screen
	# os.system ( 'clear' )
	# # Exit key
	i = i+1 


print ("Press 'q' to exit")
	# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
