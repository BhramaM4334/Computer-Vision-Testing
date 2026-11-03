import cv2
import numpy as np

cap = cv2.VideoCapture("diamond.mp4")
counter = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #add gaussian blur to reduce noise
    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(gaussian, 5, 255, cv2.THRESH_BINARY)

    #draw contours || approx simple -> compresses horizontal, vertical, and diagonal segments and leaves only their end points. For example, an up-right rectangular contour is encoded with 4 points.
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #find contour + diamond counter, diamond counter will always be reset to 0 and then added in the i in contours loop
    diamond_counter = 0
    for i in contours:
        area = cv2.contourArea(i)

        if area > 1:
            diamond_counter +=1
            x,y,w,h = cv2.boundingRect(i)

            center_x = x+w//2
            center_y = y+h//2
            #adding rectangle + circle for location, and added a safety measurement (20 pixels)
            cv2.rectangle(frame, (x - 20, y - 20), (x+w + 20, y+h + 20), (0, 0, 255), 2)
            cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)

            #adding square + circle to contour too || debugging purposes
#            cv2.rectangle(threshold, (x, y), (x + w, y + h), (255, 255, 255), 2)
#            cv2.circle(threshold, (center_x, center_y), 5, 0, -1,)

            #the center
            x_loc = int(center_x)
            y_loc = int(center_y)

            #adding the text, diamond counter + coordinate
            cv2.putText(frame, f"Diamond {diamond_counter}", (center_x - 40, center_y + 60), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
            cv2.putText(frame, f"({center_x} , {center_y})", (center_x - 45, center_y + 90), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

            print(f"Diamond found at (midpoint): ({x_loc},{y_loc}) ")

    #frame counting + printing
    counter += 1
    print(f"Frame {counter}\n")
    print("\n")

    #change threshold display
    threshold3 = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)

    f_g_display = np.hstack([frame, threshold3])

    scale_percent = 0.6
    #0 = h, 1 = w
    width = int(f_g_display.shape[1] * 0.5 * scale_percent)
    height = int(f_g_display.shape[0] * scale_percent)
    f_g_display = cv2.resize(f_g_display, (width, height))

    cv2.imshow("Color + gray", f_g_display)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break