import time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO


#Stworzenie stron wszystkich zakładek

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

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



# przyklad tego ze mozemy tworzyc bardziej skomplikowane funkcje w pythonie i wtedy js będzie 
# z nich korzystał, wysylal tu dane a python da 
@app.route('/skomplikowana_funkcja/<int:liczba>')
def skomplikowana_funkcja(liczba):
    #skomplikowane obliczenia ...
    wynik = liczba * 2
    return jsonify({'liczba': liczba, 'wynik': wynik})





if __name__ == '__main__':
    socketio.run(app, debug=True)




"""
import paho.mqtt.client as mqtt

#polaczenie z mqtt z biblioteki com
def connect_to_raspberry():
    broker_address = "192.168.8.125"
    try:
        client = com.mqtt.Client()
        client.on_connect = com.on_connect
        client.on_message = com.on_message

        client.connect(broker_address, 1883, 60)
        client.loop_start()
        if client:
            is_raspberry_connect = True
    except:
        is_raspberry_connect = False

connect_to_raspberry()


"""

"""
@socketio.on('message')
def handle_message(message):
    print('oodebrałem: ', message)
    if is_raspberry_connect:
        socketio.emit('message', 1)
    else:
        socketio.emit('message', 0)







def data_from_raspberry():
    count = com.get_last_value()
    while True:
        count = com.get_last_value()
        if count is not None:
            yield f'data: {count[0]}\n\n'
        time.sleep(1)

#publikowanie na /stream danych [0] z tabeli z raspberry pi
@app.route('/stream')
def stream():
    return Response(data_from_raspberry(), mimetype='text/event-stream')

"""
