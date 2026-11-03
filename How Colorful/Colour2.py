import cv2
import numpy as np
from collections import Counter
import time


def print_all_colors_realtime(video_path, bin_size, resize_width):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video file.")
        return

    print("Starting real-time full color display. Press Ctrl+C to stop...\n")

    frame_count = 0

    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("\nEnd of video reached.")
            break

        frame_count += 1

        # Resize frame for performance
        h, w = frame.shape[:2]
        #resize
        new_height = int(h * (resize_width / w)) # to match ratio with the width
        resized = cv2.resize(frame, (resize_width, new_height))

        # Convert to HSV
        hsv_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        # Quantize colors to keep the list readable per frame
        quantized = (hsv_frame // bin_size) * bin_size

        # Flatten and count pixels for THIS frame only
        pixels = quantized.reshape(-1, 3)
        frame_counts = Counter(map(tuple, pixels))
        total_pixels = pixels.shape[0]

        # Print header for the current frame
        print(f"=== Frame {frame_count} (Total Unique Colors: {len(frame_counts)}) ===")

        # by using enum(.most_common(n),1) it will sort from top to bottom
        isolated_frames = [] #for frames
        for rank, (hsv_color, count) in enumerate(frame_counts.most_common(5), 1):
            percentage = (count / total_pixels) * 100

            h_value = int(hsv_color[0])
            s_value = int(hsv_color[1])
            v_value = int(hsv_color[2])

            print(f"  HSV: {h_value} {s_value} {v_value} | Pixels: {count:,} ({percentage:.2f}%)")

            #updating colors
            lower_bound = np.array([h_value, s_value, v_value])
            upper_bound = np.array([h_value + bin_size - 1, min(s_value + bin_size, 255), min(v_value + bin_size, 255)])

            mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)

            frame_iso = cv2.bitwise_and(resized, resized, mask=mask)

            isolated_frames.append(frame_iso)

        print("-" * 50)

        top5_iso = np.hstack(isolated_frames)
        cv2.imshow("Original Frame", resized)
        cv2.imshow("Top Color #1 Isolated", isolated_frames[0])
        cv2.imshow("Top Color #2 Isolated", isolated_frames[1])
        cv2.imshow("Top Color #3 Isolated", isolated_frames[2])
        cv2.imshow("Top Color #4 Isolated", isolated_frames[3])
        cv2.imshow("Top Color #5 Isolated", isolated_frames[4])

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()


# Run the real-time function[cite: 1]
print_all_colors_realtime("Lucky_Charms_Diamond_Dancers.mp4", bin_size=32, resize_width=480)