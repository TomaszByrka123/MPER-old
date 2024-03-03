#!/venv/bin/python
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import time

from arduino import Arduino

baterry = 98
actualSettings = [1, 1, 1]
pcAppStatus = False
mobileAppStatus = False

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

@app.route('/mobile')
def mobileApp():
    return render_template('mobile.html')

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
podwozieData = [0, 0, 0, 0, 0]
def podwozieThreadFunction():
    def on_detction(data):
        printPage("detect: ", data)

    try:
        podwozie = Arduino('/dev/ttyACM0')
        podwozie.set_callback(on_detction)
        podwozie.start_get_data()
        printPage("POLACZENIE Z ARDUINO - PODWOZIE UDANE")
    except:
        printPage("BRAK POŁĄCZENIA Z ARDUINO - PODWOZIE")

    while True:
        try:
            podwozie.send_data(podwozieData)
        except: pass
        time.sleep(.05)


manipulatorThread = None
manipulatorData = [0, 0, 0, 0, 0]
def manipulatorThreadFunction():
    def on_detction(data):
        printPage(f"detect: {data}")

    try:
        manipulator = Arduino('/dev/ttyUSB0')
        manipulator.set_callback(on_detction)
        manipulator.start_get_data()
        printPage("POLACZENIE Z ARDUINO - MANIPULATOR UDANE")
    except:
        printPage("BRAK POŁĄCZENIA Z ARDUINO - MANIPULATOR")

    while True:
        try:
            manipulator.send_data(manipulatorData)
        except: pass
        time.sleep(.5)
      

@socketio.on('connect')
def connect():
    global pcAppStatus, mobileAppStatus
    global podwozieThread
    if podwozieThread is None:
        podwozieThread = socketio.start_background_task(target=podwozieThreadFunction)

    global manipulatorThread
    if manipulatorThread is None:
        manipulatorThread = socketio.start_background_task(target=manipulatorThreadFunction)

    if request.headers.get('User-Agent').find('Mobile') != -1:
        mobileAppStatus = True
        print('Client mobile connected')
    else:
        pcAppStatus = True
        print('Client pc connected')
    emit('status_update', {'komputer': pcAppStatus, 'mobile': mobileAppStatus}, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    global mobileAppStatus, pcAppStatus
    if request.headers.get('User-Agent').find('Mobile') != -1:
        mobileAppStatus = False
        print('Client mobile disconnected')
    else:
        pcAppStatus = False
        print('Client pc disconnected')
    emit('status_update', {'komputer': pcAppStatus, 'mobile': mobileAppStatus}, broadcast=True)
      
@socketio.on('settings')
def settings(new_settings=None):
    global actualSettings
    if new_settings is not None:
        actualSettings = new_settings
    socketio.emit('settings', actualSettings)


@socketio.on('joystickPodwozie')
def joystickPodwozie(data):
    print(data)
    podwozieData[0] = data['left'] 
    podwozieData[1] = data['right']
    podwozieData[2] = actualSettings[0]
    podwozieData[3] = actualSettings[1]
    podwozieData[4] = actualSettings[2]

@socketio.on('joystickManipulator')
def joystickManipulator(data):
    manipulatorData[0] = data[0]
    manipulatorData[1] = data[1]
    manipulatorData[2] = data[2]
    manipulatorData[3] = data[3]
    manipulatorData[4] = data[4]

if __name__ == '__main__':
    socketio.run(app, port=8080, debug=True, host='0.0.0.0')

