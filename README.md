# AAE4011 Assignment 1 — Q3: ROS-Based Vehicle Detection from Rosbag

> **Student Name:** [FUNG Tsan Wai] | **Student ID:** [25120771D] | **Date:** [15-3-2026]

---

## 1. Overview

*This project implements a complete, real-time vehicle detection pipeline wrapped in a ROS Noetic package. It reads compressed image messages from a provided rosbag, processes them by deep learning object detection model, and displays the results of real-time statistics in Tkinter dashboard.*


## 2. Detection Method *(Q3.1 — 2 marks)*

*I chose the the **YOLOv8 Nano** model for the pipeline. Because YOLOv8 Nano effectively serves as an object detector for real-time traffic management.*

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

*Provide clear, step-by-step instructions:*

1. Clone the repository
2. Install dependencies
3. Build the ROS package
4. Place the rosbag file
5. Launch the pipeline

## 6. Sample Results

*Include:*
- Image extraction summary (total frames, resolution, topic name)
- Detection results (sample screenshot, detection statistics)

## 7. Video Demonstration *(Q3.2 — 5 marks)*

**Video Link:** [YouTube (Unlisted)](https://youtu.be/your-link-here)

*The video (1–3 min) should show:*
- (a) Launching the ROS package
- (b) The UI displaying detection results
- (c) A brief explanation of the results

## 8. Reflection & Critical Analysis *(Q3.3 — 8 marks, 300–500 words)*

### (a) What Did You Learn? *(2 marks)*

*Identify at least two specific technical skills or concepts you gained.*

### (b) How Did You Use AI Tools? *(2 marks)*

*Describe how you used AI assistants. Discuss both benefits and limitations. If you did not use any, explain your alternative approach.*

### (c) How to Improve Accuracy? *(2 marks)*

*Propose two concrete strategies to improve detection accuracy and explain why each would help.*

### (d) Real-World Challenges *(2 marks)*

*Discuss two challenges of deploying this pipeline on an actual drone in real time.*

## 9. References

*List any references, libraries, or datasets used.*
