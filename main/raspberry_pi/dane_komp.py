import asyncio
import websockets

async def receive_data(websocket, path):
    async for message in websocket:
        print(f'Odebrano: {message}')


        #WYKONYWANIE WSZYTSKIEGO

        response = [1, 2, 3, 4, 2, 1, 3, 7]
        
        response_g_format = ','.join(map(str, response))
        await websocket.send(response_g_format)

start_server = websockets.serve(receive_data, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


#KOD WYKORZYSTUJĄCY MQTT DO KOMUNIKACJI, TERAZ UŻYWAMY WEBSOCKET PONIEWAZ JEST SZYBSZY
"""
import time
import random
import json
import paho.mqtt.client as mqtt

import arduino


#połączenie z arduino (SPI)
spi = arduino.start_com()

#połączenie z mqtt (PC)

broker_address = "localhost"  #broker postawiony na raspberry pi
def polaczenie(client, userdata, flags, rc):
    print("polaczono z brokerem " + str(rc))
client = mqtt.Client()
client.polaczenie = polaczenie

client.connect(broker_address, 1883, 60)
client.loop_start()


while True:
    #komunikacja z arduino
    dane_z_arduino = arduino.send_data_respond(spi, 2)
    print("dane z arduino: ", dane_z_arduino)

    #komunikacja z PC
    data = [random.randint(1, 100) for _ in range(25)]  # losowe liczby
    payload = json.dumps(data)  
    client.publish("topic/dane", payload)  #publikowanie danych dla dla MQTT
    print("Wysłano dane:", data)
    time.sleep(1)

client.loop_stop()
client.disconnect()
"""