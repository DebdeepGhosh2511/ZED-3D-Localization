import numpy as np


class WeightedMedian:
    def compute(self, points):
        if points is None or len(points) == 0:
            return None

        points = np.asarray(points)

        x = np.median(points[:, 0])
        y = np.median(points[:, 1])
        z = np.median(points[:, 2])

        return x, y, z