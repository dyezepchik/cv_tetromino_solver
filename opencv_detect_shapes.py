"""
TODO: how to match tetromino shapes? plus one pentamino shape: |_|
"""

import numpy as np
import cv2

def auto_canny(image, sigma=0.1):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
 
    # return the edged image
    return edged

img = cv2.imread('epam_tetro_small.jpg')
# gray = cv2.imread('test_shapes.jpg',0)

blur = cv2.blur(img, (5,5));
# blur = cv2.GaussianBlur(img,(3,3),0)

gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# ret3, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# ret, thresh = cv2.threshold(gray, 60, 100, cv2.THRESH_BINARY)
# thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

edges = cv2.Canny(gray, 30, 60)
# edges = auto_canny(gray)

im2, contours, h = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
cv2.drawContours(img, contours, -1, (0,255,0), 3)

# for cnt in contours:
#     approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
#     print len(approx)
#     if len(approx)==5:
#         print "pentagon"
#         cv2.drawContours(img,[cnt],0,255,-1)
#     elif len(approx)==3:
#         print "triangle"
#         cv2.drawContours(img,[cnt],0,(0,255,0),-1)
#     elif len(approx)==4:
#         print "square"
#         cv2.drawContours(img,[cnt],0,(0,0,255),-1)
#     elif len(approx) == 9:
#         print "half-circle"
#         cv2.drawContours(img,[cnt],0,(255,255,0),-1)
#     elif len(approx) > 15:
#         print "circle"
#         cv2.drawContours(img,[cnt],0,(0,255,255),-1)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()