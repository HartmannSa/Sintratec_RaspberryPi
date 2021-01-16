import RPi.GPIO as GPIO
from time import sleep

''' Test script to check if a
Button (e.g connected to pin 23) works'''

# Set Button
Button = 23

# Setup Button
GPIO.setmode(GPIO.BCM)
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
flag = 0
cnt=0

while True:
    button_state = GPIO.input(Button)
    # For Pull_Down: Button is triggerd if button_state ==1
    # For Pull_Up: Button is triggerd if button_state == 0
    if (button_state==0):
        sleep(0.5)
        if flag==0:
            flag=1
    if flag==1:
        print(cnt)
        cnt+=1
        sleep(3)
        flag = 0