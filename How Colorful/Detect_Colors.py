import numpy as np
import cv2


#cap video first
cap = cv2.VideoCapture("shape_detection_transition.mp4")

#set true

while True:
#retrieve video frame
    ret, frame = cap.read()
#if fail to retrieve
    if not ret:
        break