from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2

cap = cv2.VideoCapture('gameboy.mp4') 
frame_counter = 0

while(True):
  ret, frame = cap.read()
  frame_counter += 1
  if frame_counter == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
    frame_counter = 0
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  gray = cv2.GaussianBlur(gray, (15, 15), 0)
  ret,gray = cv2.threshold(gray, 81, 255, cv2.THRESH_BINARY)
  edged = cv2.Canny(gray, 150, 200)
  
  box = frame.copy()
  
  (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:4]
  
  for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
   
    if len(approx) == 4:
      try:
        oldarea = cv2.contourArea(approx)
        change = abs(cv2.contourArea(screenCnt) - oldarea)
        if change < oldarea/4:
          screenCnt = approx
          cv2.drawContours(box, [screenCnt], -1, (0, 255, 0), 2)
      except:
        screenCnt = approx
      break

  warped = four_point_transform(frame, screenCnt.reshape(4, 2))
  cv2.imshow("Original", imutils.resize(box, height = 350))
  cv2.imshow("Gray", imutils.resize(gray, height = 350))
  cv2.imshow("Scanned", cv2.resize(warped, (872, 800)))

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
