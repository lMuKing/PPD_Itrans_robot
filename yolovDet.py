import cv2
import numpy as np
import time

classNames = ["person"]

# Load YOLOv3 model
configPath = "/home/robot2325/Desktop/Object_Detection_Files/yolov3.cfg"
weightsPath = "/home/robot2325/Desktop/Object_Detection_Files/yolov3.weights"
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# Set backend for potential optimization
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # Use DNN_TARGET_CUDA for GPU

# Cache layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def getObjects(img, thres=0.45, nms=0.2, draw=True, objects=None):
    """
    Optimized object detection using YOLOv3, with optional class filtering.
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
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > thres:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                x = max(0, min(x, width - 1))
                y = max(0, min(y, height - 1))
                w = min(w, width - x)
                h = min(h, height - y)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    objectInfo = []
    if boxes:
        indices = cv2.dnn.NMSBoxes(boxes, confidences, thres, nms)

        target_objects = set(objects if objects else classNames)

        for i in indices:
            i = i if isinstance(i, np.int32) else i[0]
            box = boxes[i]
            class_id = class_ids[i]
            class_name = classNames[class_id]

            if class_name in target_objects:
                objectInfo.append([box, class_name])
                if draw:
                    cv2.rectangle(img, (box[0], box[1], box[2], box[3]), color=(0, 255, 0), thickness=2)
                    label = f"{class_name.upper()} {confidences[i]*100:.2f}%"
                    cv2.putText(
                        img,
                        label,
                        (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )

    return img, objectInfo

if __name__ == "__main__":
    rtsp_url = "rtsp://admin:admin@192.168.1.9:1935/"
    cap = cv2.VideoCapture(rtsp_url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break

        img = cv2.resize(img, (640, 480))
        # Detect only humans
        result, objectInfo = getObjects(img, thres=0.45, nms=0.2, objects=["person"])
        print(objectInfo)

        cv2.imshow("Output", result)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
