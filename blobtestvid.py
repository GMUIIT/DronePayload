
# Standard imports
import cv2
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='blob detector')
parser.add_argument('--img', type=str, default='data/test2.jpg')
args = parser.parse_args()

cap = cv2.VideoCapture(0)
# Read image
im = cv2.imread(args.img, cv2.IMREAD_GRAYSCALE)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

#FILTER BY COLOR
params.filterByColor = 1
params.blobColor = 255

# Change thresholds
#params.minThreshold = 0
#params.maxThreshold = 255

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else : 
	detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
