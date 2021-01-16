import config as cfg
import time
import tkinter as tk
from tkinter import ttk

#################################################################
# G-CODE
#################################################################
# Check Parameter
M119 = 'M119\n'

# Define Command M810: M92-Stepsize settings | G28-Auto Homing | G90-Absolute Positioning | G0-Move beds to starting position
GCode_Homing ='M810 M92 X'+str(cfg.STEP_SIZE_X)+' Y'+str(cfg.STEP_SIZE_Y)+' Z'+str(cfg.STEP_SIZE_Z)+\
               '|G28 X Y Z'\
               '|G90'\
               '|G0 X'+str(cfg.POWDER_BED_HEIGHT-cfg.POWDER_FILL_HEIGHT)+' Y'+str(cfg.POWDER_BED_HEIGHT)+' F'+str(cfg.FEEDRATE_XY_FAST)+'\n'
Proceed_Homing = 'M810\n'

# Define Command M811: G90-Absolute Positioning | G0-Move sledge to start | G91-Relative Positioning |  
GCode_Smooth_Powder = 'M811 G90'\
                      '|G0 Z0 F'+str(cfg.FEEDRATE_Z_SLOW)+\
                      '|G91'\
                      '|G0 X'+str(cfg.LAYER_SMOOTHING_THICKNESS)+' Y'+str(cfg.LAYER_SMOOTHING_THICKNESS)+' F'+str(cfg.FEEDRATE_XY_FAST)+\
                      '|G0 Z'+str(cfg.SLEDGE_END_POSITION)+' F'+str(cfg.FEEDRATE_Z_SLOW)+\
                      '|G0 X'+str(-cfg.LAYER_THICKNESS)+' Y'+str(-cfg.LAYER_THICKNESS)+' F'+str(cfg.FEEDRATE_XY_SLOW)+\
                      '|G0 Z'+str(-(cfg.SLEDGE_END_POSITION-cfg.SLEDGE_MID_POSITION))+' F'+str(cfg.FEEDRATE_Z_FAST)+\
                      '|G0 Y'+str(cfg.LAYER_THICKNESS)+' F'+str(cfg.FEEDRATE_XY_SLOW)+'\n'
Proceed_Smooth_Powder = 'M811\n'

# Define Command M812: G90-Absolute Positioning | G0-Move sledge to start |
GCode_Apply_Powder_Layer = 'M812 G90'\
                           '|G0 Z0 F'+str(cfg.FEEDRATE_Z_FAST)+\
                           '|G91'\
                           '|G0 X'+str(2*cfg.LAYER_THICKNESS)+' Y'+str(-cfg.LAYER_THICKNESS)+' F'+str(cfg.FEEDRATE_XY_SLOW)+\
                           '|G0 Z'+str(cfg.SLEDGE_END_POSITION)+' F'+str(cfg.FEEDRATE_Z_SLOW)+\
                           '|G0 X'+str(-cfg.LAYER_THICKNESS)+' Y'+str(-cfg.LAYER_THICKNESS)+' F'+str(cfg.FEEDRATE_XY_SLOW)+\
                           '|G0 Z'+str(-(cfg.SLEDGE_END_POSITION-cfg.SLEDGE_MID_POSITION))+' F'+str(cfg.FEEDRATE_Z_FAST)+\
                           '|G0 Y'+str(cfg.LAYER_THICKNESS)+' F'+str(cfg.FEEDRATE_XY_SLOW)+'\n' 
Proceed_Apply_Powder_Layer = 'M812\n'

def print_gcode():
    print('G-Code Homing:\n')
    print(GCode_Homing)
    print(Proceed_Homing)
    print('\nG-Code Smooth Powder:\n')
    print(GCode_Smooth_Powder)
    print(Proceed_Smooth_Powder)
    print('\nG-Code Apply Powder Layer:\n')
    print(GCode_Apply_Powder_Layer)
    print(Proceed_Apply_Powder_Layer)

def check_endstops(ser):
    ser.write(M119.encode('utf-8'))
    readout(ser)
    
def homing(ser):
    if cfg.VERBOSE == True:
        print('Homing...')
    ser.write(GCode_Homing.encode('utf-8'))
    ser.write(Proceed_Homing.encode('utf-8'))
    time.sleep(cfg.HOMING_DURATION)
    if cfg.VERBOSE == True:
        print('Homing finished')

def smooth_powder(ser):
    if cfg.VERBOSE == True:
        print('Smooth layer of powder...')
    ser.write(GCode_Smooth_Powder.encode('utf-8'))
    ser.write(Proceed_Smooth_Powder.encode('utf-8'))
    time.sleep(cfg.SMOOTH_POWDER_DURATION)
    if cfg.VERBOSE == True:
        print('Smooth layer of powder finished')
    
def apply_powder(ser):
    if cfg.VERBOSE == True:
        print('Apply layer of powder...')
    ser.write(GCode_Apply_Powder_Layer.encode('utf-8'))
    ser.write(Proceed_Apply_Powder_Layer.encode('utf-8'))
    time.sleep(cfg.APPLY_POWDER_DURATION)
    if cfg.VERBOSE == True:
        print('Apply one layer of powder finished')
        
        
#################################################################
# GUI stuff
#################################################################
class Application(tk.Frame):
    BTN_WIDTH=10
    BTN_HEIGHT=1
    
    def __init__(self,ser,printer,master=None):
        super().__init__(master)
        self.master = master
        self.ser = ser
        self.printer = printer
        master.geometry('500x800+0+0')
        master.title('GUI for '+printer.name)
        self.create_widgets()
        
    def create_widgets(self):
        # Frame Movements
        self.lbl_frame_movements = tk.LabelFrame(self.master, bg='snow', text = 'Movements',height=str(200))
        self.lbl_frame_movements.pack(fill='both',expand='yes',anchor=tk.N)
        self.btn_endstop = tk.Button(self.lbl_frame_movements,text='Endstop status',width=Application.BTN_WIDTH,command=self.btn_check_endstops)
        self.btn_endstop.grid(row=1,column=1,padx=(10,0),pady=(10,0))
