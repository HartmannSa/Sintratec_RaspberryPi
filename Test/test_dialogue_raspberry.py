import config as cfg
import serial
from time import sleep

s = serial.Serial("/dev/ttyACM0", 9600,timeout=100)
# s.open()
sleep(1)
s.flush()

# s.write("ready?\n".encode('utf-8'))

try:
    while True:
        response = s.readline().decode('utf-8').rstrip()
        print(response)
        s.flush()
        sleep(0.5)
except KeyboardInterrupt():
    s.close()