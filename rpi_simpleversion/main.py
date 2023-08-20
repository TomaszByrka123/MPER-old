from flask import Flask, render_template, request, jsonify
import asyncio 

import arduino


stara_tablica = [3, 2, 1]
tablica_do_wyslania = [1, 2, 3]

#połączenie z arduino (SPI)
spi = arduino.start_com()

async def arduino_com():
    while True:
        dane_z_arduino = arduino.send_data_respond(spi, 2)
        print("dane z arduino: ", dane_z_arduino)
        await asyncio.sleep(1)


app = Flask(__name__)


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


#FUNKCJE    

#zapis danych
@app.route('/zapisz_do_tablicy', methods=['POST'])
def zapisz_do_tablicy():
    data = request.json
    if data and 'indeks' in data and 'wartosc' in data:
        indeks = data['indeks']
        wartosc = data['wartosc']
        tablica_do_wyslania[indeks] = wartosc
        return jsonify({'message': 'Wartość zaktualizowana'})
    return jsonify({'error': 'Nieprawidłowe dane'})

#odczyt danych
@app.route('/odczytaj_z_tablicy', methods=['POST'])
def odczytaj_z_tablicy():
    data = request.json
    if data and 'indeks' in data:
        indeks = data['indeks']
        return jsonify({'message': tablica_do_wyslania[indeks]})
    return jsonify({'error': 'Nieprawidłowe dane'})


if __name__ == '__main__':
    asyncio.ensure_future(arduino_com())
    app.run(host='0.0.0.0', port=80)

