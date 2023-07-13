import spidev
import time

SPI_CHANNEL = 0
SPI_CLOCK_SPEED = 1000000

spi = spidev.SpiDev()
spi.open(0, SPI_CHANNEL)
spi.max_speed_hz = SPI_CLOCK_SPEED

try:
    while True:
        buf = spi.xfer2([0])
        dane_od_arduino = buf[0]
        print("otrzymane dane:", dane_od_arduino)
        time.sleep(1)
finally:
    spi.close()


"""import spidev

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