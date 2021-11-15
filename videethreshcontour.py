import numpy as np
import cv2
import serial
from datetime import datetime


#cap = cv2.VideoCapture(r'C:\Users\alkar\Documents\GitHub\IITPayload\data\videotest2.avi')
cap = cv2.VideoCapture(0)
while(True):
  # Capture frame-by-frame
  ret, frame = cap.read()

  gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray, (5,5), 0)
  ret, thresh_img = cv2.threshold(blur, 210, 255, cv2.THRESH_BINARY)

  contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

  for c in contours:
    try:
      ser = serial.Serial("/dev/serial0", 9600)
      now = datetime.now()
      dt_string = now.strftime("%H: %M: %S, %m/%d/%Y.\n\r")
      ser.write(f"Fire detected at {dt_string}".encode('utf8'))
    finally:
      cv2.drawContours(frame, [c], -1, (0,255,0), 3)


  cv2.imshow('frame', frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
if (ser.isOpen() == True):
  ser.close()
