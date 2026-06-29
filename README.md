# Robust 3D Object Localization using ZED Stereo Camera

## Overview

This project presents a **real-time 3D object localization system** developed using the **ZED Stereo Camera**, **YOLOv8m**, and **point cloud processing**. The system estimates accurate real-world **X, Y, and Z coordinates (in millimeters)** of selected objects and is designed for robotic localization and automation applications.

The project supports both **YOLO-based object selection** and **manual ROI selection**, allowing localization even when the object is not detected by the object detector. Multiple filtering and stabilization techniques are incorporated to improve measurement accuracy and robustness.

---

# Features

* Real-time object detection using **YOLOv8m**
* ZED Stereo Camera based depth estimation
* Manual ROI fallback for undetected objects
* Point cloud extraction from selected object
* Depth-guided filtering for manual selection
* Bounding box stabilization
* Median filtering
* Kalman filtering
* Stability gate for stationary objects
* XYZ uncertainty estimation
* CSV logging of localization results
* Validation framework (MAE, RMSE, Accuracy)
* Arduino communication support

---

# System Pipeline

```text
ZED Stereo Camera
        ↓
RGB Frame + Depth Map
        ↓
YOLOv8m Object Detection
        ↓
YOLO Selection Mode
           OR
Manual ROI Mode
        ↓
Bounding Box Stabilization
        ↓
Point Cloud Extraction
        ↓
Depth Guided Filtering
        ↓
Outlier Removal
        ↓
XYZ Estimation
        ↓
Median Filtering
        ↓
Kalman Filtering
        ↓
Stability Gate
        ↓
Uncertainty Estimation
        ↓
Final Stable XYZ
        ↓
CSV Logging
        ↓
Arduino Communication
        ↓
Validation
```

---

# Folder Structure

```text
ZED-3D-Localization/
│
├── camera/
├── communication/
├── detection/
├── filters/
├── localization/
├── logger/
├── pointcloud/
├── target_selection/
├── utils/
├── validation/
├── main.py
├── requirements.txt
└── README.md
```

---

# Technologies Used

* Python
* ZED SDK
* OpenCV
* YOLOv8 (Ultralytics)
* NumPy
* PyZED SDK
* pySerial
* Arduino

---

# Validation Results

| Metric            | Value        |
| ----------------- | ------------ |
| Average Accuracy  | **98.94%**   |
| RMSE              | **3.58 mm**  |
| MAE               | Low          |
| Coordinate Output | X, Y, Z (mm) |

---

# Research Contributions

* Hybrid object selection using YOLO and manual ROI
* Detector-independent localization
* Point cloud based XYZ estimation
* Stability-aware coordinate estimation
* Uncertainty-aware localization
* Validation framework for quantitative performance evaluation
* Arduino integration for robotic applications

---

# Applications

* Industrial Robotics
* Pick-and-Place Automation
* Autonomous Systems
* Robotic Manipulators
* Object Localization
* Human–Robot Interaction
* Smart Manufacturing

---

# Future Work

* Multi-object tracking using ByteTrack
* Camera-to-robot coordinate transformation
* ROS 2 integration
* Web-based monitoring dashboard
* Deep learning based point cloud segmentation
* Multi-camera localization

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<YOUR_USERNAME>/ZED-3D-Localization.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

---

# Results

The system estimates stable real-world coordinates in millimeters:

```text
X = 145.2 mm
Y = -37.8 mm
Z = 502.4 mm
```

along with uncertainty estimates:

```text
X = 145.2 ± 1.1 mm
Y = -37.8 ± 0.8 mm
Z = 502.4 ± 2.4 mm
```

---

# Author

**Debdeep Ghosh**

B.Tech in Computer Science and Engineering

Machine Learning • Computer Vision • Robotics • 3D Vision
