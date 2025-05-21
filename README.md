# PPD_Itrans_robot

![Project Banner](.)

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)


## 📋 Overview
This project delivers real-time object detection and QR code scanning capabilities using a Dahua IP camera and Python. With powerful computer vision integration, the system can identify various objects and decode QR codes instantly from live video feeds.

## ✨ Key Features
* **Real-time object detection** using pre-trained MobileNet SSD model
* **QR code scanning and decoding** with immediate content extraction
* **Seamless integration** with Dahua IP cameras via RTSP stream
* **Interactive visual display** with bounding boxes and labels
* **Dual functionality** through specialized scripts for different detection needs
* **Terminal output** of detected objects or QR code content
* **Lightweight implementation** for efficient performance

## 📸 Usage Examples

![Object Detection Example](https://via.placeholder.com/400x300?text=Object+Detection+Demo)
![QR Code Scanning Example](https://via.placeholder.com/400x300?text=QR+Code+Scanning+Demo)

## 🔧 Requirements

### 🐍 Python Version
* Python 3.6 

### 📦 Required Model Files
You must download and extract the following zip file into your project folder:
[Object Detection Files](https://core-electronics.com.au/media/kbase/491/Object_Detection_Files.zip)

The zip file contains these essential components:
* `coco.names`: Comprehensive list of 80+ object class names (person, car, chair, etc.)
* `ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt`: Model architecture configuration file
* `frozen_inference_graph.pb`: Pre-trained model weights optimized for detection tasks

### 📚 Required Python Libraries
```bash
# Core dependencies
pip install opencv-python    # Computer vision library for image processing
pip install numpy           # Numerical computing for efficient array operations
pip install pyzbar          # QR code and barcode detection and decoding
```
