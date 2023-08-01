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
