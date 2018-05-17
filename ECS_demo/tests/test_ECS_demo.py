from __future__ import absolute_import, division, print_function
import ECS_demo as core
import unittest
from sklearn.model_selection import train_test_split


class testKerasModels(unittest.TestCase):

    def test_baseline_model(self):
        X, Y = core.data_setup()
        model = core.baseline_model()
        X_train, X_test, y_train, y_test = train_test_split(X, Y)

        # Fit the model
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=2,
                  batch_size=128, verbose=0)

        # Final evaluation of the model
        scores = model.evaluate(X_test, y_test, verbose=0)
        print("Accuracy: %.2f%%" % (scores[1] * 100))

    def test_benchmark(self):
        core.Benchmark.run(self.test_baseline_model)


if __name__ == '__main__':
    unittest.main()
