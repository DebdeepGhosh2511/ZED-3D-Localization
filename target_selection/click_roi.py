class ClickROI:
    def __init__(self, roi_size=60):
        self.roi_size = roi_size

    def create_roi(self, click_x, click_y, frame_width, frame_height):
        half = self.roi_size // 2

        x1 = max(0, click_x - half)
        y1 = max(0, click_y - half)
        x2 = min(frame_width - 1, click_x + half)
        y2 = min(frame_height - 1, click_y + half)

        return x1, y1, x2, y2