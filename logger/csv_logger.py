import csv
import os
from datetime import datetime


class CSVLogger:
    def __init__(self, filename="outputs/csv/xyz_log.csv"):
        self.filename = filename

        os.makedirs(
            os.path.dirname(filename),
            exist_ok=True
        )

        if not os.path.exists(filename):

            with open(
                filename,
                "w",
                newline=""
            ) as f:

                writer = csv.writer(f)

                writer.writerow([
                    "timestamp",
                    "object_id",
                    "class_name",
                    "confidence",

                    "x_mm",
                    "y_mm",
                    "z_mm",

                    "x_uncertainty_mm",
                    "y_uncertainty_mm",
                    "z_uncertainty_mm"
                ])

    def log(
        self,
        detection,
        xyz,
        uncertainty=None
    ):

        if detection is None or xyz is None:
            return

        x, y, z = xyz

        if uncertainty is None:

            ux = ""
            uy = ""
            uz = ""

        else:

            ux, uy, uz = uncertainty

            ux = round(ux, 2)
            uy = round(uy, 2)
            uz = round(uz, 2)

        with open(
            self.filename,
            "a",
            newline=""
        ) as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                detection["id"],
                detection["class_name"],

                round(
                    detection["confidence"],
                    3
                ),

                round(x, 2),
                round(y, 2),
                round(z, 2),

                ux,
                uy,
                uz
            ])

        print("[OK] XYZ + Uncertainty Saved to CSV")