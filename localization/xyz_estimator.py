import numpy as np

from pointcloud.dbscan_segmenter import DBSCANSegmenter
from pointcloud.outlier_removal import OutlierRemoval


class XYZEstimator:
    def __init__(self):
        self.segmenter = DBSCANSegmenter(eps=20, min_samples=15)
        self.outlier_removal = OutlierRemoval()

    def estimate_from_center(self, points, center, intrinsics):
        if points is None or len(points) == 0:
            return None

        segmented_points = self.segmenter.segment(points)

        cleaned_points = self.outlier_removal.clean(segmented_points)

        if cleaned_points is None or len(cleaned_points) == 0:
            return None

        Z = np.median(cleaned_points[:, 2])

        u, v = center

        fx = intrinsics["fx"]
        fy = intrinsics["fy"]
        cx = intrinsics["cx"]
        cy = intrinsics["cy"]

        X = (u - cx) * Z / fx
        Y = (v - cy) * Z / fy

        return X, Y, Z