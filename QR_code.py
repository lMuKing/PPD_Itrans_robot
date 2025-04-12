import cv2  # OpenCV for video capture and image processing.
from pyzbar.pyzbar import decode # decode function from pyzbar to detect and decode QR codes.
import numpy as np # NumPy for array operations (used for drawing QR code boundaries).

# Replace with your Dahua camera's RTSP stream
url = "rtsp://admin:DZ12345678@192.168.1.95:554/cam/realmonitor?channel=1&subtype=0"

cap = cv2.VideoCapture(url)

while True: # Starts an infinite loop to process video frames continuously.
   
    ret, frame = cap.read() # Reads a frame from the video stream; ret is a boolean (True if frame is read), frame is the image.

    if not ret:
        print("Failed to grab frame")
        break


    for obj in decode(frame): # to loops through any QR codes detected in the frame using pyzbar’s decode.

        data = obj.data.decode("utf-8") # extracts the content of a QR code and converts it into a readable string.
        print("QR Code Detected:", data) # print in terminal

        # Draw rectangle around the QR

        points = obj.polygon # Gets the corner points of the QR code’s boundar

        if len(points) == 4:  # Checks if the QR code has 4 corner points

            pts = np.array([[p.x, p.y] for p in points], np.int32)  # Converts the points to a NumPy array of (x, y) coordinates for OpenCV.

            cv2.polylines(frame, [pts], True, (0, 255, 0), 3) # Draws a green (0, 255, 0) rectangle around the QR code with thickness 3.
    
    resized_frame = cv2.resize(frame, (500, 360)) # Resizes the frame to 500x360 pixels for display.

    cv2.imshow("QR Reader", resized_frame) # Displays the resized frame in a window named "QR Reader".

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()