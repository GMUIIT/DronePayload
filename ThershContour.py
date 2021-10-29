# import opencv
import cv2
import numpy as np

# Read image
src = cv2.imread("assets/test3.jpeg", 0);


# Thresholding using THRESH_TOZERO
th, dst = cv2.threshold(src,50,255, cv2.THRESH_BINARY)
cv2.imwrite("assets/opencv-thresh-tozero.jpg", dst)
image = cv2.imread("assets/opencv-thresh-tozero.jpg")

blue, green, red = cv2.split(image)

contours2, hierarchy2 = cv2.findContours(image=green, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
# draw contours on the original image
image_contour_green = image.copy()
cv2.drawContours(image=image_contour_green, contours=contours2, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
# see the results
cv2.imshow('Contour detection using green channels only', image_contour_green)
cv2.waitKey(0)
cv2.imwrite('green_channel.jpg', image_contour_green)
cv2.destroyAllWindows()

im = cv2.imread("assets/opencv-thresh-tozero.jpg", 0)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
print(params)

# Change thresholds
params.minThreshold = 100
params.maxThreshold = 1000

# Filter by Area.
params.filterByArea = True
params.minArea = 1000

# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.1

# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)