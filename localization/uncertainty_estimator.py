import numpy as np
from collections import deque


class UncertaintyEstimator:
    def __init__(self, window_size=10):
        self.window = deque(maxlen=window_size)

    def update(self, xyz):
        if xyz is None:
            return None

        self.window.append(xyz)

        if len(self.window) < 5:
            return None

        values = np.array(self.window)

        # Use Median Absolute Deviation; more stable than std for depth noise
        med = np.median(values, axis=0)
        mad = np.median(np.abs(values - med), axis=0)

        # Convert MAD to approx standard deviation
        uncertainty = 1.4826 * mad

        return float(uncertainty[0]), float(uncertainty[1]), float(uncertainty[2])

    def reset(self):
        self.window.clear()