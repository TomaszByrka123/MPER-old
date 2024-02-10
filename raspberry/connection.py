from flask import Flask, request
import socket
import netifaces as ni
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    gateway = ni.gateways()['default'][ni.AF_INET][0]
    interface = ni.gateways()['default'][ni.AF_INET][1]
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    netmask = ni.ifaddresses(interface)[ni.AF_INET][0]['netmask']

    # Get wireless connection details
    iw_output = subprocess.check_output(['iw', 'dev', interface, 'link']).decode('utf-8')

    return f'''
    <h1>Informacje o połączeniu</h1>
    <p>Adres IP klienta: {request.remote_addr}</p>
    <p>Adres IP hosta: {host_ip}</p>
    <p>Adres IP interfejsu: {ip}</p>
    <p>Maska podsieci: {netmask}</p>
    <p>Brama domyślna: {gateway}</p>
    <p>Nagłówki żądania: {request.headers}</p>
    <h2>Informacje o połączeniu bezprzewodowym</h2>
    <pre>{iw_output}</pre>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0')
