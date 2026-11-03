from ultralytics import YOLO
import cv2
import numpy as np
import torch
from torchvision.transforms import functional as F

device = "cuda"
if not torch.cuda.is_available():
    device = "cpu"

# load model default
model_path = r"best.pt"
model = YOLO(model_path)

#run hollow knight video

cap = cv2.VideoCapture("gameplay.mp4")
if not cap.isOpened():
    raise IOError("gameplay where bro")

#start
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture the next frame.")
        break

    results = model(frame, conf=0.5)  # prediksi dengan confidence threshold = 0.5

    for result in results:
        boxes = result.boxes

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()  # masih ternormalisasi [0, 1]
        conf_score = box.conf.item()
        cls_id = box.cls.item()
        cls_name = model.names[cls_id]

        cv2.rectangle(  #integers + rgb color + thickness
            frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2
        )
        cv2.putText(    #text
            frame, f"{cls_name} ({conf_score:.2f})",
            (int(x1), int(y1) - 10), 1, 1, (255, 255, 255)
        )

    cv2.imshow("info", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
