#!/venv/bin/python
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import time

from arduino import Arduino

baterry = 98
actualSettings = [1, 1, 1]

app = Flask(__name__)
socketio = SocketIO(app)

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

"""
#cashowanie obrazów (na testy jest wyłączone)
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'public, max-age=86400'  # 1 dzień w sekundach
    return response
"""
    
def printPage(message):
    print(message)
    socketio.emit('message', message)




podwozieThread = None
podwozieData = [0, 0]
def podwozieThreadFunction():
    def on_detction(data):
        printPage("detect: ", data)

    try:
        podwozie = Arduino('/dev/ttyACM0')
        podwozie.set_callback(on_detction)
        podwozie.start_get_data()
        print("polaczenie z arduino - podwozie udane")
    except:
        printPage("BRAK POŁĄCZENIA Z ARDUINO - PODWOZIE")

    while True:
        try:
            podwozieData.extend(actualSettings)
            podwozie.send_data(podwozieData)
        except:
            pass
        time.sleep(.05)



manipulatorThread = None
manipulatorData = [0, 0, 0, 0, 0]
def manipulatorThreadFunction():
    def on_detction(data):
        printPage("detect: ", data)

    try:
        manipulator = Arduino('/dev/ttyACM0')
        manipulator.set_callback(on_detction)
        manipulator.start_get_data()
        print("polaczenie z arduino - manipulator udane")
    except:
        printPage("BRAK POŁĄCZENIA Z ARDUINO - MANIPULATOR")

    while True:
        try:
            manipulator.send_data(manipulatorData)
        except:
            pass
        time.sleep(.05)
      


@socketio.on('connect')
def connect():
    printPage("połączenie z raspberry pi udane")
    global podwozieThread
    if podwozieThread is None:
        podwozieThread = socketio.start_background_task(target=podwozieThreadFunction)

    global manipulatorThread
    if manipulatorThread is None:
        manipulatorThread = socketio.start_background_task(target=manipulatorThreadFunction)

@socketio.on('settings')
def settings(new_settings=None):
    global actualSettings
    if new_settings is not None:
        actualSettings = new_settings
    socketio.emit('settings', actualSettings)


@socketio.on('joystickPodwozie')
def joystickPodwozie(data):
    podwozieData[0] = data['left'] 
    podwozieData[1] = data['right']


@socketio.on('joystickManipulator')
def joystickManipulator(data):
    manipulatorData = data

if __name__ == '__main__':
    socketio.run(app, port=8080, debug=True, host='0.0.0.0')

