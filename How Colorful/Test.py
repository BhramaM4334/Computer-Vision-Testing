import cv2
import numpy as np
import time


def count_specific_colors_realtime(video_path, resize_width=480):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file.")
        return

    # Define the HSV ranges for the colors you want to track
    color_ranges = {
        "Blue": (np.array([90, 50, 50]), np.array([130, 255, 255])),
        "Green": (np.array([35, 50, 50]), np.array([85, 255, 255])),
        "Yellow": (np.array([20, 50, 50]), np.array([35, 255, 255])),
        "Red": [(np.array([0, 50, 50]), np.array([10, 255, 255])),
                (np.array([170, 50, 50]), np.array([180, 255, 255]))]
    }

    print("Tracking specific colors in real-time. Press Ctrl+C to stop...\n")

    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30
    frame_delay = 1.0 / fps

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("\nEnd of video reached.")
            break

        frame_count += 1

        # Resize frame for performance
        h, w = frame.shape[:2]
        new_height = int(h * (resize_width / w))
        resized = cv2.resize(frame, (resize_width, new_height))

        # 1. Convert frame to HSV
        hsv_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        total_pixels = resized.shape[0] * resized.shape[1]

        print(f"=== Frame {frame_count} ===")

        # 2. Loop through each color category and isolate it
        for color_name, bounds in color_ranges.items():

            if color_name == "Red":
                # Red needs two masks because it wraps around 0 and 180
                mask1 = cv2.inRange(hsv_frame, bounds[0][0], bounds[0][1])
                mask2 = cv2.inRange(hsv_frame, bounds[1][0], bounds[1][1])
                mask = cv2.bitwise_or(mask1, mask2)  # Combine both red ranges
            else:
                # Single range for other colors
                mask = cv2.inRange(hsv_frame, bounds[0], bounds[1])

            # 3. Count non-zero pixels in the mask (pixels matching that color)
            pixel_count = cv2.countNonZero(mask)
            percentage = (pixel_count / total_pixels) * 100

            print(f"  {color_name:<8} | Pixels: {pixel_count:,} ({percentage:.2f}%)")

        print("-" * 40)

        # Match real-time video playback speed
        elapsed = time.time() - start_time
        if elapsed < frame_delay:
            time.sleep(frame_delay - elapsed)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()


# Run the function
count_specific_colors_realtime("Lucky_Charms_Diamond_Dancers.mp4", resize_width=480)