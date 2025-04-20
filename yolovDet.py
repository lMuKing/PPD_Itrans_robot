import cv2
import numpy as np
import time

# Load YOLOv3 model
configPath = "/home/robot2325/Desktop/Object_Detection_Files/yolov3.cfg"
weightsPath = "/home/robot2325/Desktop/Object_Detection_Files/yolov3.weights"
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# Optimize for CPU
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # Switch to DNN_TARGET_CUDA for GPU

# Cache output layers
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def detect_persons(img, conf_thres=0.5, nms_thres=0.4):
    """
    Optimized person detection using YOLOv3.
    Returns image with bounding boxes and list of person detections.
    """
    t_start = time.time()
    height, width = img.shape[:2]

    # Prepare input blob
    blob = cv2.dnn.blobFromImage(img, scalefactor=1/255.0, size=(416, 416), swapRB=False, crop=False)
    net.setInput(blob)

    # Forward pass
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []

    # Process detections, only for person
    for output in outputs:
        for detection in output:
            confidence = detection[5]  # Person class (index 5, class_id 0)
            if confidence > conf_thres:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = max(0, min(int(center_x - w / 2), width - 1))
                y = max(0, min(int(center_y - h / 2), height - 1))
                w = min(w, width - x)
                h = min(h, height - y)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))

    # Apply NMS
    person_detections = []
    if boxes:
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_thres, nms_thres)
        for i in indices:
            i = i if isinstance(i, np.int32) else i[0]
            box = boxes[i]
            person_detections.append(box)
            # Draw bounding box and confidence
            cv2.rectangle(img, (box[0], box[1], box[2], box[3]), color=(0, 255, 0), thickness=2)
            label = f"PERSON {confidences[i]*100:.1f}%"
            cv2.putText(img, label, (box[0] + 5, box[1] + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    

    return img, person_detections

if __name__ == "__main__":
    rtsp_url = "rtsp://admin:admin@192.168.1.23:1935/"
    cap = cv2.VideoCapture(rtsp_url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break

        img = cv2.resize(img, (640, 480))
        result, detections = detect_persons(img)
        print(f"Persons detected: {len(detections)}")

        cv2.imshow("Person Detection", result)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
