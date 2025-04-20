# PPD_Itrans_robot 

This project allows you to detect objects and QR codes in real-time using a Dahua IP camera and Python.
There are two main scripts: one for object detection and another for QR code scanning.
It uses a pre-trained MobileNet SSD model for object detection.
Results are shown in a display window, with object names or QR code content printed in the terminal.

Required Python Version:
Python 3

Download Required Model Files:
You must download and extract the following zip file into your project folder:
https://core-electronics.com.au/media/kbase/491/Object_Detection_Files.zip

The zip file contains:

coco.names: a list of object class names (e.g. person, car, etc.)

ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt: the model configuration file

frozen_inference_graph.pb: the pre-trained model weights

Install Required Python Libraries:

pip install opencv-python
This installs OpenCV for image and video processing.

pip install numpy
This installs NumPy for working with arrays and image data.

pip install pyzbar
This installs the pyzbar library used in QR_code.py for QR code detection.

Project Files:

Object_Dect.py
This script loads the object detection model and connects to the Dahua RTSP stream to detect and label objects in real time.

QR_code.py
This script connects to the same RTSP stream and detects QR codes using pyzbar. It draws boxes around detected QR codes and prints their content.
