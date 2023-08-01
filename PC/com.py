#biblioteka do obslugi komunikacji raspoberry pi ze strona przez MQTT
import json
import paho.mqtt.client as mqtt

broker_address = "192.168.8.125" #adres maliny bo na niej jest broker

last_value = None  #ostatnia odczytana wartosc

def on_connect(client, userdata, flags, rc):
    print("polaczono z MQTT - " + str(rc))
    client.subscribe("topic/dane")  # Temat: dane

def on_message(client, userdata, msg):
    global last_value
    payload = json.loads(msg.payload.decode()) #odczyt danych
    last_value = payload
    #print("Odebrano dane:", payload)

def get_last_value():
    return last_value  #wyjsciowa funkcja

def send_data(client, data):
    payload = json.dumps(data)
    client.publish("topic/pc", payload)
    print("wyslano dane: ", data)




#PRZYKLAD UZYCIA
"""
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, 1883, 60)
client.loop_start()

"""


