import cv2

from camera.zed_camera import ZEDCamera
from detection.yolo_detector import YOLODetector
from target_selection.object_selector import ObjectSelector
from target_selection.click_roi import ClickROI
from pointcloud.point_extractor import PointCloudExtractor
from localization.xyz_estimator import XYZEstimator
from localization.uncertainty_estimator import UncertaintyEstimator
from filters.median_xyz import MedianXYZ
from filters.kalman_xyz import KalmanXYZ
from filters.bbox_smoother import BBoxSmoother
from filters.stability_gate import StabilityGate
from utils.visualization import Visualizer
from logger.csv_logger import CSVLogger


clicked_point = None
selection_mode = "YOLO"   # YOLO or MANUAL


def mouse_callback(event, x, y, flags, param):
    global clicked_point

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f"[CLICK] Pixel selected: ({x}, {y})")


def get_bbox_center(bbox):
    x1, y1, x2, y2 = bbox
    return (x1 + x2) // 2, (y1 + y2) // 2


def main():
    global clicked_point, selection_mode

    camera = ZEDCamera()

    if not camera.open():
        return

    intrinsics = camera.get_intrinsics()
    print("[OK] Camera Intrinsics:", intrinsics)

    detector = YOLODetector()
    selector = ObjectSelector()
    click_roi = ClickROI(roi_size=60)

    extractor = PointCloudExtractor(step=3, central_ratio=0.30)
    estimator = XYZEstimator()

    median_filter = MedianXYZ(window_size=30)
    kalman_filter = KalmanXYZ()
    bbox_smoother = BBoxSmoother(window_size=8)

    # Stronger freeze behavior for stationary objects
    stability_gate = StabilityGate(window_size=30, movement_threshold=12)

    uncertainty_estimator = UncertaintyEstimator(window_size=10)

    visualizer = Visualizer()
    logger = CSVLogger()

    window_name = "ZED 3D Localization"

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    last_detection = None
    last_xyz = None
    last_uncertainty = None

    print("Controls:")
    print("Y = YOLO selection mode")
    print("M = Manual ROI mode")
    print("Left Click = Select target")
    print("R = Reset")
    print("S = Save XYZ + Uncertainty")
    print("Q = Quit")

    while True:
        frame, point_cloud = camera.get_frame_and_point_cloud()

        if frame is None or point_cloud is None:
            continue

        frame_height, frame_width = frame.shape[:2]
        detections = detector.detect(frame)

        if clicked_point is not None:
            click_x, click_y = clicked_point

            if selection_mode == "YOLO":
                selected = selector.select_by_click(
                    detections,
                    click_x,
                    click_y
                )

                if selected is None:
                    roi_bbox = click_roi.create_roi(
                        click_x,
                        click_y,
                        frame_width,
                        frame_height
                    )

                    selected = selector.select_manual_roi(
                        roi_bbox,
                        click_x,
                        click_y
                    )

            else:
                roi_bbox = click_roi.create_roi(
                    click_x,
                    click_y,
                    frame_width,
                    frame_height
                )

                selected = selector.select_manual_roi(
                    roi_bbox,
                    click_x,
                    click_y
                )

            median_filter.reset()
            kalman_filter.reset()
            bbox_smoother.reset()
            stability_gate.reset()
            uncertainty_estimator.reset()

            clicked_point = None

        selected_detection = selector.get_selected(detections)

        frame = visualizer.draw_all_detections(frame, detections)

        stable_xyz = None
        uncertainty = None

        if selected_detection is not None:
            if selector.mode == "YOLO":
                smoothed_bbox = bbox_smoother.update(
                    selected_detection["bbox"]
                )

                selected_detection["bbox"] = smoothed_bbox
                selected_detection["center"] = get_bbox_center(smoothed_bbox)

                points = extractor.extract_points(
                    point_cloud,
                    smoothed_bbox,
                    use_central_region=True
                )

                center = selected_detection["center"]

            else:
                bbox = selected_detection["bbox"]
                selected_detection["center"] = get_bbox_center(bbox)

                points = extractor.extract_points_depth_guided(
                    point_cloud,
                    bbox,
                    selected_detection["click_point"],
                    depth_band=25
                )

                center = selected_detection["click_point"]

            raw_xyz = estimator.estimate_from_center(
                points,
                center,
                intrinsics
            )

            median_xyz = median_filter.update(raw_xyz)
            kalman_xyz = kalman_filter.update(median_xyz)

            # This freezes XYZ once object is stationary.
            stable_xyz = stability_gate.update(kalman_xyz)

            uncertainty = uncertainty_estimator.update(median_xyz)

            last_detection = selected_detection
            last_xyz = stable_xyz
            last_uncertainty = uncertainty

            frame = visualizer.draw_selected(
                frame,
                selected_detection,
                stable_xyz,
                uncertainty=uncertainty,
                mode=selector.mode
            )

            if stable_xyz is not None:
                X, Y, Z = stable_xyz

                if uncertainty is not None:
                    ux, uy, uz = uncertainty

                    print(
                        f"{selector.mode} | "
                        f"{selected_detection['class_name']} | "
                        f"X={X:.1f}±{ux:.1f} mm, "
                        f"Y={Y:.1f}±{uy:.1f} mm, "
                        f"Z={Z:.1f}±{uz:.1f} mm"
                    )

                else:
                    print(
                        f"{selector.mode} | "
                        f"{selected_detection['class_name']} | "
                        f"X={X:.1f} mm, "
                        f"Y={Y:.1f} mm, "
                        f"Z={Z:.1f} mm"
                    )

        frame = visualizer.draw_instructions(frame)

        cv2.putText(
            frame,
            f"Selection Mode: {selection_mode}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("y"):
            selection_mode = "YOLO"
            print("[MODE] YOLO selection mode")

        elif key == ord("m"):
            selection_mode = "MANUAL"
            print("[MODE] Manual ROI mode")

        elif key == ord("r"):
            selector.clear_selection()
            median_filter.reset()
            kalman_filter.reset()
            bbox_smoother.reset()
            stability_gate.reset()
            uncertainty_estimator.reset()

            last_detection = None
            last_xyz = None
            last_uncertainty = None

        elif key == ord("s"):
            if last_detection is not None and last_xyz is not None:
                logger.log(
                    last_detection,
                    last_xyz,
                    last_uncertainty
                )
            else:
                print("[WARNING] No XYZ available to save")

        elif key == ord("q"):
            break

    camera.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()