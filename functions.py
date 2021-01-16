import config as cfg
import time
import tkinter as tk

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

def check_endstops(ser,gui_output_text=False):
    ser.write(M119.encode('utf-8'))
    time.sleep(0.1)
    readout(ser,gui_output_text)
    
def homing(ser):
    if cfg.VERBOSE == True:
        print('Homing all axis...')
    ser.write(GCode_Homing.encode('utf-8'))
    ser.write(Proceed_Homing.encode('utf-8'))
    time.sleep(cfg.HOMING_DURATION)
    if cfg.VERBOSE == True:
        print('Homing all axis finished')

def smooth_powder(ser):
    if cfg.VERBOSE == True:
        print('Smoothing powder...')
    ser.write(GCode_Smooth_Powder.encode('utf-8'))
    ser.write(Proceed_Smooth_Powder.encode('utf-8'))
    time.sleep(cfg.SMOOTH_POWDER_DURATION)
    if cfg.VERBOSE == True:
        print('Smoothing powder succesfull?')
    
def apply_powder(ser):
    if cfg.VERBOSE == True:
        print('Applying one layer of powder...')
#     ser.write(GCode_Apply_Powder_Layer.encode('utf-8'))
#     ser.write(Proceed_Apply_Powder_Layer.encode('utf-8'))
    time.sleep(cfg.APPLY_POWDER_DURATION)
    if cfg.VERBOSE == True:
        print('Applying one layer of powder finished')



#################################################################
# printer properties
#################################################################
class printer:
    def __init__(self,NAME,ser):
        self.name = NAME
        self.ser = ser
        self.homed = False
        self.smoothed = False
        self.layer_thickness = cfg.LAYER_THICKNESS
        self.sledge_position = 0
        self.powder_bed_position = 0
        self.workpiece_bed_position = 0
        self.ready = False
        self.sledge_max_pos = cfg.SLEDGE_END_POSITION
      
      
      
#################################################################
# output shell
#################################################################      
def readout(ser,gui_output_text=False):
    ser.flush()
    if(ser.in_waiting > 0):
        line = ser.readline().decode('utf-8').rstrip()
        while(ser.in_waiting > 0):
            ## this prints the string from the Arduino
            line = ser.readline().decode('utf-8').rstrip()
            if(gui_output_text != False):
                write_gui_output_text(gui_output_text,line)
            else:
                print(line)
            time.sleep(0.01)
        ser.flush()
    else:
        pass
       
def write_gui_output_text(stringlist,text):
    stringlist.insert(tk.END,text)
    stringlist.yview_moveto(1)
    print(text)

#################################################################
# GUI stuff
#################################################################
class Application(tk.Frame):
    BTN_WIDTH = 10 # Button width used for every button except start and stop
    FRAME_HEIGHT = 200
    
    def __init__(self,prntr,master=None):
        super().__init__(master)
        self.master = master
        self.prntr = prntr
        master.geometry('750x1000+0+0')
        master.title('GUI for '+prntr.name)
        self.lbl_frame_output = tk.LabelFrame(self.master, bg='white', text = 'Output',height=str(Application.FRAME_HEIGHT))
        self.output_text = tk.Listbox(self.lbl_frame_output,width=200)
        self.create_widgets()
        print('Creating GUI... done')
