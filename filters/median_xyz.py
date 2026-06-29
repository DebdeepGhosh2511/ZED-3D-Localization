import numpy as np
from collections import deque


class MedianXYZ:
    def __init__(self, window_size=10):
        self.window = deque(maxlen=window_size)

    def update(self, xyz):
        if xyz is None:
            return None

        self.window.append(xyz)

        values = np.array(self.window)

        median_x = np.median(values[:, 0])
        median_y = np.median(values[:, 1])
        median_z = np.median(values[:, 2])

        return median_x, median_y, median_z

    def reset(self):
        self.window.clear()