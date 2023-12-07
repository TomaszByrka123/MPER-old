from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import time

#import arduino


app = Flask(__name__)
socketio = SocketIO(app)

#ZAKŁADKI
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/czujnik')
def czujnik():
    return render_template('czujnik.html')

@app.route('/kamery')
def kamery():
    return render_template('kamery.html')

@app.route('/lokalizacja')
def lokalizacja():
    return render_template('lokalizacja.html')

@app.route('/sterowanie')
def sterowanie():
    return render_template('sterowanie.html')

@app.route('/ustawienia')
def ustawienia():
    return render_template('ustawienia.html')

@app.route('/science')
def science():
    return render_template('science.html')


@socketio.on('joystick')
def handle_message(message):
    go(message)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