#         readout(self.prntr.ser,self.output_text)
        
    def create_widgets(self):
        # Frame printer properties
        self.lbl_frame_properties = tk.LabelFrame(self.master, bg='white', text = 'Printer properties')
        self.lbl_frame_properties.pack(fill='both',expand='yes',side=tk.TOP)
        tk.Label(self.lbl_frame_properties,text='layer thickness:',bg='white').grid(row=1,column=1,padx=(10,0),pady=(10,0))
        self.LT = tk.StringVar()
        self.LT.set(str(self.prntr.layer_thickness)+' µm')
        self.lbl_layer_thickness = tk.Label(self.lbl_frame_properties,textvariable=self.LT,bg='white')
        self.lbl_layer_thickness.grid(row=2,column=1,padx=(10,0),pady=(10,0))
        self.lt_entry = tk.Entry(self.lbl_frame_properties,width=Application.BTN_WIDTH)
        self.lt_entry.grid(row=3,column=1,pady=(10,0))
        tk.Button(self.lbl_frame_properties,text='Apply',command=self.set_layer_thickness,width=Application.BTN_WIDTH-2).grid(row=4,column=1,pady=(10,10))
        
        # Frame Movements
        self.lbl_frame_movements = tk.LabelFrame(self.master, bg='gray70', text = 'Movements',height=str(Application.FRAME_HEIGHT))
        self.lbl_frame_movements.pack(fill='both',expand='yes',side=tk.TOP)
        self.btn_endstop = tk.Button(self.lbl_frame_movements,text='Endstop status',width=Application.BTN_WIDTH,command=self.btn_endstops_fnc)
        self.btn_endstop.grid(row=2,column=1,padx=(10,0),pady=(10,0))
        self.btn_homing = tk.Button(self.lbl_frame_movements,text='Home all axes',width=Application.BTN_WIDTH,command=self.btn_homing_fnc)
        self.btn_homing.grid(row=1,column=1,padx=(10,0),pady=(10,0))
        self.btn_homing_x = tk.Button(self.lbl_frame_movements,text='Home x-axis',width=Application.BTN_WIDTH,command=self.btn_homing_x_fnc)
        self.btn_homing_x.grid(row=1,column=2,padx=(10,0),pady=(10,0))
        self.btn_homing_y = tk.Button(self.lbl_frame_movements,text='Home y-axis',width=Application.BTN_WIDTH,command=self.btn_homing_y_fnc)
        self.btn_homing_y.grid(row=1,column=3,padx=(10,0),pady=(10,0))
        self.btn_homing_z = tk.Button(self.lbl_frame_movements,text='Home z-axis',width=Application.BTN_WIDTH,command=self.btn_homing_z_fnc)
        self.btn_homing_z.grid(row=1,column=4,padx=(10,0),pady=(10,0))
        self.btn_smooth = tk.Button(self.lbl_frame_movements,text='Smooth powder',width=Application.BTN_WIDTH,command=self.btn_smooth_powder_fnc,state=tk.DISABLED)
        self.btn_smooth.grid(row=2,column=2,padx=(10,0),pady=(10,0))
        self.btn_addLayer = tk.Button(self.lbl_frame_movements,text='Add layer',width=Application.BTN_WIDTH,command=self.btn_apply_powder_fnc,state=tk.DISABLED)
        self.btn_addLayer.grid(row=2,column=3,padx=(10,0),pady=(10,0))
        self.btn_moveBeds = tk.Button(self.lbl_frame_movements,text='Move Beds',bg='antique white',width=Application.BTN_WIDTH,command=self.btn_move_beds_fnc)
        self.btn_moveBeds.grid(row=2,column=4,padx=(10,0),pady=(10,0))
        tk.Label(self.lbl_frame_movements,text='sledge position:\n[mm]',bg='gray70').grid(row=3,column=1)
        self.scale_sledge = tk.Scale(self.lbl_frame_movements,command=self.set_sledge_position,orient='horizontal', bg='antique white',from_=0,to=self.prntr.sledge_max_pos,length=380)#, label='layer thickness')
        self.scale_sledge.grid(row=3,column=2,padx=(10,0),pady=(10,10),columnspan=3)
        tk.Label(self.lbl_frame_movements,text='powder bed\n[mm]',bg='gray70').grid(row=1,column=5,padx=(10,0))
        self.scale_bed1 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg='antique white',from_=125,to=0)
        self.scale_bed1.grid(row=2,column=5,padx=(10,0),pady=(0,0),rowspan=2)
        tk.Label(self.lbl_frame_movements,text='workpiece bed\n[mm]',bg='gray70').grid(row=1,column=6,padx=(10,0))
        self.scale_bed2 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg='antique white',from_=125,to=0)
        self.scale_bed2.grid(row=2,column=6,padx=(10,0),pady=(0,0),rowspan=2)
        
        # Frame Heating
        self.lbl_frame_heating = tk.LabelFrame(self.master, bg='coral1', text = 'Heating',height=str(Application.FRAME_HEIGHT))
        self.lbl_frame_heating.pack(expand='yes',fill='both',side=tk.TOP)
