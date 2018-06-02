# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
import argparse
import imutils
import cv2


def ShapeDetector(c):

	shape = ""
	peri = cv2.arcLength(c, True)

	approx = cv2.approxPolyDP(c, 0.04 * peri, True)

	if len(approx) == 5:
		shape = "pentagon"
	else:
		shape = "no"

	return shape


cap = cv2.VideoCapture("http://192.168.1.188:8080/")

while True:

    ret, im = cap.read()

	image = cv2.imread(args["image"])
	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])

	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

	blurred= cv2.medianBlur(gray, 5) 

	#blurred = cv2.GaussianBlur(gray, (7, 7), 0)

	cv2.imshow("blurred" ,blurred)
	cv2.waitKey(0)

	#thresh = cv2.threshold(blurred, 180, 245, cv2.THRESH_BINARY)[1]

	mask = cv2.erode(resized, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	cv2.imshow("data",mask)
	cv2.waitKey(0)


	cv2.imshow("thresh" ,thresh)
	cv2.waitKey(0)


	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	for c in cnts:

		M = cv2.moments(c)
		if(M["m00"] != 0):
			cX = int((M["m10"] / M["m00"]) * ratio)
			cY = int((M["m01"] / M["m00"]) * ratio)
			shape = ShapeDetector(c)

			if(shape == "pentagon"):
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				print(cX, cY)
				cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
				cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)

				# show the output image
				cv2.imshow("Image", image)
				cv2.waitKey(0)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
        
cap.release()
cv2.destroyAllWindows()