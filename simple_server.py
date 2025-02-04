from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import numpy as np
from model import NeuralNetwork, DenseLayer
from activations import relu, relu_derivative, sigmoid, sigmoid_derivative

# ایجاد مدل و بارگذاری آن
model = NeuralNetwork()
model.add_layer(DenseLayer(2, 64, activation=relu, activation_derivative=relu_derivative))
model.add_layer(DenseLayer(64, 1, activation=sigmoid, activation_derivative=sigmoid_derivative))
model.load_model('model.pkl')

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('templates/index.html', 'r', encoding='utf-8') as file:
                self.wfile.write(file.read().encode('utf-8'))
        elif self.path.startswith('/static/'):
            file_path = self.path[1:]
            if os.path.exists(file_path):
                self.send_response(200)
                if file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif file_path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File not found")
        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            X = np.array(data['input'])
            prediction = model.predict(X)
            response = {'output': prediction.tolist()}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "File not found")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting simple server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
