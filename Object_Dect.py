import cv2 # OpenCV for video capture and image processing.
import numpy as np # NumPy for array operations (used for drawing QR code boundaries).


classNames = [] # Initializes an empty list for class names.
classFile = "/home/robot2325/Desktop/Object_Detection_Files/coco.names"  # Full path to coco which contains object class labels (e.g., "person", "car").
with open(classFile, "rt") as f:  # Opens and reads the file
    classNames = f.read().rstrip("\n").split("\n")  # removing trailing newlines and splitting into a list of class names.




# Load model
configPath = "/home/robot2325/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"  # This is a text file that describes the blueprint of the SSD MobileNet V3 model.
# It tells the computer how the model is built, like which layers it has and how they connect .

weightsPath = "/home/robot2325/Desktop/Object_Detection_Files/frozen_inference_graph.pb"  # This file contains the knowledge the model learned during training.
#  It stores numbers (weights) that help the model recognize objects like "person" or "car." It’s like the model’s brain.


net = cv2.dnn_DetectionModel(weightsPath, configPath)  # This line uses OpenCV to combine the blueprint (.pbtxt) and the knowledge (.pb) to create a working model.
# The model is now ready to look at images or videos, find objects, and label them with boxes.



net.setInputSize(320, 320) # Sets input image size to 320x320 pixels.
net.setInputScale(1.0 / 127.5)  # Scales pixel values by dividing by 127.5.
net.setInputMean((127.5, 127.5, 127.5)) # 
net.setInputSwapRB(True)

def getObjects(img, thres=0.45, nms=0.2, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    objectInfo = []
    if len(objects) == 0:
        objects = classNames
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className])
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(
                        img,
                        f"{classNames[classId-1].upper()} {round(confidence*100,2)}%",
                        (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                    )
    return img, objectInfo

if __name__ == "__main__":
    rtsp_url = "rtsp://admin:DZ12345678@192.168.1.95:554/cam/realmonitor?channel=1&subtype=0"
    cap = cv2.VideoCapture(rtsp_url)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to grab frame")
            break

        img = cv2.resize(img, (640, 480))
        result, objectInfo = getObjects(img, thres=0.45, nms=0.2)
        print(objectInfo)

        cv2.imshow("Output", result)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()