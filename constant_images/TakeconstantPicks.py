#!usr/bin/env python3

import cv2
import time
import datetime

cam = cv2.VideoCapture(0)

while True:
	time.sleep(30)
	curr_time = datetime.datetime.now()
	formatted_time = "{}-{}-{}-{}".format(curr_time.day, curr_time.hour,
					 curr_time.minute, curr_time.second)
	ret, image = cam.read()
	cv2.imwrite('/home/pi/constant_images/{}.jpg'.format(formatted_time), image)


cam.release()
cv2.destroyAllWindows()
