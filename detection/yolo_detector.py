from ultralytics import YOLO


class YOLODetector:
    def __init__(self, model_path="models/yolov8m.pt", conf_threshold=0.10):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        print("[OK] YOLOv8m Loaded for small object detection")

    def detect(self, frame):
        results = self.model(
            frame,
            imgsz=1280,
            conf=self.conf_threshold,
            iou=0.35,
            max_det=100,
            agnostic_nms=False,
            verbose=False
        )[0]

        detections = []
        object_id = 1

        for box in results.boxes:
            confidence = float(box.conf[0])

            if confidence < self.conf_threshold:
                continue

            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

            width = x2 - x1
            height = y2 - y1
            area = width * height

            # Ignore extremely tiny false detections only
            if area < 100:
                continue

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            detections.append({
                "id": object_id,
                "class_id": class_id,
                "class_name": class_name,
                "bbox": (x1, y1, x2, y2),
                "center": (center_x, center_y),
                "area": area,
                "confidence": confidence
            })

            object_id += 1

        return detections