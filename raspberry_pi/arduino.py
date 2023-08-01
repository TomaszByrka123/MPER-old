#BIBLIOTEKA DO OBSŁUGI PRZESYLU DANYCH PRZEZ ARDUINO

import spidev
import time
import random

def start_com():
    SPI_CHANNEL = 0
    SPI_CLOCK_SPEED = 1000000

    spi = spidev.SpiDev()
    spi.open(0, SPI_CHANNEL)
    spi.max_speed_hz = SPI_CLOCK_SPEED

    return spi

def send_data_respond(spi, data):
    try:
        #wyslanie zapytania i odbior odpowiedzi
        buf = spi.xfer2([data])
        dane_od_arduino = buf[0]
    except:
        print("BŁĄD KOMUNIKACJI Z ARDUINO")
    finally:
        return dane_od_arduino
        spi.close()


"""
import spidev

SPI_CHANNEL = 0
SPI_CLOCK_SPEED = 1000000

spi = spidev.SpiDev()
spi.open(0, SPI_CHANNEL)
spi.max_speed_hz = SPI_CLOCK_SPEED

do_wyslania=1234

buf = [do_wyslania, 0]
resp = spi.xfer2(buf)

print("Data returned:", resp[1])
spi.close()
"""