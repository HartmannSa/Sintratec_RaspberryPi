import serial
import config as cfg
import functions as fnc
import tkinter as tk
import RPi.GPIO as GPIO
from time import sleep

# Set the serial communication port from Arduino
ser = serial.Serial('/dev/ttyACM0', cfg.BAUDRATE)

# Set Pin for add-layer-signal
pin_laser_connection = 23

# Setup pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_laser_connection,GPIO.IN,pull_up_down=GPIO.PUD_UP)

# # read and print bootup message from arduino
# fnc.readout(ser)

# define the printer and the printer GUI properties
gui_root = tk.Tk()
printer = fnc.printer('Sintratec laser printer',ser)
printer_gui = fnc.Application(printer,master=gui_root)

while True:
    # Add Layer if Laser is triggered
    pin_state = GPIO.input(pin_laser_connection)
    # For Pull_Up: Laser is triggerd if button_state == 0
    if (pin_state==0):
        sleep(0.5)
        fnc.write_gui_output_text(printer_gui.output_text,'Signal from Laser received')
        if printer.homed and printer.smoothed:
            fnc.apply_powder(ser)
        
    # Enable Buttons in Gui after Homing and Smoothing
    if printer.homed and printer.smoothed:
        printer_gui.btn_enable("btn_addLayer",True)
    elif printer.homed:
        printer_gui.btn_enable("btn_smooth",True)
    
    printer_gui.update_idletasks()
    printer_gui.update()

