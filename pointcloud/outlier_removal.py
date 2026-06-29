import numpy as np


class OutlierRemoval:
    def __init__(self, min_depth=100, max_depth=3000, z_threshold=15):
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.z_threshold = z_threshold

    def clean(self, points):
        if points is None or len(points) == 0:
            return np.array([])

        points = np.asarray(points)

        points = points[
            (points[:, 2] > self.min_depth) &
            (points[:, 2] < self.max_depth)
        ]

        if len(points) == 0:
            return np.array([])

        z_median = np.median(points[:, 2])

        points = points[
            np.abs(points[:, 2] - z_median) < self.z_threshold
        ]

        if len(points) == 0:
            return np.array([])

        median = np.median(points, axis=0)
        distances = np.linalg.norm(points - median, axis=1)

        distance_median = np.median(distances)

        if distance_median == 0:
            return points

        threshold = distance_median * 2.0

        return points[distances < threshold]