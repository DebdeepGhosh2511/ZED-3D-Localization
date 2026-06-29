class SimpleKalman:
    def __init__(self, process_noise=0.05, measurement_noise=2.0):
        self.q = process_noise
        self.r = measurement_noise
        self.x = None
        self.p = 1.0

    def update(self, measurement):
        if measurement is None:
            return self.x

        if self.x is None:
            self.x = measurement
            return self.x

        self.p = self.p + self.q
        k = self.p / (self.p + self.r)

        self.x = self.x + k * (measurement - self.x)
        self.p = (1 - k) * self.p

        return self.x

    def reset(self):
        self.x = None
        self.p = 1.0


class KalmanXYZ:
    def __init__(self):
        self.kx = SimpleKalman()
        self.ky = SimpleKalman()
        self.kz = SimpleKalman()

    def update(self, xyz):
        if xyz is None:
            return None

        x, y, z = xyz

        return (
            self.kx.update(x),
            self.ky.update(y),
            self.kz.update(z)
        )

    def reset(self):
        self.kx.reset()
        self.ky.reset()
        self.kz.reset()