#         self.btn_endstop.place(x='0',y='0')
#         self.btn_endstop.pack(apadx=10,pady=10)
#         self.btn_endstop.pack(anchor=tk.NW,padx=10,pady=10)
        self.btn_homing = tk.Button(self.lbl_frame_movements,text='Home all axis',width=Application.BTN_WIDTH,command=self.btn_homing)
        self.btn_homing.grid(row=2,column=1,padx=(10,0),pady=(10,0))
#         self.btn_homing.place(x='140',y='0')
#         self.btn_homing.pack(anchor=tk.W,side=tk.LEFT,padx=10,pady=10)
        self.btn_smooth = tk.Button(self.lbl_frame_movements,text='Smooth powder',width=Application.BTN_WIDTH,command=self.btn_smooth_powder,state=tk.DISABLED)
        self.btn_smooth.grid(row=2,column=2,padx=(10,0),pady=(10,0))
#         self.btn_smooth.place(x='0',y='40')
#         self.btn_smooth.pack(anchor=tk.W,side=tk.LEFT,padx=10,pady=10)
        self.btn_addLayer = tk.Button(self.lbl_frame_movements,text='Add layer',width=Application.BTN_WIDTH,command=self.btn_apply_powder,state=tk.DISABLED)
        self.btn_addLayer.grid(row=3,column=1,padx=(10,0),pady=(10,0))
#         self.btn_addLayer.place(x='140',y='40')
#         self.scale_layer_thichness = tk.Scale(self.lbl_frame_movements, orient='horizontal', bg='snow', label='layer thickness')
#         self.scale_layer_thichness.place(x='280',y='40')
        self.btn_moveBeds = tk.Button(self.lbl_frame_movements,text='Move Beds',width=Application.BTN_WIDTH,command=self.btn_move_beds)
        self.btn_moveBeds.grid(row=3,column=2,padx=(10,0),pady=(10,0))
#         self.btn_moveBeds.pack(anchor=tk.SW,padx=10,pady=10)
#         self.scale_bed1 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg='snow')
#         self.scale_bed1.place(x='420',y='0')
#         self.scale_bed2 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg='snow')
#         self.scale_bed2.place(x='490',y='0')
        
        # Frame Heating
        self.lbl_frame_heating = tk.LabelFrame(self.master, bg='coral1', text = 'Heating',height=str(200))
        self.lbl_frame_heating.pack(expand='yes',fill='both',anchor=tk.N)
#         self.scale_temp1 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp1.place(x='0',y='0')
#         self.scale_temp2 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp2.place(x='140',y='0')
        
        # output window:
        self.lbl_frame_output = tk.LabelFrame(self.master, bg='white', text = 'Output',height=str(200))
        self.lbl_frame_output.pack(fill='both', expand='yes',anchor=tk.E)
#         self.mytext = tk.StringVar(value='test\n'*5)
#         self.myframe = ttk.Frame(self.master)
#         self.myentry = ttk.Entry(self.myframe,textvariable=self.mytext,state='readonly')
#         self.myscroll = ttk.Scrollbar(self.myframe,orient='vertical',command=self.myentry.xview)
#         self.myentry.config(yscrollcommand=self.myscroll.set)
#         self.myframe.grid()
#         self.myentry.grid(column=1,sticky='ew')
#         self.myscroll.grid(column=2,sticky='ew')
        
        self.btn_start = tk.Button(self.master,text='START',command=self.btn_start,bg='DarkOliveGreen1',height=Application.BTN_HEIGHT)
        self.btn_start.pack(fill='x', expand='yes',anchor=tk.S,padx='10',pady=(0,0))
        
        self.btn_stop = tk.Button(self.master,text='STOP',command=self.btn_stop,bg='red',height=Application.BTN_HEIGHT)
        self.btn_stop.pack(fill='x', expand='yes',anchor=tk.S,padx='10',pady=(1,0))
      
    def btn_destroy(self):
        self.master.destroy()
    
    def btn_check_endstops(self):
        check_endstops(self.ser)
        
    def btn_homing(self):
        homing(self.ser)
        self.printer.homed = True
        
    def btn_move_beds(self):
        pass
        
    def btn_smooth_powder(self):
#         smooth_powder(self.ser)
        self.printer.smoothed = True
        
    def btn_apply_powder(self):
        pass
#         apply_powder(self.ser)
        # send signal to laser
        
    def btn_start(self):
        print('Printing started')
        
    def btn_stop(self):
        print('Printing stopped')
        
    def btn_enable(self,btn_name,btn_var):
         if btn_name == 'btn_addLayer':
             if btn_var==True:
                 self.btn_addLayer['state']=tk.NORMAL
             else:
                 self.btn_addLayer['state']=tk.DISABLED
         elif btn_name == 'btn_smooth':
             if btn_var==True:
                 self.btn_smooth['state']=tk.NORMAL
             else:
                 self.btn_smooth['state']=tk.DISABLED
    
        

#################################################################
# printer properties
#################################################################
class printer():
    def __init__(self,NAME):
        self.name = NAME
        self.homed = False
        self.smoothed = False
        
#################################################################
# output shell
#################################################################      
def readout(ser):
    ser.flush()
    line = ser.readline().decode('utf-8').rstrip()
    while(ser.in_waiting > 0):
        ## this prints the string from the Arduino
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    ser.flush()
