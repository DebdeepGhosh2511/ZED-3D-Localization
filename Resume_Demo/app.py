import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ZED 3D Localization",
    page_icon="🎯",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.hero {
    padding: 35px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #0891b2);
    color: white;
    margin-bottom: 25px;
}
.card {
    padding: 22px;
    border-radius: 18px;
    background-color: #161b22;
    border: 1px solid #30363d;
    color: white;
}
.metric-card {
    padding: 20px;
    border-radius: 16px;
    background: #111827;
    border: 1px solid #374151;
    text-align: center;
}
.small-text {
    color: #9ca3af;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>🎯 Robust 3D Object Localization System</h1>
    <h2>ZED Stereo Camera + YOLOv8m + Point Cloud Processing + Arduino Communication</h2>
    <p>
    A real-time 3D localization system that estimates stable X, Y, Z coordinates
    of objects using stereo vision, object detection, filtering, uncertainty estimation,
    and validation analytics.
    </p>
</div>
""", unsafe_allow_html=True)

st.warning("Demo Mode Enabled — No ZED Camera Connected")

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accuracy", "98.94%")

with col2:
    st.metric("RMSE", "3.58 mm")

with col3:
    st.metric("Range Tested", "100–600 mm")

with col4:
    st.metric("Model", "YOLOv8m")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Demo Videos",
    "Screenshots",
    "Validation",
    "Pipeline"
])

# ---------------- OVERVIEW ----------------
with tab1:
    st.header("Project Overview")

    st.markdown("""
    This project performs **real-time 3D object localization** using a ZED stereo camera.
    It supports both **YOLO-based object selection** and **manual ROI fallback** for objects
    that are not detected by YOLO.

    ### Key Features
    - ZED stereo camera based depth sensing
    - YOLOv8m object detection
    - Manual ROI mode for undetected objects
    - Depth-guided point cloud extraction
    - DBSCAN segmentation
    - Outlier removal
    - Median + Kalman filtering
    - Stability gate for stationary objects
    - XYZ uncertainty estimation
    - CSV logging and validation
    - Arduino coordinate communication
    """)

    st.success(
        "Final Output: Stable real-world X, Y, Z coordinates in millimeters."
    )

# ---------------- VIDEOS ----------------
with tab2:
    st.header("Project Demo Videos")

    videos = {
        "YOLO Detection": "Resume_Demo/videos/YoloDetection_video.mp4",
        "Manual ROI Selection": "Resume_Demo/videos/manual_roi_video.mp4",
        "Coordinate Detection using Arduino": "Resume_Demo/videos/coordinate_detectionusing_Arduino.mp4",
        "Arduino Setup": "Resume_Demo/videos/aurdino_setup.mp4"
    }

    for title, path in videos.items():
        st.subheader(title)
        if os.path.exists(path):
            st.video(path)
        else:
            st.info(f"Video not found: {path}")

# ---------------- SCREENSHOTS ----------------
with tab3:
    st.header("Screenshots")

    screenshots = [
        ("YOLO Detection", "Resume_Demo/screenshots/yolodetection.jpeg"),
        ("Manual ROI", "Resume_Demo/screenshots/manual_roi.jpeg"),
        ("XYZ Estimation", "Resume_Demo/screenshots/xyz_estimation.jpeg"),
        ("Object at 100 mm", "Resume_Demo/screenshots/object_100mm.jpeg"),
        ("Object at 200 mm", "Resume_Demo/screenshots/object_200mm.jpeg"),
        ("Object at 300 mm", "Resume_Demo/screenshots/object_300mm.jpeg"),
        ("Object at 400 mm", "Resume_Demo/screenshots/object_400mm.jpeg"),
        ("Object at 500 mm", "Resume_Demo/screenshots/object_500mm.jpeg"),
    ]

    cols = st.columns(2)

    for i, (caption, path) in enumerate(screenshots):
        with cols[i % 2]:
            if os.path.exists(path):
                st.image(path, caption=caption, use_container_width=True)
            else:
                st.info(f"Missing: {path}")

# ---------------- VALIDATION ----------------
with tab4:
    st.header("Validation Results")

    csv_path = "validation_report.csv"

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.dataframe(df, use_container_width=True)
    else:
        actual = [100, 200, 300, 400, 500, 600]
        predicted = [102.8, 201.0, 302.4, 399.2, 494.3, 605.4]

        df = pd.DataFrame({
            "Actual_Z_mm": actual,
            "Predicted_Z_mm": predicted
        })

        df["Absolute_Error_mm"] = abs(df["Actual_Z_mm"] - df["Predicted_Z_mm"])
        df["Accuracy_%"] = (1 - df["Absolute_Error_mm"] / df["Actual_Z_mm"]) * 100

        st.dataframe(df, use_container_width=True)

    st.subheader("Validation Graphs")

    graph_cols = st.columns(3)

    graphs = [
        ("Actual vs Predicted", "graphs/actual_vs_predicted.png"),
        ("Absolute Error", "graphs/abserror_atdiffdist.png"),
        ("Accuracy vs Distance", "graphs/accuracyvsdistance.png")
    ]

    for col, (title, path) in zip(graph_cols, graphs):
        with col:
            st.markdown(f"### {title}")
            if os.path.exists(path):
                st.image(path, use_container_width=True)
            else:
                st.info(f"Missing: {path}")

    if os.path.exists(csv_path):
        with open(csv_path, "rb") as file:
            st.download_button(
                label="Download Validation Report",
                data=file,
                file_name="validation_report.csv",
                mime="text/csv"
            )

# ---------------- PIPELINE ----------------
with tab5:
    st.header("Complete System Pipeline")

    st.code("""
ZED Stereo Camera
        ↓
RGB Frame + Depth Map
        ↓
YOLOv8m Object Detection
        ↓
YOLO Selection Mode OR Manual ROI Mode
        ↓
Depth-Guided Point Cloud Extraction
        ↓
DBSCAN Segmentation
        ↓
Outlier Removal
        ↓
Center-Based XYZ Estimation
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
Validation Analytics
""")

    st.header("Research Contributions")

    st.markdown("""
    - **Hybrid selection system:** YOLO mode + manual ROI fallback.
    - **Detector-independent localization:** works even when YOLO misses an object.
    - **Depth-guided filtering:** prevents table/background contamination.
    - **DBSCAN point-cloud segmentation:** isolates the target object.
    - **Stability gate:** freezes coordinates for stationary objects.
    - **Uncertainty-aware output:** reports XYZ with confidence range.
    - **Validation framework:** RMSE, accuracy, and error analysis.
    """)

st.markdown("---")
st.caption("Developed by Debdeep Ghosh | ZED Stereo Vision 3D Localization Project")