import numpy as np
import cv2


cap = cv2.VideoCapture(r'C:\Users\alkar\Documents\GitHub\IITPayload\data\videotest2.avi')

while(True):
  # Capture frame-by-frame
  ret, frame = cap.read()

  gray = cv2.cvtColor (frame, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray, (5,5), 0)
  ret, thresh_img = cv2.threshold(blur, 91, 255, cv2.THRESH_BINARY)

  contours = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

  for c in contours:
    cv2.drawContours(frame, [c], -1, (0,255,0), 3)


  cv2.imshow('frame', frame)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()