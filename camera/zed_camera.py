import os

os.add_dll_directory(r"C:\Program Files (x86)\ZED SDK\bin")

import cv2
import pyzed.sl as sl

class ZEDCamera:
    def __init__(self):
        self.zed = sl.Camera()
        self.image = sl.Mat()
        self.point_cloud = sl.Mat()
        self.runtime_params = sl.RuntimeParameters()

    def open(self):
        init_params = sl.InitParameters()
        init_params.camera_resolution = sl.RESOLUTION.HD720
        init_params.camera_fps = 30
        init_params.depth_mode = sl.DEPTH_MODE.NEURAL
        init_params.coordinate_units = sl.UNIT.MILLIMETER

        status = self.zed.open(init_params)

        if status != sl.ERROR_CODE.SUCCESS:
            print("[ERROR] Failed to open ZED Camera:", status)
            return False

        print("[OK] ZED Camera Opened")
        return True

    def get_intrinsics(self):
        calib = (
            self.zed.get_camera_information()
            .camera_configuration
            .calibration_parameters
            .left_cam
        )

        return {
            "fx": calib.fx,
            "fy": calib.fy,
            "cx": calib.cx,
            "cy": calib.cy
        }

    def get_frame_and_point_cloud(self):
        if self.zed.grab(self.runtime_params) != sl.ERROR_CODE.SUCCESS:
            return None, None

        self.zed.retrieve_image(self.image, sl.VIEW.LEFT)
        self.zed.retrieve_measure(self.point_cloud, sl.MEASURE.XYZ)

        frame = self.image.get_data()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        return frame, self.point_cloud

    def close(self):
        self.zed.close()
        print("[OK] ZED Camera Closed")