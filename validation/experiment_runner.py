import csv
import os
from datetime import datetime

from validation.benchmark import Benchmark


class ExperimentRunner:

    def __init__(self):

        self.benchmark = Benchmark()

    def add_measurement(
        self,
        actual_distance,
        predicted_distance
    ):

        self.benchmark.add_sample(
            actual_distance,
            predicted_distance
        )

    def generate_report(self):

        self.benchmark.report()

    def save_report(
        self,
        filename="outputs/reports/experiment_results.csv"
    ):

        os.makedirs(
            os.path.dirname(filename),
            exist_ok=True
        )

        mae = self.benchmark.metrics.mae(
            self.benchmark.actual_z,
            self.benchmark.predicted_z
        )

        rmse = self.benchmark.metrics.rmse(
            self.benchmark.actual_z,
            self.benchmark.predicted_z
        )

        accuracy = (
            self.benchmark.metrics
            .accuracy_percentage(
                self.benchmark.actual_z,
                self.benchmark.predicted_z
            )
        )

        with open(
            filename,
            "w",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Actual_Z",
                    "Predicted_Z"
                ]
            )

            for actual, predicted in zip(
                self.benchmark.actual_z,
                self.benchmark.predicted_z
            ):

                writer.writerow(
                    [
                        actual,
                        predicted
                    ]
                )

            writer.writerow([])
            writer.writerow(
                [
                    "Timestamp",
                    datetime.now()
                ]
            )

            writer.writerow(
                [
                    "MAE",
                    round(mae, 3)
                ]
            )

            writer.writerow(
                [
                    "RMSE",
                    round(rmse, 3)
                ]
            )

            writer.writerow(
                [
                    "Accuracy",
                    round(accuracy, 3)
                ]
            )

        print(
            "[OK] Experiment report saved"
        )