#         self.scale_temp1 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp1.place(x='0',y='0')
#         self.scale_temp2 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp2.place(x='140',y='0')
        
        # Frame Output:
        self.lbl_frame_output.pack(fill='both', expand='yes',side=tk.TOP)
        self.scr_bar_vert = tk.Scrollbar(self.lbl_frame_output)
        self.scr_bar_vert.pack(side=tk.RIGHT,fill='y')
        self.scr_bar_hori = tk.Scrollbar(self.lbl_frame_output,orient=tk.HORIZONTAL)
        self.scr_bar_hori.pack(side=tk.BOTTOM,fill='x')
        self.output_text['yscrollcommand'] = self.scr_bar_vert.set
        self.output_text['xscrollcommand'] = self.scr_bar_hori.set
        self.output_text.pack(side=tk.LEFT,fill='both')
        self.scr_bar_vert.config(command=self.output_text.yview)
        self.scr_bar_hori.config(command=self.output_text.xview)
        
        # start button:
        self.btn_start = tk.Button(self.master,text='START',command=self.btn_start_fnc,bg='DarkOliveGreen1',state=tk.DISABLED)
        self.btn_start.pack(fill='both', expand='yes',side=tk.LEFT,padx='10',pady='10')
        
        # pause button:
        self.btn_pause = tk.Button(self.master,text='PAUSE',command=self.btn_pause_fnc,bg='yellow2')
        self.btn_pause.pack(fill='both', expand='yes',side=tk.LEFT,padx='10',pady='10')
        
        # stop button
        self.btn_stop = tk.Button(self.master,text='STOP',command=self.btn_stop_fnc,bg='red')
        self.btn_stop.pack(fill='both', expand='yes',side=tk.RIGHT,padx='10',pady='10')
        
# ===== widget functions =======================================================================
    def set_layer_thickness(self):
        strval=str(self.lt_entry.get())
        intval=int(self.lt_entry.get())
        if (intval <= cfg.MAX_LAYER_THICKNESS):
            self.prntr.layer_thickness = intval
            self.LT.set(strval+' µm')
            self.lt_entry.delete(0,'end')
            write_gui_output_text(self.output_text,'Changed layer thickness to '+strval+' µm')
        else:
            self.lt_entry.delete(0,'end')
            write_gui_output_text(self.output_text,'Maximum '+str(cfg.MAX_LAYER_THICKNESS)+' µm allowed')
            
        
    def set_sledge_position(self,var):
        self.prntr.sledge_position = var
#         fahre zu jener Position
        
    def set_powder_bed_position(self,var):
        self.prntr.powder_bed_position = var
#         fahre zu jener Position
        
    def set_workpiece_bed_position(self,var):
        self.prntr.workpiece_bed_position = var
#         fahre zu jener Position
    
    def btn_endstops_fnc(self):
        self.prntr.ser.write(M119.encode('utf-8'))
        readout(self.prntr.ser,self.output_text)
#         check_endstops(self.prntr.ser,self.output_text)
        
    def btn_homing_fnc(self):
        write_gui_output_text(self.output_text,'Homing all axes...')
        homing(self.prntr.ser)
        self.prntr.homed = True
        write_gui_output_text(self.output_text,'Homing all axes finished')
    
    def btn_homing_x_fnc(self):
        write_gui_output_text(self.output_text,'Homing x-axis...')
        pass
        write_gui_output_text(self.output_text,'Homing x-axis finished')
        
    def btn_homing_y_fnc(self):
        write_gui_output_text(self.output_text,'Homing y-axis...')
        pass
        write_gui_output_text(self.output_text,'Homing y-axis finished')
        
    def btn_homing_z_fnc(self):
        write_gui_output_text(self.output_text,'Homing z-axis...')
        pass
        write_gui_output_text(self.output_text,'Homing z-axis finished')
        
    def btn_move_beds_fnc(self):
        write_gui_output_text(self.output_text,'Moving beds...')
        pass
        write_gui_output_text(self.output_text,'Moving beds finished')
        
    def btn_smooth_powder_fnc(self):
        write_gui_output_text(self.output_text,'Smoothing powder...')
#         smooth_powder(self.prntr.ser)
        self.prntr.smoothed = True
        write_gui_output_text(self.output_text,'Smoothing powder succesfull?')
        
    def btn_apply_powder_fnc(self):
        write_gui_output_text(self.output_text,'Applying powder...')
#         apply_powder(self.prntr.ser)
        write_gui_output_text(self.output_text,'Applying powder finished')
        # send signal to laser
        
    def btn_start_fnc(self):
        write_gui_output_text(self.output_text,'Printing started')
        
    def btn_pause_fnc(self):
        write_gui_output_text(self.output_text,'Printing paused')
        
    def btn_stop_fnc(self):
        write_gui_output_text(self.output_text,'Printing stopped')
#         self.master.destroy()
        
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
    