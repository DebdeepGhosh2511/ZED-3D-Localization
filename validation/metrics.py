import numpy as np


class Metrics:

    def mae(self, actual, predicted):

        actual = np.array(actual)
        predicted = np.array(predicted)

        return np.mean(
            np.abs(actual - predicted)
        )

    def rmse(self, actual, predicted):

        actual = np.array(actual)
        predicted = np.array(predicted)

        return np.sqrt(
            np.mean(
                (actual - predicted) ** 2
            )
        )

    def accuracy_percentage(
        self,
        actual,
        predicted
    ):

        actual = np.array(actual)
        predicted = np.array(predicted)

        error = np.abs(
            actual - predicted
        )

        accuracy = (
            1 - error / actual
        ) * 100

        return np.mean(
            accuracy
        )

    def std_deviation(
        self,
        actual,
        predicted
    ):

        actual = np.array(actual)
        predicted = np.array(predicted)

        error = np.abs(
            actual - predicted
        )

        return np.std(error)

    def max_error(
        self,
        actual,
        predicted
    ):

        actual = np.array(actual)
        predicted = np.array(predicted)

        error = np.abs(
            actual - predicted
        )

        return np.max(error)

    def min_error(
        self,
        actual,
        predicted
    ):

        actual = np.array(actual)
        predicted = np.array(predicted)

        error = np.abs(
            actual - predicted
        )

        return np.min(error)