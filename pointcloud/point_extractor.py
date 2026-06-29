import numpy as np
import pyzed.sl as sl


class PointCloudExtractor:
    def __init__(self, step=3, central_ratio=0.30):
        self.step = step
        self.central_ratio = central_ratio

    def _valid_point(self, point):
        X, Y, Z = point[0], point[1], point[2]

        if np.isnan(X) or np.isnan(Y) or np.isnan(Z):
            return False

        if np.isinf(X) or np.isinf(Y) or np.isinf(Z):
            return False

        return True

    def extract_points(self, point_cloud, bbox, use_central_region=True):
        x1, y1, x2, y2 = bbox

        width = x2 - x1
        height = y2 - y1

        if width <= 0 or height <= 0:
            return np.array([])

        if use_central_region:
            margin_x = int(width * (1 - self.central_ratio) / 2)
            margin_y = int(height * (1 - self.central_ratio) / 2)

            x1 += margin_x
            y1 += margin_y
            x2 -= margin_x
            y2 -= margin_y

        points = []

        for y in range(y1, y2, self.step):
            for x in range(x1, x2, self.step):
                err, point = point_cloud.get_value(x, y)

                if err != sl.ERROR_CODE.SUCCESS:
                    continue

                if not self._valid_point(point):
                    continue

                points.append([point[0], point[1], point[2]])

        return np.array(points)

    def extract_points_depth_guided(
        self,
        point_cloud,
        bbox,
        click_point,
        depth_band=25
    ):
        click_x, click_y = click_point

        err, clicked_point_3d = point_cloud.get_value(click_x, click_y)

        if err != sl.ERROR_CODE.SUCCESS or not self._valid_point(clicked_point_3d):
            print("[WARNING] Invalid clicked depth, using normal ROI extraction")
            return self.extract_points(point_cloud, bbox, use_central_region=False)

        clicked_z = clicked_point_3d[2]

        x1, y1, x2, y2 = bbox
        points = []

        for y in range(y1, y2, self.step):
            for x in range(x1, x2, self.step):
                err, point = point_cloud.get_value(x, y)

                if err != sl.ERROR_CODE.SUCCESS:
                    continue

                if not self._valid_point(point):
                    continue

                X, Y, Z = point[0], point[1], point[2]

                if abs(Z - clicked_z) <= depth_band:
                    points.append([X, Y, Z])

        return np.array(points)