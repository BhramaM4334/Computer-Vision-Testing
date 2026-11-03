import cv2 as cv2
import numpy as np

#capture video
cap = cv2.VideoCapture("shape_detection_transition.mp4")

#resize
cap.set(3, 1080)  # Width
cap.set(4, 560)  # Height

#while true
while True:
#retrieve video frame
    ret, frame = cap.read()
#if fail to retrieve
    if not ret:
        break

#turn to grayscale for contouring
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    abs_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#threshold the gray
    _, gray = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
#turn gray to 3 channels for appropriate displaying with others
    gray_3channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

#contour
    contour, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#contour frame
    contour_frame = np.zeros_like(frame)

#draw contouor
    for i in range(len(contour)):
    #to define the contours -> contour[i]
        cv2.drawContours(contour_frame, contour, -1, 255, 2)
#approx the contour for drawing later
        perimeter = cv2.arcLength(contour[i], True)
        approx = cv2.approxPolyDP(contour[i], 0.04 * perimeter, True)
        vertices = len(approx)

#displaying, init shape_name
#x+w = x axis full, y+h = y axis full
        x, y, w, h = cv2.boundingRect(approx)
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)

        shape_name = "???"

        if vertices == 3:
            shape_name = "Triangle"
        elif vertices == 4:
        #no need to check aspect ratio since it's a rectangle
            shape_name = "Square"
        elif vertices == 5:
            shape_name = "Pentagon"
        elif vertices == 6:
            shape_name = "Hexagon"
        else:
            # If vertices are high, check if it's a circle using circularity
            area = cv2.contourArea(contour[i])
            circularity = (4 * np.pi * area) / (perimeter ** 2)
            if circularity > 0.8:  # Circles are close to 1.
                shape_name = "Circle"
#draw contours + put text
        cv2.drawContours(frame, contour[i], 0, (0, 255, 0), 2)
        cv2.putText(frame, shape_name, (center_x - 50, center_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Parameters: frame, top-left point, bottom-right point, color (BGR), thickness
        cv2.rectangle(frame, (center_x - 10, center_y - 10), (center_x + 10, center_y + 10), (0, 255, 0), 2)

            # Draw a dot in the center
            # Parameters: frame, center point, radius, color (BGR), thickness (-1 fills the circle)
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)


#combined display
    combined_display = np.hstack([frame, gray_3channel, contour_frame]) #hstack = horizontal stack
#rescale, 0 = height & 1 = width
    scale_percent = 0.6
    width = int(combined_display.shape[1] * scale_percent *0.3)
    height = int(combined_display.shape[0] * scale_percent)
    n_display = cv2.resize(combined_display, (width, height))

#frame display resize
    f_display = cv2.resize(frame, (width, height))


#open video
    #cv2.imshow("Video", n_display)     #combined video
    cv2.imshow("video", f_display)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()