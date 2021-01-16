import config as cfg
import tkinter as tk
from gcode import *
from time import sleep
from functions import *

class GUI(tk.Frame):
    def __init__(self,printer,master=None):
        super().__init__(master)
        self.master = master
        self.prntr = printer
        master.geometry(str(cfg.GUI_WIDTH)+'x'+str(cfg.GUI_HEIGHT)+'+0+0')
        master.title('GUI for '+printer.name)
        self.create_widgets()
        print('Creating GUI... done')
        
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
                 
    def update_strvars(self):
        self.strvar_SledgePos.set('Sledge = '+str(self.prntr.sledge_position)+'mm')
        self.strvar_PowderBedPos.set('Powder bed = '+str(self.prntr.powder_bed_position)+'mm')
        self.strvar_WorkpieceBedPos.set('Workpiece bed = '+str(self.prntr.workpiece_bed_position)+'mm')
        self.strvar_LT.set(str(self.prntr.layer_thickness)+'mm')

    def create_widgets(self):
        # Frames
        self.lbl_frame_properties = tk.LabelFrame(self.master, bg='white', text = 'Printer properties',height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_properties.pack(fill='both',expand='yes',side=tk.TOP)
        self.lbl_frame_movements = tk.LabelFrame(self.master, bg='gray70', text = 'Movements',height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_movements.pack(fill='both',expand='yes',side=tk.TOP)
        self.lbl_frame_heating = tk.LabelFrame(self.master, bg='coral1', text = 'Heating',height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_heating.pack(expand='yes',fill='both',side=tk.TOP)
        self.lbl_frame_input = tk.LabelFrame(self.master, bg='white', text = 'Input',height=str(10))
        self.lbl_frame_input.pack(fill='both', expand='yes',side=tk.TOP)
        self.lbl_frame_output = tk.LabelFrame(self.master, bg='white', text = 'Output',height=str((cfg.FRAME_HEIGHT)*2))
        self.lbl_frame_output.pack(fill='both', expand='yes',side=tk.TOP)
        
        # Printer properties
        tk.Label(self.lbl_frame_properties,text='layer thickness:',bg='white').grid(row=1,column=1,padx=(10,0),pady=(10,0))
        self.strvar_LT = tk.StringVar()
#         self.strvar_LT.set(str(self.prntr.layer_thickness)+'mm')
        self.lbl_layer_thickness = tk.Label(self.lbl_frame_properties,textvariable=self.strvar_LT,bg='white')
        self.lbl_layer_thickness.grid(row=2,column=1,padx=(10,0),pady=(10,0))
        self.lt_entry = tk.Entry(self.lbl_frame_properties,width=cfg.BTN_WIDTH)
        self.lt_entry.grid(row=3,column=1,pady=(10,0))
        tk.Button(self.lbl_frame_properties,text='Apply',command=self.btn_set_layer_thickness,width=cfg.BTN_WIDTH-2).grid(row=4,column=1,pady=(10,0))
        self.btn_endstop = tk.Button(self.lbl_frame_properties,text='Endstop status',width=cfg.BTN_WIDTH,command=self.btn_endstops_fnc)
        self.btn_endstop.grid(row=5,column=1,pady=(10,0))
        tk.Label(self.lbl_frame_properties,text='Positions:',bg='white').grid(row=1,column=2,padx=(10,0),pady=(10,0))
        self.strvar_PowderBedPos = tk.StringVar()
#         self.strvar_PowderBedPos.set('Powder bed = '+str(self.prntr.powder_bed_position)+'mm')
        self.lbl_powder_bed_pos = tk.Label(self.lbl_frame_properties,textvariable=self.strvar_PowderBedPos,bg='white')
        self.lbl_powder_bed_pos.grid(row=2,column=2,padx=(10,0),pady=(10,0))
        self.strvar_WorkpieceBedPos = tk.StringVar()
#         self.strvar_WorkpieceBedPos.set('Workpiece bed = '+str(self.prntr.workpiece_bed_position)+'mm')
        self.lbl_workpiece_bed_pos = tk.Label(self.lbl_frame_properties,textvariable=self.strvar_WorkpieceBedPos,bg='white')
        self.lbl_workpiece_bed_pos.grid(row=3,column=2,padx=(10,0),pady=(10,0))
        self.strvar_SledgePos = tk.StringVar()
#         self.strvar_SledgePos.set('Sledge = '+str(self.prntr.sledge_position)+'mm')
        self.lbl_sledge_pos = tk.Label(self.lbl_frame_properties,textvariable=self.strvar_SledgePos,bg='white')
        self.lbl_sledge_pos.grid(row=4,column=2,padx=(10,0),pady=(10,0))
        
        # Movements
        self.btn_homing = tk.Button(self.lbl_frame_movements,text='Home all axes',width=cfg.BTN_WIDTH,command=self.btn_homing_fnc)
        self.btn_homing.grid(row=1,column=1,padx=(10,0),pady=(10,0))
        self.btn_homing_x = tk.Button(self.lbl_frame_movements,text='Home x-axis',width=cfg.BTN_WIDTH,command=self.btn_homing_x_fnc)
        self.btn_homing_x.grid(row=1,column=2,padx=(10,0),pady=(10,0))
        self.btn_homing_y = tk.Button(self.lbl_frame_movements,text='Home y-axis',width=cfg.BTN_WIDTH,command=self.btn_homing_y_fnc)
        self.btn_homing_y.grid(row=1,column=3,padx=(10,0),pady=(10,0))
        self.btn_homing_z = tk.Button(self.lbl_frame_movements,text='Home z-axis',width=cfg.BTN_WIDTH,command=self.btn_homing_z_fnc)
        self.btn_homing_z.grid(row=1,column=4,padx=(10,0),pady=(10,0))
        self.btn_smooth = tk.Button(self.lbl_frame_movements,text='Smooth powder',width=cfg.BTN_WIDTH,command=self.btn_smooth_powder_fnc,state=tk.DISABLED)
        self.btn_smooth.grid(row=2,column=1,padx=(10,0),pady=(10,0))
        self.btn_addLayer = tk.Button(self.lbl_frame_movements,text='Add layer',width=cfg.BTN_WIDTH,command=self.btn_apply_powder_fnc,state=tk.DISABLED)
        self.btn_addLayer.grid(row=2,column=2,padx=(10,0),pady=(10,0))
        self.btn_moveBeds = tk.Button(self.lbl_frame_movements,text='Move Beds',bg='antique white',width=cfg.BTN_WIDTH,command=self.btn_move_beds_fnc)
        self.btn_moveBeds.grid(row=2,column=4,padx=(10,0),pady=(10,0))
        tk.Label(self.lbl_frame_movements,text='sledge position:\n[mm]',bg='gray70').grid(row=3,column=1)
        self.scale_sledge = tk.Scale(self.lbl_frame_movements,command=self.scale_sledge_fnc,orient='horizontal', bg='antique white',from_=0,to=cfg.SLEDGE_END_POS,length=380)#,variable=self.prntr.sledge_position)#, label='layer thickness')
        self.scale_sledge.grid(row=3,column=2,padx=(10,0),pady=(10,10),columnspan=3)
        tk.Label(self.lbl_frame_movements,text='powder bed\n[mm]',bg='gray70').grid(row=1,column=5,padx=(10,0))
        self.scale_bed1 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg='antique white',from_=125,to=0)
        self.scale_bed1.grid(row=2,column=5,padx=(10,0),pady=(0,0),rowspan=2)
        tk.Label(self.lbl_frame_movements,text='workpiece bed\n[mm]',bg='gray70').grid(row=1,column=6,padx=(10,0))
        self.scale_bed2 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg='antique white',from_=125,to=0)
        self.scale_bed2.grid(row=2,column=6,padx=(10,0),pady=(0,0),rowspan=2)
        
        # Heating
#         self.scale_temp1 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp1.place(x='0',y='0')
#         self.scale_temp2 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp2.place(x='140',y='0')

        # Input:
        self.input_entry = tk.Entry(self.lbl_frame_input)
        self.input_entry.pack(side=tk.LEFT,expand='yes',fill='x')
        tk.Button(self.lbl_frame_input,text='Send',command=self.btn_send_fnc,width=cfg.BTN_WIDTH).pack(side=tk.RIGHT)
        
        # Output:
        self.scr_bar_vert = tk.Scrollbar(self.lbl_frame_output)
        self.scr_bar_vert.pack(side=tk.RIGHT,fill='y')
        self.scr_bar_hori = tk.Scrollbar(self.lbl_frame_output,orient=tk.HORIZONTAL)
        self.scr_bar_hori.pack(side=tk.BOTTOM,fill='x')
        self.output_text = tk.Listbox(self.lbl_frame_output,width=200)
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
        
        
        
# **********************************************************************************************
#                                                                                              *
#                                 Printer properties - functions                               *
#                                                                                              *
# **********************************************************************************************
    def btn_set_layer_thickness(self):
        strval=str(self.lt_entry.get())
        floatval=float(self.lt_entry.get())
        if (floatval <= cfg.LAYER_THICKNESS_MAX) & (floatval > 0):
            self.prntr.layer_thickness = floatval
            self.lt_entry.delete(0,'end')
            self.write_gui_output_text('Changed layer thickness to '+strval+'mm')
        else:
            self.lt_entry.delete(0,'end')
            self.write_gui_output_text('Maximum '+str(cfg.LAYER_THICKNESS_MAX)+'mm allowed')
            
    def btn_endstops_fnc(self):
        send(self.prntr.ser,GC_Endstops)
            
            
# **********************************************************************************************
#                                                                                              *
#                                 Movement - functions                                         *
#                                                                                              *
# **********************************************************************************************
    def scale_sledge_fnc(self,var):
        self.prntr.sledge_position = var
#         fahre zu jener Position
        
    def scale_powder_bed_fnc(self,var):
        self.prntr.powder_bed_position = var
#         fahre zu jener Position
        
    def scale_workpiece_bed_fnc(self,var):
        self.prntr.workpiece_bed_position = var
#         fahre zu jener Position
        
    def btn_homing_fnc(self):
        send(self.prntr.ser,GC_Homing)
        self.prntr.homed = True
        self.prntr.sledge_position = 0
        self.prntr.powder_bed_position = 0
        self.prntr.workpiece_bed_position = 0
    
    def btn_homing_x_fnc(self):
        send(self.prntr.ser,GC_Home_X)
        self.prntr.x_homed = True
        self.prntr.powder_bed_position = 0
        
    def btn_homing_y_fnc(self):
        send(self.prntr.ser,GC_Home_Y)
        self.prntr.y_homed = True
        self.prntr.workpiece_bed_position = 0
        
    def btn_homing_z_fnc(self):
        send(self.prntr.ser,GC_Home_Z)
        self.prntr.z_homed = True
        self.prntr.sledge_position = 0
        
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
        
# **********************************************************************************************
#                                                                                              *
#                                 Input console - functions                                    *
#                                                                                              *
# **********************************************************************************************
    def btn_send_fnc(self):
        strval=str(self.input_entry.get())
        send(self.prntr.ser,strval+'\n')
        self.input_entry.delete(0,'end')
        
        
# **********************************************************************************************
#                                                                                              *
#                                 Output console - functions                                   *
#                                                                                              *
# **********************************************************************************************
    def write_gui_output_text(self,txt):
        self.output_text.insert(tk.END,txt)
        self.output_text.yview_moveto(1)

    def readout(self):
        while(self.prntr.ser.in_waiting > 0):
            line = self.prntr.ser.readline().decode('utf-8').rstrip()
            self.write_gui_output_text(line)
            sleep(0.01)
        
        
# **********************************************************************************************
#                                                                                              *
#                                 Start, pause & stop - functions                              *
#                                                                                              *
# **********************************************************************************************
    def btn_start_fnc(self):
        write_gui_output_text(self.output_text,'Printing started')
        
    def btn_pause_fnc(self):
        send(self.prntr.ser,'pause\n')
        
    def btn_stop_fnc(self):
        send(self.prntr.ser,'stop\n')