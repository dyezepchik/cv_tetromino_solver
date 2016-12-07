"""
  Mat src=imread("test_shapes.jpg",1);
  Mat thr,gray;
  blur(src,src,Size(3,3));
  cvtColor(src,gray,CV_BGR2GRAY);
  Canny(gray,thr,50, 190, 3, false );
  vector<vector<Point> > contours;
  vector<Vec4i> hierarchy;
  findContours( thr.clone(),contours,hierarchy,CV_RETR_EXTERNAL,CV_CHAIN_APPROX_SIMPLE,Point(0,0));

  vector<vector<Point> > contours_poly(contours.size());
  vector<Rect> boundRect( contours.size() );
  vector<Point2f>center( contours.size() );
  vector<float>radius( contours.size() );
  vector<vector<Point> >hull( contours.size() );
  for( int i = 0; i < contours.size(); i++ )
  {
  approxPolyDP( Mat(contours[i]), contours_poly[i], 10, true );
  boundRect[i] = boundingRect( Mat(contours_poly[i]) );
  minEnclosingCircle( (Mat)contours_poly[i], center[i], radius[i] );
  convexHull( Mat(contours[i]), hull[i], false );

  if( contours_poly[i].size()>15) // Check for corner
     drawContours( src, contours_poly, i, Scalar(0,255,0), 2, 8, vector<Vec4i>(), 0, Point() ); // True object
  else
     drawContours( src, contours_poly, i, Scalar(0,0,255), 2, 8, vector<Vec4i>(), 0, Point() ); // false object
    //drawContours( src, hull, i, Scalar(0,0,255), 2, 8, vector<Vec4i>(), 0, Point() );
    // rectangle( src, boundRect[i].tl(), boundRect[i].br(), Scalar(0,255,0), 2, 8, 0 );
     //circle( src, center[i], (int)radius[i], Scalar(0,0,255), 2, 8, 0 );
  }
  imshow("src",src);
  imshow("Canny",thr);
  waitKey();
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