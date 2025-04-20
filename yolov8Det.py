import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort.deep_sort import DeepSort
import time
import math
import os

# Configuration
RTSP_URL = "rtsp://admin:admin@192.168.1.9:1935/"
FRAME_WIDTH = 640  # Resize frame for faster processing
PPM = 100  # Pixels per meter (calibrate based on scene)
FPS = 15  # Assumed FPS for speed calculation (adjust if known)
SKIP_FRAMES = 2  # Process every 2nd frame to reduce load

# Initialize YOLOv8 model
model = YOLO("yolov8n.pt")  # Nano model for Raspberry Pi

# Initialize DeepSORT
deepsort = DeepSort(
    model_path="deep_sort/deep_checkpoint/ckpt.t7",  # Path to ReID model
    max_dist=0.2,
    min_confidence=0.3,
    nms_max_overlap=0.5,
    max_iou_distance=0.7,
    max_age=70,
    n_init=3,
    nn_budget=100,
    use_cuda=False  # CPU for Raspberry Pi
)

# Initialize video capture
cap = cv2.VideoCapture(
    f"rtspsrc location={RTSP_URL} ! decodebin ! videoconvert ! appsink",
    cv2.CAP_GSTREAMER
)

if not cap.isOpened():
    print("Error: Could not open RTSP stream")
    exit()

# Track history for direction and speed
track_history = {}  # {track_id: [(x, y, time), ...]}
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read frame")
        break

    frame_count += 1
    if frame_count % SKIP_FRAMES != 0:
        continue  # Skip frames to reduce load

    # Resize frame
    frame = cv2.resize(frame, (FRAME_WIDTH, int(frame.shape[0] * FRAME_WIDTH / frame.shape[1])))

    # YOLOv8 detection
    results = model(frame, classes=[0], conf=0.5)  # Class 0 = person
    detections = []
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        detections.append([x1, y1, x2 - x1, y2 - y1, conf])

    # Update DeepSORT
    detections = np.array(detections)
    tracks = deepsort.update(detections, frame)

    # Process tracks
    current_time = time.time()
    for track in tracks:
        x1, y1, x2, y2, track_id = track
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

        # Calculate centroid
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        # Initialize track history
        if track_id not in track_history:
            track_history[track_id] = []

        # Store current position and time
        track_history[track_id].append((cx, cy, current_time))

        # Keep only last 5 positions to save memory
        track_history[track_id] = track_history[track_id][-5:]

        # Calculate direction and speed
        direction = "Stationary"
        speed = 0.0
        if len(track_history[track_id]) >= 2:
            prev_cx, prev_cy, prev_time = track_history[track_id][-2]
            delta_x = cx - prev_cx
            delta_y = cy - prev_cy
            delta_time = current_time - prev_time

            # Direction
            if abs(delta_x) > 5 or abs(delta_y) > 5:  # Threshold to avoid noise
                if abs(delta_x) > abs(delta_y):
                    direction = "Right" if delta_x > 0 else "Left"
                else:
                    direction = "Down" if delta_y > 0 else "Up"

            # Speed (meters per second)
            distance_pixels = math.sqrt(delta_x**2 + delta_y**2)
            distance_meters = distance_pixels / PPM
            if delta_time > 0:
                speed = distance_meters / delta_time

        # Draw bounding box and annotations
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"ID {track_id} | {direction} | {speed:.2f} m/s"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display frame
    cv2.imshow("Person Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()