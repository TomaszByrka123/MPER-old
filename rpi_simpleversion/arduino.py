#OBSŁUGA KOMUNIKACJI Z ARDUINO PRZEZ UART

#!/usr/bin/env python3
import serial
import threading
import time


class Arduino:
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.arduino = serial.Serial(self.serial_port, 9600, timeout=1)
        self.arduino.reset_input_buffer()
        self.is_running = False
        self.thread = None
        self.callback = None


    def get_data(self):
        while self.is_running:
            if self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode('utf-8').rstrip()
                if self.callback:
                    self.callback(line)


    def start_get_data(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self.get_data)
            self.thread.start()


    def stop_get_data(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()


    def set_callback(self, callback):
        self.callback = callback


    def send_data(self, data):
        try:
            for number in data:
                self.arduino.write(str(number).encode('utf-8'))
                print(f"Wysłano do Arduino: {data}")
                time.sleep(0.1)
        except Exception as e:
            print(f"Błąd wysyłania danych: {str(e)}")


    def __del__(self):
        if 'arduino' in locals() and self.arduino.is_open:
            self.arduino.close()



#uzycie:

def on_detction(data):
    print("detect: ", data)

try:
    podwozie = Arduino('/dev/ttyACM0')
    podwozie.set_callback(on_detction)
    podwozie.start_get_data()
    while True:
        input_str = input("Podaj x i y: ")
        numbers = input_str.split()
        x = int(numbers[0])
        y = int(numbers[1])
        print("x: ", x, "y: ", y)
        podwozie.send_data([100, 100])
        time.sleep(3)
except:
    print("nie udalo się połączyć z arduino")





"""
import serial

def send_data(serial_port, data):
    try:
        ser = serial.Serial(serial_port, 9600, timeout=1)
        ser.write(data.encode('utf-8'))
        print(f"Wysłano do Arduino: {data}")
    except Exception as e:
        print(f"Błąd wysyłania danych: {str(e)}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()



if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            send_data('/dev/ttyACM0', 5)
            print(line)

"""