from time import *

def send(ser,gcode):
    ser.write(gcode.encode('utf-8'))
    sleep(0.01)