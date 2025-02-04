# My Library

A simple deep learning library.

## Installation

You can install this library using pip:

```bash
pip install my_library

from my_library import NeuralNetwork, DenseLayer, relu, relu_derivative, sigmoid, sigmoid_derivative
import numpy as np

# Create a model
model = NeuralNetwork()
model.add_layer(DenseLayer(2, 64, activation=relu, activation_derivative=relu_derivative))
model.add_layer(DenseLayer(64, 1, activation=sigmoid, activation_derivative=sigmoid_derivative))

# Create some sample data
X = np.random.randn(100, 2)
y = np.random.randn(100, 1)

# Train the model
model.train(X, y, epochs=1000)

# Make predictions
predictions = model.predict(X)
print(predictions)
