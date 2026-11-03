import numpy as np
import cv2

cap = cv2.VideoCapture("noisy_mask.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #median blur
    median = cv2.medianBlur(gray,17)

    #create 5x5 kernel with 8-bit unsigned integer type
    kernel = np.ones((5, 5), np.uint8)
    #modify

    #modified = cv2.dilate(median, kernel, iterations=2)

    eroded = cv2.erode(median, kernel, iterations = 1)
    opening = cv2.morphologyEx(median, cv2.MORPH_CLOSE, kernel)
    #gauss blur

    gauss_m = cv2.GaussianBlur(eroded, (5, 5), 2)

    morph_frame = np.hstack([eroded, opening])
    cv2.imshow("median only",  median)
    cv2.imshow("original", frame)
    cv2.imshow("erode + open", morph_frame)
    if(cv2.waitKey(15) & 0xFF == ord('q')):
        break

#release memory
cv2.destroyAllWindows()
cap.release()