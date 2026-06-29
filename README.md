# 🎯 Robust 3D Object Localization using ZED Stereo Camera

![Python](https://img.shields.io/badge/Python-3.11-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Demo-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Overview

This repository presents a **real-time 3D object localization system** developed using the **ZED Stereo Camera**, **YOLOv8m**, and **point cloud processing**. The system estimates accurate real-world **X, Y, and Z coordinates (in millimeters)** of selected objects and is designed for robotic localization, industrial automation, and computer vision research.

The project supports both **YOLO-based object selection** and **manual ROI selection**, enabling localization even when the object detector fails to detect the target.

---

# ✨ Key Features

* 🎯 Real-time object detection using YOLOv8m
* 📷 ZED Stereo Camera based depth estimation
* 🖱️ Manual ROI fallback for undetected objects
* ☁️ Point cloud extraction
* 📏 Depth-guided filtering
* 📦 Bounding box stabilization
* 📊 Median filtering
* ⚙️ Kalman filtering
* 🔒 Stability gate for stationary objects
* 📈 XYZ uncertainty estimation
* 📝 CSV logging
* 📉 Validation framework (MAE, RMSE, Accuracy)
* 🤖 Arduino communication
* 🌐 Interactive Streamlit demo

---

# ⚙️ Complete Pipeline

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
XYZ + Uncertainty Estimation
        ↓
CSV Logging
        ↓
Arduino Communication
        ↓
Validation
```

---

# 📁 Repository Structure

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
│
├── Resume_Demo/
│   ├── app.py
│   ├── requirements.txt
│   ├── graphs/
│   ├── screenshots/
│   ├── videos/
│   └── validation_report.csv
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

---

# 🛠 Technologies Used

* Python
* OpenCV
* NumPy
* Ultralytics YOLOv8m
* ZED SDK
* PyZED SDK
* Streamlit
* Matplotlib
* Pandas
* Arduino
* Git & GitHub

---

# 📊 Experimental Results

| Metric                |                        Value |
| --------------------- | ---------------------------: |
| Average Accuracy      |                   **98.94%** |
| RMSE                  |                  **3.58 mm** |
| Tested Distance Range |               **100–600 mm** |
| Output                | **X, Y, Z Coordinates (mm)** |

---

# 🔬 Research Contributions

* Hybrid target selection using **YOLO detection** and **manual ROI fallback**.
* Detector-independent localization for undetected objects.
* Depth-guided point cloud processing.
* Stability-aware coordinate estimation using Median + Kalman filtering.
* XYZ uncertainty estimation for localization confidence.
* Quantitative validation framework using MAE, RMSE, and accuracy.
* Arduino integration for robotic applications.

---

# 🚀 Applications

* Industrial Robotics
* Pick-and-Place Automation
* Smart Manufacturing
* Human–Robot Interaction
* Autonomous Systems
* Object Localization
* Computer Vision Research

---

# 🔮 Future Scope

* Multi-object tracking using ByteTrack
* Camera-to-robot coordinate transformation
* ROS 2 integration
* Deep learning based point cloud segmentation
* Multi-camera localization
* Real-time web dashboard

---

# 💻 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ZED-3D-Localization.git
```

Move into the project:

```bash
cd ZED-3D-Localization
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the localization system:

```bash
python main.py
```

---

# 🌐 Streamlit Demonstration

An interactive Streamlit application is included inside the **Resume_Demo** folder.

Launch it locally using:

```bash
cd Resume_Demo
streamlit run app.py
```

After deployment, the live demo URL can be added here.

---

# 📷 Demo

The Streamlit application showcases:

* Project overview
* System pipeline
* Performance metrics
* Validation results
* Graphical analysis
* Screenshots
* Demonstration videos

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

**Debdeep Ghosh**

B.Tech – Computer Science & Engineering

**Areas of Interest**

* Computer Vision
* Machine Learning
* Robotics
* 3D Vision
* Artificial Intelligence

---

⭐ If you find this project useful, consider giving it a **star** on GitHub.
