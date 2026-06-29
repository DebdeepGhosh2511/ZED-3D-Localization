import numpy as np
from sklearn.cluster import DBSCAN


class DBSCANSegmenter:
    def __init__(self, eps=20, min_samples=15):
        self.eps = eps
        self.min_samples = min_samples

    def segment(self, points):
        if points is None or len(points) == 0:
            return np.array([])

        points = np.asarray(points)

        if len(points) < self.min_samples:
            return points

        clustering = DBSCAN(
            eps=self.eps,
            min_samples=self.min_samples
        ).fit(points)

        labels = clustering.labels_

        valid_labels = labels[labels != -1]

        if len(valid_labels) == 0:
            return points

        unique_labels, counts = np.unique(valid_labels, return_counts=True)

        main_label = unique_labels[np.argmax(counts)]

        object_points = points[labels == main_label]

        return object_points