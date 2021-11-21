# TODO:
	# Optimize code. Make functions. Streamline
	# Write output to log file/serial device every certain number of frames
	# instead of every frame (too much output).
# Notes:
	# Currently (11/20/21) ready for startup on boot: CTRL+C works.
	# Please use tabs instead of spaces for white space 
	# Need to run in the root directory of the repo. (not in any subdirectory) so
	# log output is properly written.
import numpy as np
import cv2
import serial 
import os, signal
from datetime import datetime

cap = cv2.VideoCapture(0)

# Custom signal handler to handle a CTRL+C interrupt so that video capture and
# serial device are closed.
def sig_hand(sig, frame):
	print("\nFIRE DETECTION TERMINATED")
	cap.release()
	cv2.destroyAllWindows()

signal.signal(signal.SIGINT, sig_hand)

while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()

	if ret:
		# Convert to grayscale image
		gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
		# Reduce noise in image
		blur = cv2.GaussianBlur(gray, (5,5), 0)
		# Threshold the grayscale image: 
		# blur -> src img
		# 210 -> threshold value (anything below 210 turns to black)
		# 255 -> max threshold value for the THRESH_BINARY function
		# cv2.THRESH_BINARY -> if src(x,y) > thresh, set to maxval, else 0 (black)
		ret, thresh_img = cv2.threshold(blur, 210, 255, cv2.THRESH_BINARY)

		# Finds edges in the threshed image 
		# src img
		# cv2.RETR_TREE -> retrieval mode that finds contours within contours
		# cv2.CHAIN_APPROX_SIMPLE -> compresses horizontal, vertical, and diagonal 
		# segments and leaves only their end points. For example, an up-right 
		# rectangular contour is encoded with 4 points.
		contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
		now = datetime.now()
		dt_string = now.strftime("%H: %M: %S on %m/%d/%Y")
		fire_detected = 0
		try: 
			# Open a serial connection to XBee module.
			ser = serial.Serial("/dev/serial0", 9600)
			message = f"Fire detected at {dt_string}. \n\r"
			for c in contours:
				cv2.drawContours(frame, [c], -1, (0,255,0), 3)
				fire_detected = 1
			if fire_detected == 1:
				# Write the byte string (1s and 0s) to the serial device
				ser.write(message.encode('utf8'))
			ser.close()
		except:
			message = f"Fire detected at {dt_string}. \n"
			mon_dy_yr = now.strftime("%m-%d-%Y")
			for c in contours:
				cv2.drawContours(frame, [c], -1, (0,255,0), 3)
				fire_detected = 1
			if fire_detected == 1:
				os.system(f"echo \"{message}\" >> logs/{mon_dy_yr}_fire.log")


		"""
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		"""
	else:
		break
	
cap.release()
cv2.destroyAllWindows()
