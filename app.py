from flask import Flask, request, jsonify, render_template
import numpy as np
from model import NeuralNetwork, DenseLayer
from activations import relu, relu_derivative, sigmoid, sigmoid_derivative

app = Flask(__name__)

# ایجاد مدل و بارگذاری آن
model = NeuralNetwork()
model.add_layer(DenseLayer(2, 64, activation=relu, activation_derivative=relu_derivative))
model.add_layer(DenseLayer(64, 1, activation=sigmoid, activation_derivative=sigmoid_derivative))
model.load_model('model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    X = np.array(data['input'])
    prediction = model.predict(X)
    return jsonify({'output': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
