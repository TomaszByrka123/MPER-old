import time
from flask import Flask, render_template, Response
import paho.mqtt.client as mqtt
import com

broker_address = "192.168.8.125"

client = com.mqtt.Client()
client.on_connect = com.on_connect
client.on_message = com.on_message

client.connect(broker_address, 1883, 60)
client.loop_start()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_numbers():
    count = com.get_last_value()
    while True:
        count = com.get_last_value()
        if count is not None:
            yield f'data: {count[0]}\n\n'
        time.sleep(1)

@app.route('/stream')
def stream():
    return Response(generate_numbers(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
