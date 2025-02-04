import numpy as np

# تعریف لایه Dense
class DenseLayer:
    def __init__(self, input_dim, output_dim, activation=None):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.activation = activation
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
        # مشتق وزرن‌ها و بایاس‌ها
        self.dweights = np.dot(self.inputs.T, dvalues)
        self.dbiases = np.sum(dvalues, axis=0, keepdims=True)
        # مشتق ورودی‌ها برای لایه قبلی
        self.dinputs = np.dot(dvalues, self.weights.T)
        return self.dinputs

# الگوریتم بهینه‌سازی SGD
class SGD:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def update(self, layers):
        for layer in layers:
            layer.weights -= self.learning_rate * layer.dweights
            layer.biases -= self.learning_rate * layer.dbiases

# تعریف شبکه عصبی
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
            # پیش‌رو
            output = self.forward(X)
            # محاسبه خطا
            loss = np.mean((output - y) ** 2)
            # پس‌رو
            dloss = 2 * (output - y) / y.size
            self.backward(dloss)
            # به‌روزرسانی وزن‌ها
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

# مثال استفاده
if __name__ == "__main__":
    # ایجاد داده‌های نمونه
    X = np.random.randn(100, 2)
    y = np.random.randn(100, 1)

    # تعریف مدل
    model = NeuralNetwork()
    model.add_layer(DenseLayer(2, 64, activation=np.tanh))
    model.add_layer(DenseLayer(64, 1, activation=None))

    # آموزش مدل
    model.train(X, y, epochs=1000)

    # ارزیابی مدل
    predictions = model.predict(X)
    loss = np.mean((predictions - y) ** 2)
    print(f"Final Loss: {loss}")

    # ذخیره مدل
    model.save_model('model.pkl')

    # بارگذاری مدل
    model.load_model('model.pkl')
