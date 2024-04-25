#!/venv/bin/python3
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import threading
import time
import subprocess

from arduino import Arduino
from lcd import LCD


"""
#plik z kamerą (uruchamianie kamery automatycznie, trzeba usunac jeszze run_camera_mper.service)
try:
    subprocess.run(['sudo', 'python3', 'camera_pi.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except:
    print("Błąd uruchomienia kamery")
"""

baterry = 98
actualSettings = [1, 1, 1]
pcAppStatus = False
mobileAppStatus = False
lcd = LCD(rgb_addr=0x60,col= 16,row = 2)
lcd.home()
errorTable = []

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
    
def printPage(message, code=None):
    if message not in errorTable: errorTable.append(message)
    if code is not None: lcd.print_out(str(code))
    print(message)
    try: socketio.emit('message', message)
    except: pass


podwozieData = [100, 100, 0, 0, 0]
podwozieWorking = False
def podwozieThreadFunction():
    global podwozieWorking
    def on_detction(data):
        pass
    try:
        podwozie = Arduino('/dev/ttyACM0')
        podwozie.set_callback(on_detction)
        podwozie.start_get_data()
        podwozieWorking = True
        printPage("POLACZENIE Z ARDUINO - PODWOZIE UDANE")
    except:
        printPage("BRAK POŁĄCZENIA Z ARDUINO - PODWOZIE", "A")

    if podwozieWorking:
        while True:
            try: podwozie.send_data(podwozieData)
            except: pass
            time.sleep(.1)

manipulatorData = [0, 0, 0, 0, 0]
manipulatorWorking = False
def manipulatorThreadFunction():
    global manipulatorWorking
    def on_detction(data):
        pass
    try:
        manipulator = Arduino('/dev/ttyUSB0')
        manipulator.set_callback(on_detction)
        manipulator.start_get_data()
        manipulatorWorking = True
        printPage("POLACZENIE Z ARDUINO - MANIPULATOR UDANE")
    except: printPage("BRAK POŁĄCZENIA Z ARDUINO - MANIPULATOR", "B")

    if manipulatorWorking:
        while True:
            try:
                manipulator.send_data(manipulatorData)
            except: pass
            time.sleep(.5)

@socketio.on('connect')
def connect():
    global pcAppStatus, mobileAppStatus
    
    for error in errorTable: printPage(error)

    if request.headers.get('User-Agent').find('Mobile') != -1: mobileAppStatus = True
    else: pcAppStatus = True
    emit('status_update', {'komputer': pcAppStatus, 'mobile': mobileAppStatus}, broadcast=True)

  
@socketio.on('disconnect')
def disconnect():
    global mobileAppStatus, pcAppStatus
    if request.headers.get('User-Agent').find('Mobile') != -1: mobileAppStatus = False
    else: pcAppStatus = False
    emit('status_update', {'komputer': pcAppStatus, 'mobile': mobileAppStatus}, broadcast=True)

@socketio.on('settings')
def settings(new_settings=None):
    global actualSettings
    if new_settings is not None:
        actualSettings = new_settings
    socketio.emit('settings', actualSettings)


@socketio.on('joystickPodwozie')
def joystickPodwozie(data):
    podwozieData[2] = actualSettings[0]
    podwozieData[3] = actualSettings[1]
    podwozieData[4] = actualSettings[2]
    podwozieData[0] = data['left'] 
    podwozieData[1] = data['right']



@socketio.on('joystickManipulator')
def joystickManipulator(data):
    manipulatorData[0] = data[0]
    manipulatorData[1] = data[1]
    manipulatorData[2] = data[2]
    manipulatorData[3] = data[3]
    manipulatorData[4] = data[4]

if __name__ == '__main__':
    
    podwozieThread = threading.Thread(target=podwozieThreadFunction)
    podwozieThread.start()

    manipulatorThread = threading.Thread(target=manipulatorThreadFunction)
    manipulatorThread.start()

    socketio.run(app, port=8080, debug=True, allow_unsafe_werkzeug=True, host='0.0.0.0')
    
