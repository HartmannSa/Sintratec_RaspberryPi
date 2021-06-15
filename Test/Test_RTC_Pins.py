import config as cfg
import RPi.GPIO as GPIO
from gcode import *
from time import sleep
from printer import *
from functions import *
 

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setwarnings(False)
# Setup Pin for receiving signal from laser:
GPIO.setup(cfg.pin_laser_input,GPIO.IN,pull_up_down=GPIO.PUD_UP) #GPIO.PUD_UP (RTC OUT Low=0, high=1) and PUD_DOWN (Low=0, high=1)
# Setup Pin for sending a signal to laser:
GPIO.setup(cfg.pin_laser_output,GPIO.OUT)
GPIO.output(cfg.pin_laser_output,GPIO.LOW)

ready_to_send_signal_back = False
intervall = 1

while True:
    try:
        #GPIO.output(cfg.pin_laser_output,GPIO.HIGH)
        #sleep(2*intervall)
        #GPIO.output(cfg.pin_laser_output,GPIO.LOW)      
        #sleep(2*intervall)
        
        # Add Layer if Laser is triggered
        pin_state_input = GPIO.input(cfg.pin_laser_input)
        # For Pull_Up: Laser is triggerd if button_state == 0
        if (pin_state_input==1):
            print('Signal from Laser received')                              
            sleep(3)
            print('Sending Signal back')  
            GPIO.output(cfg.pin_laser_output,GPIO.HIGH)
            sleep(cfg.time_output_signal)
            GPIO.output(cfg.pin_laser_output,GPIO.LOW)
            sleep(0.01)
            print('Done')         
        else:
            sleep(0.01)
            print('nope')            
    except Exception:
        print('Closed GUI -> Program stoped')
        break         
