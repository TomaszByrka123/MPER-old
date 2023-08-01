from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

default_position = [51.5074, -0.1278]

x = default_position[0]
y = default_position[1]

@app.route('/')
def index():
    return render_template('mapa.html')

@app.route('/get_position')
def get_position():
    global x, y
    # Symulacja zmiany pozycji (będzie odbieranie danych z raspberry od GPS)
    x += 0.001
    y -= 0.001
    return jsonify({'lat': x, 'lng': y})

if __name__ == '__main__':
    app.run(debug=True)
