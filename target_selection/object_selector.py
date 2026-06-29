class ObjectSelector:
    def __init__(self, max_missing_frames=10):
        self.selected_bbox = None
        self.selected_detection = None
        self.selected_class_name = None
        self.mode = None
        self.missing_count = 0
        self.max_missing_frames = max_missing_frames

    def select_by_click(self, detections, click_x, click_y):
        candidates = []

        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]

            if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                area = (x2 - x1) * (y2 - y1)
                candidates.append((area, detection))

        if not candidates:
            return None

        candidates.sort(key=lambda x: x[0])
        selected = candidates[0][1]

        self.selected_bbox = selected["bbox"]
        self.selected_detection = selected
        self.selected_class_name = selected["class_name"]
        self.mode = "YOLO"
        self.missing_count = 0

        print(f"[OK] YOLO object selected: ID {selected['id']} {selected['class_name']}")
        return selected

    def select_manual_roi(self, bbox, click_x, click_y):
        self.selected_bbox = bbox
        self.selected_detection = {
            "id": 0,
            "class_name": "manual_roi",
            "confidence": 1.0,
            "bbox": bbox,
            "center": ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2),
            "click_point": (click_x, click_y)
        }

        self.selected_class_name = "manual_roi"
        self.mode = "MANUAL"
        self.missing_count = 0

        print("[OK] Manual depth-guided ROI selected")
        return self.selected_detection

    def get_selected(self, detections):
        if self.selected_bbox is None:
            return None

        if self.mode == "MANUAL":
            return self.selected_detection

        old_x1, old_y1, old_x2, old_y2 = self.selected_bbox
        old_cx = (old_x1 + old_x2) // 2
        old_cy = (old_y1 + old_y2) // 2
        old_area = (old_x2 - old_x1) * (old_y2 - old_y1)

        best_detection = None
        best_score = float("inf")

        for detection in detections:
            class_penalty = 0 if detection["class_name"] == self.selected_class_name else 500

            cx, cy = detection["center"]
            x1, y1, x2, y2 = detection["bbox"]
            area = (x2 - x1) * (y2 - y1)

            center_distance = ((cx - old_cx) ** 2 + (cy - old_cy) ** 2) ** 0.5
            area_change = abs(area - old_area) / old_area if old_area > 0 else 0

            if area_change > 2.0:
                continue

            score = center_distance + (area_change * 100) + class_penalty

            if score < best_score:
                best_score = score
                best_detection = detection

        if best_detection is not None:
            self.selected_bbox = best_detection["bbox"]
            self.selected_detection = best_detection
            self.selected_class_name = best_detection["class_name"]
            self.missing_count = 0
            return self.selected_detection

        self.missing_count += 1

        if self.missing_count <= self.max_missing_frames:
            return self.selected_detection

        print("[WARNING] Selected object lost")
        return None

    def clear_selection(self):
        self.selected_bbox = None
        self.selected_detection = None
        self.selected_class_name = None
        self.mode = None
        self.missing_count = 0
        print("[OK] Selection cleared")