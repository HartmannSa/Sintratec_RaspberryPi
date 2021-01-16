from tkinter import *
import g_code as gc
import config as cfg
import serial

ser = serial.Serial("/dev/ttyACM0", cfg.BAUDRATE)

gui = Tk()
gui.title('GUI for laser printer')
gui.geometry("1000x500+100+200")

def endstop_status():
    gc.check_endstops(ser)
    
# Button_H = Button(gui,text='Homing',command=gc.check_endstops(ser))
Button_H = Button(gui,text='Test_function',command=endstop_status)
Button_H.pack()
# Button_H.place(x = 100, y = 490)

gui.mainloop()
# while True:
#     gui.update_idletasks()
#     gui.update()