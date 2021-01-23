import serial
import config as cfg
import tkinter as tk
import RPi.GPIO as GPIO
from time import sleep
from gui import *
from printer import *
from functions import *
    
def main():
    # Set the serial communication port from Arduino
    print('Connecting to Arduino...')
    ser = serial.Serial('/dev/ttyACM0', cfg.BAUDRATE, timeout=0.01)
    sleep(2)
    #Define Macros
    print('Defining macros...')
    send(ser,GC_Macro1)
    send(ser,GC_Macro2)
    send(ser,GC_Macro3)
    send(ser,GC_Macro4)
    send(ser,GC_Macro5)
    send(ser,GC_Macro6)
    print('Arduino connected and ready!')

    # Set Pin for add-layer-signal
    pin_laser_connection = 23

    # Setup pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_laser_connection,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    # define the printer and the printer GUI properties
    gui_root = tk.Tk()   
    printer = Printer('Sintratec laser printer',ser)
    printer_gui = GUI(printer,master=gui_root)
    # printer_gui.mainloop()

    while True:
        try:
            if (gui_root.state() == 'normal'):
                # Add Layer if Laser is triggered
                pin_state = GPIO.input(pin_laser_connection)
                # For Pull_Up: Laser is triggerd if button_state == 0
                if (pin_state==0):
                    sleep(0.5)
                    printer_gui.write_gui_output_text('Signal from Laser received')
                    if printer.homed and printer.smoothed:
                        send(printer.ser, GC_Layer)
                
                # Enable Buttons in Gui after Homing and Smoothing
                if (printer.homed or (printer.x_homed and printer.y_homed and printer.z_homed)) and printer.smoothed:
                    printer_gui.btn_enable("btn_addLayer",True)
                elif printer.homed:
                    printer_gui.btn_enable("btn_smooth",True)
        
                printer_gui.readout()       
                printer_gui.update_idletasks()
                printer_gui.update()        
        except Exception:
            print('Closed Gui -> Stoped Programm')
            break           

if __name__ == '__main__':
    main()
