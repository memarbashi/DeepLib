import numpy as np
from activations import relu, relu_derivative, sigmoid, sigmoid_derivative, softmax, softmax_derivative

class DenseLayer:
    def __init__(self, input_dim, output_dim, activation=None, activation_derivative=None):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.activation = activation
        self.activation_derivative = activation_derivative
        self.weights = np.random.randn(input_dim, output_dim) * 0.01
        self.biases = np.zeros((1, output_dim))

    def forward(self, inputs):
        self.inputs = inputs
        linear_output = np.dot(inputs, self.weights) + self.biases
        if self.activation:
            self.output = self.activation(linear_output)
        else:
            self.output = linear_output
        return self.output

    def backward(self, dvalues):
        if self.activation_derivative:
            dvalues = dvalues * self.activation_derivative(self.output)
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
        self.dinputs = np.dot(dvalues, self.weights.T)
        return self.dinputs

class SGD:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def update(self, layers):
        for layer in layers:
            layer.weights -= self.learning_rate * layer.dweights
            layer.biases -= self.learning_rate * layer.dbiases

class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.optimizer = SGD(learning_rate=0.01)

    def add_layer(self, layer):
        self.layers.append(layer)

    def forward(self, X):
        for layer in self.layers:
            X = layer.forward(X)
        return X

    def backward(self, dvalues):
        for layer in reversed(self.layers):
            dvalues = layer.backward(dvalues)

    def train(self, X, y, epochs=1000):
        for epoch in range(1, epochs + 1):
            output = self.forward(X)
            loss = np.mean((output - y) ** 2)
            dloss = 2 * (output - y) / y.size
            self.backward(dloss)
            self.optimizer.update(self.layers)
            if epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss}")

    def predict(self, X):
        return self.forward(X)

    def save_model(self, filename):
        import pickle
        model_data = {
            'weights': [layer.weights for layer in self.layers],
            'biases': [layer.biases for layer in self.layers],
            'activations': [layer.activation for layer in self.layers]
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)

    def load_model(self, filename):
        import pickle
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        for layer, weights, biases, activation in zip(self.layers, model_data['weights'], model_data['biases'], model_data['activations']):
            layer.weights = weights
            layer.biases = biases
            layer.activation = activation
