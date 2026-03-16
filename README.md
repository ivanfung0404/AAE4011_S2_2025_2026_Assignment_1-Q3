# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

> **Student Name:** FUNG Tsan Wai | **Student ID:** 25120771D | **Date:** 15-3-2026

---

## 1. Overview

*This project implements a complete, real-time vehicle detection pipeline wrapped in a ROS Noetic package. It reads compressed image messages from a provided rosbag, processes them by deep learning object detection model, and displays the results of real-time statistics in Tkinter dashboard.*


## 2. Detection Method *(Q3.1 — 2 marks)*

*I chose the **YOLOv8 Nano** model for the pipeline. It is because YOLOv8 Nano have an outstanding performance in high-speed inference and efficiency. Also, since the environment runs inside a WSL2 virtual machine, YOLOv8 is friendly for this situation which can be run easily. So it is suitable for this project which is real-time and resource-constrained applications*

## 3. Repository Structure
```
vehicle_detector_pkg/
│
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── vehicle_detection.launch      # Launch file to start the ROS node
└── src/
    └── vehicle_detection.py          # Main Python script (extraction, YOLO, and UI)
```
## 4. Prerequisites

- OS: Ubuntu 20.04 (native or via WSL2)
- ROS: ROS 1 Noetic
- Python: Python 3.8+
- Core libraries:
  - rospy, rosbag
  - opencv-python (cv2)
  - numpy
  - Pillow (PIL)
  - ultralytics (YOLOv8)
  - tkinter, ttk

## 5. How to Run *(Q3.1 — 2 marks)*

Ensure that you have set up the ROS 1 Noetic environment with Ubuntu 20.04 and opened a terminal before following the steps. Type the command below step by step

1. Clone the repository
   ```
   cd ~/catkin_ws/src
   git clone https://github.com/ivanfung0404/AAE4011_S2_2025_2026_Assignment_1-Q3/tree/main/vehicle_detector_pkg
   ```
2. Install dependencies
   ```
   sudo apt update
   sudo apt install python3-pip
   pip3 install ultralytics pillow numpy opencv-python
   ```
3. Build the workspace
   ```
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash
   ```
4. Place the rosbag file

   Open src/vehicle_detection.py and update the bag_path variable to match your local absolute path:
   ```
   bag_path = '/path/to/your/downloaded/2026-02-23-15-58-29.bag'
   ```
5. Launch the pipeline
   ```
   cd ~/catkin_ws
   source devel/setup.bash
   roslaunch vehicle_detector_pkg vehicle_detection.launch
   ```
## 6. Sample Results

- Image extraction summary
  - Total frames: 1122
  - Resolution: 2200 x 1740
  - Topic name: `/hikcamera/image_1/compressed`

- Detection results screenshot:
  ![Vehicle Detection Dashboard](ui_result_sceenshot.png)
  

## 7. Video Demonstration *(Q3.2 — 5 marks)*

**Video Link:** https://youtu.be/SwM3xvqDMK0

## 8. Reflection & Critical Analysis *(Q3.3 — 8 marks, 300–500 words)*

### (a) What Did You Learn? *(2 marks)*

The two primary technical skills or concept I gained are What is Ros environment and practical experience in ROS data processing and manipulation. First, I learned that the Robot Operating System is a set of software libraries open source software libraries and tools that help to build robot applications. Second, I learned how to extract, decode, and handle data from a rosbag file using the libraries to develop a Python application after this assignment.

### (b) How Did You Use AI Tools? *(2 marks)*

I used AI assistants as a programming tool and a teacher to help me learn new skills and concepts. I asked the AI to help me write the Python script and adjust it until fulfil the requirement. For the benefits of using AI, It is helpful for programming. It can generate the script very fast and with a fully functional application. At the same time, the limitation is that AI will sometimes give me some outdated or wrong information. I need the verify it by myself to ensure I mix up the concepts.
 
### (c) How to Improve Accuracy? *(2 marks)*

1. Use the latest version, fully trained model. I find out that the current YOLOv8 Nano model has a low accuracy in vehicle detection. It will mix up the type of the vehicle such as bus and truck during the detection. Using the latest version like YOLO26 which is released in January 2026 can help to improve the accuracy.

2. Provide a high resolution images. Processing higher-resolution images from the camera can improve detection accuracy. It can provide more detailed pixel data and clearer edge features make the model have a high accuracy during the detection.

### (d) Real-World Challenges *(2 marks)*

1. The limits of the environment. There are some factors that affect the application like sudden changes in lighting, vibrations, rain and fog that degrade image quality. It will make the pipeline unusable.

2. Power Consumption and Battery Drain. The heavy computational load will drain the drone’s battery much faster that reduce its maximum flight time and operational range.

## 9. References

- Ultralytics YOLOv8: https://github.com/ultralytics/ultralytics

- ROS Noetic Documentation: http://wiki.ros.org/noetic

- Tkinter/TTK Styling: Python Software Foundation
