import serial
import config as cfg
import tkinter as tk
import RPi.GPIO as GPIO
from time import sleep
from gui import *
from printer import *
from functions import *
import gcode
    
def main():
    # Set the serial communication port from Arduino
    print('Connecting to Arduino...')
    ser = serial.Serial('/dev/ttyACM0', cfg.BAUDRATE, timeout=0.01)
    sleep(2)


    print('Arduino connected and ready!')

    # Setup Pin for add-layer-signal
    pin_laser_connection = 23 # ein Kabel in Pin-No. 16, das andere in Pin-No. 14
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(pin_laser_connection,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    # define the printer and the printer GUI properties
    gui_root = tk.Tk()   
    printer = Printer('Sintratec laser printer',ser)
    printer_gui = GUI(printer,master=gui_root)
    # Use default Values from config (not from Arduino)
    send(ser,'G100X'+str(printer.bed_speed)+'Y'+str(printer.bed_speed)+'Z'+str(printer.sledge_speed)+ '\n')
    
    msg_homed_shown = False
    while True:
        try:
            if (gui_root.state() == 'normal'):
                if(printer.x_homed and printer.y_homed and printer.z_homed):
                    printer.homed = True
                # Enable Buttons in GUI after Homing and Smoothing
                if (printer.homed):
                    if not msg_homed_shown:
                        printer_gui.showInfoAfterHomed()
                        msg_homed_shown = True
                    printer_gui.btn_enable("btn_smooth",True)                    
                if (printer.homed and printer.smoothed):
                    printer_gui.btn_enable("btn_addLayer",True)
                    printer_gui.btn_enable("btn_start",True)

                # Add Layer if Laser is triggered
                pin_state = GPIO.input(pin_laser_connection)
                # For Pull_Up: Laser is triggerd if button_state == 0
                if (pin_state==0):
                    sleep(0.5)
                    printer_gui.write_gui_output_text('Signal from Laser received',False)
                    if printer.ready:
                        if printer.homed and printer.smoothed:
                            printer_gui.write_gui_output_text('Adding layer...',False)
                            send(printer.ser, gcode.GC_Layer(printer))
                            # HIER WARTEN BIS LAYERAUFTRAGUNG FERTIG, DANN SIGNAL AN LASER SENDEN
                        else:
                            printer_gui.write_gui_output_text('Layer was not added: Printer is not homed or powder is not smoothed!',False)
                    else:
                        printer_gui.write_gui_output_text('Signal from Laser was ignored, because printing process was not started yet',False)

                printer_gui.readout()       
                printer_gui.update_idletasks()
                printer_gui.update()        
        except Exception:
            print('Closed GUI -> Program stoped')
            break           

if __name__ == '__main__':
    main()
