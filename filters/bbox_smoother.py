from collections import deque
import numpy as np


class BBoxSmoother:
    def __init__(self, window_size=8):
        self.window = deque(maxlen=window_size)

    def update(self, bbox):
        if bbox is None:
            return None

        self.window.append(bbox)

        values = np.array(self.window)

        x1 = int(np.median(values[:, 0]))
        y1 = int(np.median(values[:, 1]))
        x2 = int(np.median(values[:, 2]))
        y2 = int(np.median(values[:, 3]))

        return x1, y1, x2, y2

    def reset(self):
        self.window.clear()