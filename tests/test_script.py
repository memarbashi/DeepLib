import unittest
from my_library import NeuralNetwork, DenseLayer, relu, relu_derivative, sigmoid, sigmoid_derivative
import numpy as np

class TestLibrary(unittest.TestCase):
    def test_forward(self):
        model = NeuralNetwork()
        model.add_layer(DenseLayer(2, 64, activation=relu, activation_derivative=relu_derivative))
        model.add_layer(DenseLayer(64, 1, activation=sigmoid, activation_derivative=sigmoid_derivative))

        X = np.random.randn(1, 2)
        output = model.forward(X)
        self.assertEqual(output.shape, (1, 1))

if __name__ == '__main__':
    unittest.main()
