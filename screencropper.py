from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2

cap = cv2.VideoCapture('gameboy.mp4') 
frame_counter = 0
found = False
while(True):
  # Capture frame-by-frame
  ret, frame = cap.read()
  frame_counter += 1
  #If the last frame is reached, reset the capture and the frame_counter
  if frame_counter == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
    frame_counter = 0 #Or whatever as long as it is the same as next line
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
  # Our operations on the frame come here

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (15, 15), 0)
  ret,gray = cv2.threshold(gray, 81, 255, cv2.THRESH_BINARY)
  edged = cv2.Canny(gray, 150, 200)
  
  box = frame.copy()
  
  # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  # ORANGE_MIN = np.array([0, 0, 0],np.uint8)
  # ORANGE_MAX = np.array([100, 100, 100],np.uint8)
  # frame_threshed = cv2.inRange(gray, ORANGE_MIN, ORANGE_MAX)
  # edged = cv2.Canny(frame_threshed, 150, 200)

  # find the contours in the edged image, keeping only the
  # largest ones, and initialize the screen contour
  (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:4]
  
  # loop over the contours
  for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
   
    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:# and found != True:
      found = True
      
      try:
        oldarea = cv2.contourArea(approx)
        change = abs(cv2.contourArea(screenCnt) - oldarea)
        if change > 50 and change < oldarea/4:
          screenCnt = approx
          cv2.drawContours(box, [screenCnt], -1, (0, 255, 0), 2)
          # cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2)
      except:
        screenCnt = approx
      
      # try:
      #   if abs( (approx[1][0][0] - approx[0][0][0]) :
      #     screenCnt = approx
      #   else:
      #     print 'no'
      # except:
      #   # cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 2)
      break

  # convert the warped image to grayscale, then threshold it
  # to give it that 'black and white' paper effect
  # warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
  # warped = threshold_adaptive(warped, 250, offset = 10)
  # warped = warped.astype("uint8") * 255
  

  warped = four_point_transform(frame, screenCnt.reshape(4, 2))
  cv2.imshow("Original", imutils.resize(box, height = 350))
  cv2.imshow("Gray", imutils.resize(gray, height = 350))
  cv2.imshow("Scanned", cv2.resize(warped, (800, 800)))

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
