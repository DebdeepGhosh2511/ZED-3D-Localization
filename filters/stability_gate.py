import numpy as np
from collections import deque


class StabilityGate:
    def __init__(self, window_size=30, movement_threshold=12):
        self.window = deque(maxlen=window_size)
        self.movement_threshold = movement_threshold
        self.frozen_xyz = None
        self.is_frozen = False

    def update(self, xyz):
        if xyz is None:
            return None

        if self.is_frozen:
            movement = np.linalg.norm(np.array(xyz) - np.array(self.frozen_xyz))

            if movement <= self.movement_threshold:
                return self.frozen_xyz

            self.is_frozen = False
            self.window.clear()

        self.window.append(xyz)

        if len(self.window) < self.window.maxlen:
            return xyz

        values = np.array(self.window)

        xyz_range = np.max(values, axis=0) - np.min(values, axis=0)

        if np.all(xyz_range <= self.movement_threshold):
            self.frozen_xyz = tuple(np.median(values, axis=0))
            self.is_frozen = True
            print(
                f"[LOCKED STABLE XYZ] "
                f"X={self.frozen_xyz[0]:.1f}, "
                f"Y={self.frozen_xyz[1]:.1f}, "
                f"Z={self.frozen_xyz[2]:.1f} mm"
            )
            return self.frozen_xyz

        return xyz

    def reset(self):
        self.window.clear()
        self.frozen_xyz = None
        self.is_frozen = False