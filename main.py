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

    # Setup Pins for receiving and sending signal to RTC Board:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    GPIO.setwarnings(False)
    GPIO.setup(cfg.pin_laser_input,GPIO.IN,pull_up_down=GPIO.PUD_UP) # for receiving
    GPIO.setup(cfg.pin_laser_output,GPIO.OUT) # for sending
    GPIO.setup(cfg.pin_error_output,GPIO.OUT) # for sending error
    GPIO.output(cfg.pin_laser_output,GPIO.LOW)
    GPIO.output(cfg.pin_error_output,GPIO.LOW)

    # Start GUI and define the printer and GUI properties
    gui_root = tk.Tk()   
    printer = Printer('Sintratec laser printer',ser)
    printer_gui = GUI(printer,master=gui_root)
    
    # Use default Values from Pi-config.py (not from Arduino) and set the Step size and speed
    send(ser,'M92X' +str(cfg.STEP_SIZE_X)+'Y'+str(cfg.STEP_SIZE_Y)+'Z'+str(cfg.STEP_SIZE_Z)+ '\n')
    send(ser,'G100X'+str(cfg.BED_SPEED_SLOW)+'Y'+str(cfg.BED_SPEED_SLOW)+'Z'+str(cfg.SLEDGE_SPEED_SLOW)+ '\n')
    send(ser,'G101X'+str(cfg.HOMING_SPEED_BED)+'Y'+str(cfg.HOMING_SPEED_BED)+'Z'+str(cfg.HOMING_SPEED_SLEDGE)+ '\n')
    
    msg_homed_shown = False
    
    # HEATING
    # WAIT UNTIL PRINTER IS HEATED UP
    
    # MAIN LOOP
    while True:
        try:
            if (gui_root.state() == 'normal'):
                
                # Check Homing Status and enable Buttons if homed
                if(printer.x_homed and printer.y_homed and printer.z_homed):
                    printer.homed = True
                if (printer.homed):
                    if not msg_homed_shown:
                        printer_gui.showInfoAfterHomed()
                        msg_homed_shown = True
                    printer_gui.btn_enable("btn_smooth",True)                    
                    printer_gui.btn_enable("btn_addLayer",True)
                    printer_gui.btn_enable("btn_start",True)

                # Check GPIO Pin to react on external signals
                pin_state_input = GPIO.input(cfg.pin_laser_input)
                # RTC Digital Output Pin 15: High equals pin_input = 1, Low equals 0
                if (pin_state_input==0):
                    sleep(0.5)
                    printer_gui.write_gui_output_text('Signal from Laser received',False)
                    if printer.homed: 
                        if printer.ready:
                            if not printer.ready_to_send_signal_back:
                                printer_gui.write_gui_output_text('Adding layer...',False)
                                printer.ready_to_send_signal_back = True
                                # Send G-Code to Add a layer
                                send(printer.ser, gcode.GC_Layer(printer))
                            else:
                                printer_gui.write_gui_output_text('Signal from Laser ignored: Printer is not done adding a layer yet!',False)
                        else:
                            printer_gui.write_gui_output_text('Signal from Laser ignored: Printing process was not started yet or is paused!',False)
                    else:
                        printer_gui.write_gui_output_text('Layer was not added: Printer is not homed!',False)
                
                # Auslesen des Arduinos 
                printer_gui.readout()
                # Aktualisieren der GUI
                printer_gui.update_idletasks()
                printer_gui.update()        
        except Exception:
            print('Closed GUI -> Program stoped')
            break           

if __name__ == '__main__':
    main()
