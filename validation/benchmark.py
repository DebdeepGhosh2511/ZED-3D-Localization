import csv
import os

from validation.metrics import Metrics


class Benchmark:
    def __init__(self):
        self.actual_z = []
        self.predicted_z = []
        self.metrics = Metrics()

    def add_sample(self, actual_z, predicted_z):
        self.actual_z.append(actual_z)
        self.predicted_z.append(predicted_z)

    def report(self):
        if len(self.actual_z) == 0:
            print("No validation samples added")
            return

        mae = self.metrics.mae(self.actual_z, self.predicted_z)
        rmse = self.metrics.rmse(self.actual_z, self.predicted_z)
        accuracy = self.metrics.accuracy_percentage(self.actual_z, self.predicted_z)
        std_dev = self.metrics.std_deviation(self.actual_z, self.predicted_z)
        max_error = self.metrics.max_error(self.actual_z, self.predicted_z)
        min_error = self.metrics.min_error(self.actual_z, self.predicted_z)

        print("\nValidation Report")
        print("-----------------")
        print(f"MAE       : {mae:.2f} mm")
        print(f"RMSE      : {rmse:.2f} mm")
        print(f"Accuracy  : {accuracy:.2f}%")
        print(f"Std Dev   : {std_dev:.2f} mm")
        print(f"Max Error : {max_error:.2f} mm")
        print(f"Min Error : {min_error:.2f} mm")

    def save(self, filename="outputs/reports/validation_report.csv"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        mae = self.metrics.mae(self.actual_z, self.predicted_z)
        rmse = self.metrics.rmse(self.actual_z, self.predicted_z)
        accuracy = self.metrics.accuracy_percentage(self.actual_z, self.predicted_z)
        std_dev = self.metrics.std_deviation(self.actual_z, self.predicted_z)
        max_error = self.metrics.max_error(self.actual_z, self.predicted_z)
        min_error = self.metrics.min_error(self.actual_z, self.predicted_z)

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(["Actual_Z_mm", "Predicted_Z_mm", "Absolute_Error_mm", "Accuracy_%"])

            for actual, predicted in zip(self.actual_z, self.predicted_z):
                error = abs(actual - predicted)
                acc = (1 - error / actual) * 100

                writer.writerow([
                    actual,
                    predicted,
                    round(error, 2),
                    round(acc, 2)
                ])

            writer.writerow([])
            writer.writerow(["Metric", "Value"])
            writer.writerow(["MAE_mm", round(mae, 2)])
            writer.writerow(["RMSE_mm", round(rmse, 2)])
            writer.writerow(["Accuracy_%", round(accuracy, 2)])
            writer.writerow(["Std_Dev_mm", round(std_dev, 2)])
            writer.writerow(["Max_Error_mm", round(max_error, 2)])
            writer.writerow(["Min_Error_mm", round(min_error, 2)])

        print("[OK] Validation report saved")