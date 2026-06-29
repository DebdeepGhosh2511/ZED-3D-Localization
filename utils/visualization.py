import cv2


class Visualizer:
    def draw_all_detections(self, frame, detections):
        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]

            label = (
                f"ID:{detection['id']} "
                f"{detection['class_name']} "
                
            )

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

        return frame

    def draw_selected(self, frame, detection, xyz, uncertainty=None, mode="YOLO"):
        if detection is None:
            return frame

        x1, y1, x2, y2 = detection["bbox"]

        if mode == "MANUAL":
            label = "LOCKED: Manual ROI"
            color = (0, 0, 255)
        else:
            label = f"LOCKED ID:{detection['id']} {detection['class_name']}"
            color = (0, 255, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

        cv2.putText(
            frame,
            label,
            (x1, max(y1 - 35, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        if xyz is not None:
            X, Y, Z = xyz

            cv2.putText(
                frame,
                f"X:{X:.1f} Y:{Y:.1f} Z:{Z:.1f} mm",
                (x1, y2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            if uncertainty is not None:
                ux, uy, uz = uncertainty

                cv2.putText(
                    frame,
                    f"+/- X:{ux:.1f} Y:{uy:.1f} Z:{uz:.1f} mm",
                    (x1, y2 + 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 200, 255),
                    2
                )

        return frame

    def draw_instructions(self, frame):
        text = "Click object/point | R: reset | S: save | Q: quit"

        cv2.putText(
            frame,
            text,
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        return frame