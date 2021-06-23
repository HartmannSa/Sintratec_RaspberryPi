import config as cfg
import tkinter as tk
import RPi.GPIO as GPIO
from gcode import *
from time import sleep
from functions import *
from tkinter import messagebox
#from PIL import ImageTK, Image

class GUI(tk.Frame):
    def __init__(self,printer,master=None):
        super().__init__(master)
        self.master = master
        self.prntr = printer
        master.geometry(str(cfg.GUI_WIDTH)+'x'+str(cfg.GUI_HEIGHT)+'+'+str(cfg.GUI_POS_X)+'+'+str(cfg.GUI_POS_Y))
        # Größe&Posiion der Gui von Bildschirmecke unten links im Format: BreitexHöhe+PosX+PosY
        master.title('GUI for '+printer.name)
        self.create_widgets()
        print('Creating GUI... done')
        self.process_paused = False
        
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
         elif btn_name == 'btn_start':
             if btn_var==True:
                 self.btn_start['state']=tk.NORMAL
             else:
                 self.btn_start['state']=tk.DISABLED
                 
    def update_strvars(self):
        self.strvar_LT.set(str(self.prntr.layer_thickness))
        self.strvar_LT_smoothing.set(str(self.prntr.layer_thickness_smoothing))
        self.strvar_sledge_step.set(str(self.prntr.sledge_step)+' mm')
        self.strvar_bed_x_step.set(str(self.prntr.bed_x_step)+' mm')
        self.strvar_bed_y_step.set(str(self.prntr.bed_y_step)+' mm')
        #self.strvar_mode_secure.set(str(self.prntr.mode_secure))
        self.update_labels()
        self.strvar_bed_speed.set(str(self.prntr.bed_speed))
        self.strvar_sledge_speed.set(str(self.prntr.sledge_speed))
        self.strvar_xsteps.set(str(self.prntr.step_size_x))
        self.strvar_ysteps.set(str(self.prntr.step_size_y))
        self.strvar_zsteps.set(str(self.prntr.step_size_z))
        self.scale_sledge.set(self.prntr.sledge_position)
        self.scale_bed1.set(self.prntr.powder_bed_position)
        self.scale_bed2.set(self.prntr.workpiece_bed_position)
        
    def update_labels(self):
        # Red Marking for NOT SECURE MODE
        if (str(self.prntr.mode_secure)==str(1)):
            self.strvar_mode_secure.set('on')
            self.btn_mode.config(text='Turn off')
            self.lbl_mode_secure.config(bg=cfg.lblFrame_Movements_color)
            self.lbl_frame_movements.config(bg=cfg.lblFrame_Movements_color)
        else:
            self.strvar_mode_secure.set('off')
            self.lbl_mode_secure.config(bg=cfg.scaleChanged_color)
            self.lbl_frame_movements.config(bg=cfg.scaleChanged_color)
            self.btn_mode.config(text='Turn on')
        # Warnings for Homing
        if (self.prntr.x_homed):
            self.lbl_warning_x.config(text='')        
        else:
            self.lbl_warning_x.config(text='Axis not homed')
        if (self.prntr.y_homed):
            self.lbl_warning_y.config(text='')        
        else:
            self.lbl_warning_y.config(text='Axis not homed')
        if (self.prntr.z_homed):
            self.lbl_warning_z.config(text='')        
        else:
            self.lbl_warning_z.config(text='Axis not homed')
        
 
    def process_dataline(self, line):
        # line enhält Daten im folgenden Format:
        # pos x | pos y | pos z | step x | step y | step z | speed x | speed y | speed z
        try:
            data = line.split('|')
            self.prntr.powder_bed_position = data[0]    # pos X
            self.prntr.workpiece_bed_position = data[1] # pos Y
            self.prntr.sledge_position = data[2]        # pos Z
            self.prntr.step_size_x = data[3]            # step x
            self.prntr.step_size_y = data[4]            # step y
            self.prntr.step_size_z = data[5]            # step z
            self.prntr.bed_speed = data[6]              # speed x
            self.prntr.sledge_speed = data[8]           # speed z
            self.prntr.mode_secure = data[9]            # Mode Secure
            self.update_strvars()
        except Exception:
            self.write_gui_output_text('Failed to process dataline: ' + str(line),False)
            
    def readout(self):
        while(self.prntr.ser.in_waiting > 0): # Solange Lines im Buffer sind
            line = self.prntr.ser.readline().decode('utf-8').rstrip()  # Line wird aus dem Puffer in Variable line geschoben          
            if ('|' in line):
                # Auslesen und Verarbeiten der nächsten Linie, die Positionsdaten enthält
                self.process_dataline(line)
            else:
                self.write_gui_output_text(line,True)
            if (line == 'Homing x-axis done'):
                self.prntr.x_homed = True
            if (line == 'Homing y-axis done'):
                self.prntr.y_homed = True
            if (line == 'Homing z-axis done'):
                self.prntr.z_homed = True
            #if ("macro 4 done" in line): 
                #self.showInfoAfterSmoothed() 
            if ("macro 5 done" in line) and self.prntr.ready_to_send_signal_back:
                self.prntr.ready_to_send_signal_back = False
                GPIO.output(cfg.pin_laser_output,True)
                sleep(cfg.time_output_signal)
                GPIO.output(cfg.pin_laser_output,False)
            sleep(0.01)
       
    def keybinding_Esc(self, event):
        self.master.destroy()       
        
    def create_widgets(self):
        self.master.bind('<Key-Escape>', self.keybinding_Esc)
        
        # Frames
        self.lbl_frame_first = tk.LabelFrame(self.master, bd=0, bg=cfg.lblFrame_First_color,height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_first.pack(fill='both',expand='yes',side=tk.TOP)
        self.lbl_frame_general = tk.LabelFrame(self.lbl_frame_first, bg=cfg.lblFrame_First_color, text = 'General',height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_general.pack(fill='both',expand='yes',side=tk.LEFT)
        self.lbl_frame_homing = tk.LabelFrame(self.lbl_frame_first, bg=cfg.lblFrame_First_color, text = 'Homing',height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_homing.pack(fill='both',expand='yes',side=tk.LEFT)
        
        self.lbl_frame_second = tk.LabelFrame(self.master, bg=cfg.lblFrame_Movements_color, text = 'Movements and Macros',height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_second.pack(fill='both',expand='yes',side=tk.TOP)
        self.lbl_frame_movements = tk.LabelFrame(self.lbl_frame_second,bd=0, bg=cfg.lblFrame_Movements_color,height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_movements.pack(fill='both',expand='yes',side=tk.LEFT)
        self.lbl_frame_macros = tk.LabelFrame(self.lbl_frame_second,bd=0, bg=cfg.lblFrame_Movements_color,height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_macros.pack(fill='both',expand='yes',side=tk.LEFT)
        
#         self.lbl_frame_movements = tk.LabelFrame(self.master, bg=cfg.lblFrame_Movements_color, text = 'Movements',height=str(cfg.FRAME_HEIGHT))
#         self.lbl_frame_movements.pack(fill='both',expand='yes',side=tk.TOP)
#         self.lbl_frame_properties = tk.LabelFrame(self.master, bg=cfg.lblFrame_PrinterProperties_color, text = 'Printer properties',height=str(cfg.FRAME_HEIGHT))
#         self.lbl_frame_properties.pack(fill='both',expand='yes',side=tk.TOP)
        self.lbl_frame_heating = tk.LabelFrame(self.master, bg=cfg.lblFrame_Heating_color, text = 'Heating',height=str(cfg.FRAME_HEIGHT))
        self.lbl_frame_heating.pack(expand='yes',fill='both',side=tk.TOP)
        self.lbl_frame_input = tk.LabelFrame(self.master, bg=cfg.lblFrame_Input_color, text = 'Input',height=str(10))
        self.lbl_frame_input.pack(fill='both', expand='yes',side=tk.TOP)
        self.lbl_frame_output = tk.LabelFrame(self.master, bg=cfg.lblFrame_Output_color, text = 'Output',height=str((cfg.FRAME_HEIGHT)*2))
        self.lbl_frame_output.pack(fill='both', expand='yes',side=tk.TOP)
              
        
        # ********************************************************************************************************************************************#
        # General                                                                                                                        #
        # ********************************************************************************************************************************************# 
        # EndstopStatus
        self.btn_endstop = tk.Button(self.lbl_frame_general,text='Endstop status',command=self.btn_endstops_fnc)
        self.btn_endstop.grid(row=1,column=1,padx=(0,0), pady=(10,0))
        
        # Macros
        self.btn_macros = tk.Button(self.lbl_frame_general,text='Macros',width=cfg.BTN_WIDTH,command=self.btn_macros_fnc)
        self.btn_macros.grid(row=1,column=2,padx=(10,0),pady=(10,0), columnspan=2)
        
        # Disable Motors
        self.btn_disable_motors = tk.Button(self.lbl_frame_general,text='Disable Motors',width=cfg.BTN_WIDTH,command=self.btn_disable_motors)
        self.btn_disable_motors.grid(row=1,column=4,padx=(10,0),pady=(10,0), columnspan=2)
        
        # Enable Motors
        self.btn_enable_motors = tk.Button(self.lbl_frame_general,text='Enable Motors',width=cfg.BTN_WIDTH,command=self.btn_enable_motors)
        self.btn_enable_motors.grid(row=1,column=6,padx=(10,0),pady=(10,0), columnspan=2)
        
        # Step sizes
        tk.Label(self.lbl_frame_general,text='Stepsizes [steps/mm]:',bg=cfg.lblFrame_First_color).grid(row=2,column=1,padx=(10,0),pady=(10,0))
        tk.Label(self.lbl_frame_general,text='Bed (x) = ',bg=cfg.lblFrame_First_color).grid(row=2,column=2,padx=(cfg.pad_x,0),pady=(10,0),sticky='E')
        self.strvar_xsteps = tk.StringVar()
        self.strvar_xsteps.set(str(self.prntr.step_size_x))
        self.lbl_xsteps = tk.Label(self.lbl_frame_general,textvariable=self.strvar_xsteps,bg=cfg.lblFrame_First_color)
        self.lbl_xsteps.grid(row=2,column=3,padx=(0,0),pady=(10,0),sticky='W')
        
        tk.Label(self.lbl_frame_general,text='Bed (y) = ',bg=cfg.lblFrame_First_color).grid(row=2,column=4,padx=(cfg.pad_x,0),pady=(10,0),sticky='E')
        self.strvar_ysteps = tk.StringVar()
        self.strvar_ysteps.set(str(self.prntr.step_size_y))
        self.lbl_ysteps = tk.Label(self.lbl_frame_general,textvariable=self.strvar_ysteps,bg=cfg.lblFrame_First_color)
        self.lbl_ysteps.grid(row=2,column=5,padx=(0,0),pady=(10,0),sticky='W')
        
        tk.Label(self.lbl_frame_general,text='Sledge (z) = ',bg=cfg.lblFrame_First_color).grid(row=2,column=6,padx=(cfg.pad_x,0),pady=(10,0),sticky='E')
        self.strvar_zsteps = tk.StringVar()
        self.strvar_zsteps.set(str(self.prntr.step_size_z))
        self.lbl_zsteps = tk.Label(self.lbl_frame_general,textvariable=self.strvar_zsteps,bg=cfg.lblFrame_First_color)
        self.lbl_zsteps.grid(row=2,column=7,padx=(0,0),pady=(10,0),sticky='W')
        
        # ********************************************************************************************************************************************#
        # Homing                                                                                                                          #
        # ********************************************************************************************************************************************#
        # Buttons Homing
        self.btn_homing = tk.Button(self.lbl_frame_homing,text='Home all axes',width=cfg.BTN_WIDTH+5,command=self.btn_homing_fnc)
        self.btn_homing.grid(row=1,column=1,padx=(10,0),pady=(10,0))
        self.btn_homing_x = tk.Button(self.lbl_frame_homing,text='Home x-axis',width=cfg.BTN_WIDTH,command=self.btn_homing_x_fnc)
        self.btn_homing_x.grid(row=1,column=2,padx=(10,0),pady=(10,0))
        self.btn_homing_y = tk.Button(self.lbl_frame_homing,text='Home y-axis',width=cfg.BTN_WIDTH,command=self.btn_homing_y_fnc)
        self.btn_homing_y.grid(row=1,column=3,padx=(10,0),pady=(10,0))
        self.btn_homing_z = tk.Button(self.lbl_frame_homing,text='Home z-axis',width=cfg.BTN_WIDTH,command=self.btn_homing_z_fnc)
        self.btn_homing_z.grid(row=1,column=4,padx=(10,0),pady=(10,0))
        
        tk.Label(self.lbl_frame_homing,text='Homing Speed [mm/s]:',bg=cfg.lblFrame_First_color).grid(row=2,column=1,padx=(10,0),pady=(10,0))
        tk.Label(self.lbl_frame_homing,text= cfg.HOMING_SPEED_BED ,bg=cfg.lblFrame_First_color).grid(row=2,column=2,padx=(10,0),pady=(10,0))
        tk.Label(self.lbl_frame_homing,text= cfg.HOMING_SPEED_BED ,bg=cfg.lblFrame_First_color).grid(row=2,column=3,padx=(10,0),pady=(10,0))
        tk.Label(self.lbl_frame_homing,text= cfg.HOMING_SPEED_SLEDGE,bg=cfg.lblFrame_First_color).grid(row=2,column=4,padx=(10,0),pady=(10,0))
        
        # ********************************************************************************************************************************************#
        # Movements                                                                                                                          #
        # ********************************************************************************************************************************************#
            # Button Move Beds
        self.btn_moveBeds = tk.Button(self.lbl_frame_movements,text='Move',width=4*cfg.BTN_WIDTH_SMALL, bg=cfg.moveBeds_color,command=self.btn_move_beds_fnc)
        self.btn_moveBeds.grid(row=1,column=1,padx=(10,0),pady=(10,0), columnspan=4)
            # Button Undo 
        self.btn_undo = tk.Button(self.lbl_frame_movements,text='Undo',width=4*cfg.BTN_WIDTH_SMALL, bg=cfg.moveBeds_color,command=self.btn_undo_fnc)
        self.btn_undo.grid(row=1,column=5,padx=(10,0),pady=(10,0), columnspan=4)
        
            # Sledge Position - label, scale
        tk.Label(self.lbl_frame_movements,text='sledge position\n(z) [mm]',bg=cfg.lblFrame_Movements_color).grid(row=2,column=1,padx=(10,0),pady=(10,0), columnspan =2)
            # Button Steps
        self.btn_sledge_left = tk.Button(self.lbl_frame_movements,text='<',bg=cfg.moveBeds_color,width=cfg.BTN_WIDTH_SMALL,command=self.btn_step_sledge_left_fnc)
        self.btn_sledge_left.grid(row=2,column=3,padx=(10,0),pady=(10,0))
        self.btn_sledge_right = tk.Button(self.lbl_frame_movements,text='>',bg=cfg.moveBeds_color,width=cfg.BTN_WIDTH_SMALL,command=self.btn_step_sledge_right_fnc)
        self.btn_sledge_right.grid(row=2,column=4,padx=(0,0),pady=(10,0))
            # Label output "10mm"
        self.strvar_sledge_step = tk.StringVar()
        self.strvar_sledge_step.set(str(self.prntr.sledge_step)+' mm')
        self.lbl_sledge_step = tk.Label(self.lbl_frame_movements,textvariable=self.strvar_sledge_step,bg=cfg.lblFrame_Movements_color)
        self.lbl_sledge_step.grid(row=2,column=5,padx=(10,0),pady=(10,0))
            # Entry
        self.sledge_step_entry = tk.Entry(self.lbl_frame_movements,width=cfg.BTN_WIDTH_SMALL)
        self.sledge_step_entry.grid(row=2,column=6,pady=(10,0))
        self.sledge_step_entry.bind('<Return>', self.btn_set_sledge_step )
            # Apply Button
        tk.Button(self.lbl_frame_movements,text='Apply',command=self.btn_set_sledge_step,width=cfg.BTN_WIDTH_SMALL).grid(row=2,column=7,pady=(10,0))
            
            # Label Homing Warning
        self.lbl_warning_z = tk.Label(self.lbl_frame_movements,text='Axis not homed!',fg=cfg.scaleChanged_color,bg=cfg.lblFrame_Movements_color)
        self.lbl_warning_z.grid(row=3,column=1,padx=(10,0),pady=(10,0), columnspan=2)
            # Sledge scale
        self.scale_sledge = tk.Scale(self.lbl_frame_movements,orient='horizontal', bg=cfg.moveBeds_color,from_=cfg.SLEDGE_MAX_POS,to=0,length=200)#250, variable=self.prntr.sledge_position)#, label='layer thickness')
        self.scale_sledge.bind("<ButtonRelease-1>", self.scale_sledge_fnc)
        self.scale_sledge.grid(row=3,column=3,padx=(10,0),pady=(10,10),columnspan=4)
        
#             # Label Homing Warning
#         self.lbl_warning = tk.Label(self.lbl_frame_movements,text='Axes not homed!',fg=cfg.scaleChanged_color,bg=cfg.lblFrame_Movements_color)
#         self.lbl_warning.grid(row=3,column=7,padx=(10,0),pady=(10,0))
            
            # Workpiece bed (Y)- label
        tk.Label(self.lbl_frame_movements,text='workpiece bed\n(y) [mm]',bg=cfg.lblFrame_Movements_color).grid(row=4,column=1,padx=(10,0), columnspan=2)
            # Label Homing Warning
        self.lbl_warning_y = tk.Label(self.lbl_frame_movements,text='Axis not homed!',fg=cfg.scaleChanged_color,bg=cfg.lblFrame_Movements_color)
        self.lbl_warning_y.grid(row=5,column=1,padx=(10,0),pady=(10,0), columnspan=2)
            #  Scale
        self.scale_bed2 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg=cfg.moveBeds_color,from_=cfg.BED_MAX_POS,to=0)
        self.scale_bed2.bind("<ButtonRelease-1>", self.scale_workpiece_bed_fnc)
        self.scale_bed2.grid(row=4,column=3,padx=(10,0),pady=(0,0),rowspan=2, columnspan=2)
            # Button Steps Workpiece Bed
        self.btn_bed_y_up = tk.Button(self.lbl_frame_movements,text='^',bg=cfg.moveBeds_color,width=cfg.BTN_WIDTH_SMALL,command=self.btn_step_bed_y_up_fnc)
        self.btn_bed_y_up.grid(row=6,column=3,padx=(10,0),pady=(10,0))
        self.btn_bed_y_down = tk.Button(self.lbl_frame_movements,text='v',bg=cfg.moveBeds_color,width=cfg.BTN_WIDTH_SMALL,command=self.btn_step_bed_y_down_fnc)
        self.btn_bed_y_down.grid(row=6,column=4,padx=(0,0),pady=(10,0))
            # Label output "10mm"
        self.strvar_bed_y_step = tk.StringVar()
        self.strvar_bed_y_step.set(str(self.prntr.bed_y_step)+' mm')
        self.lbl_bed_y_step = tk.Label(self.lbl_frame_movements, textvariable=self.strvar_bed_y_step, width=cfg.BTN_WIDTH, bg=cfg.lblFrame_Movements_color)
        self.lbl_bed_y_step.grid(row=6,column=1,padx=(10,0),pady=(10,0), columnspan=2, sticky='E')
            # Entry
        self.bed_y_step_entry = tk.Entry(self.lbl_frame_movements,width=cfg.BTN_WIDTH)
        self.bed_y_step_entry.grid(row=7,column=1,padx=(10,0), pady=(0,0), columnspan=2, sticky='E')
        self.bed_y_step_entry.bind('<Return>', self.btn_set_bed_y_step )
            # Apply Button
        tk.Button(self.lbl_frame_movements,text='Apply',command=self.btn_set_bed_y_step,width=cfg.BTN_WIDTH_SMALL).grid(row=7,column=3,padx=(10,0),pady=(0,0)) 
        
            # Powder Bed - label, scale
        self.scale_bed1 = tk.Scale(self.lbl_frame_movements, orient='vertical', bg=cfg.moveBeds_color,from_=cfg.BED_MAX_POS,to=0)
        self.scale_bed1.bind("<ButtonRelease-1>", self.scale_powder_bed_fnc)
        self.scale_bed1.grid(row=4,column=5,padx=(0,0),pady=(0,0),rowspan=2, columnspan=2)
        tk.Label(self.lbl_frame_movements,text='powder bed\n(x) [mm]',bg=cfg.lblFrame_Movements_color).grid(row=4,column=7,padx=(0,0), sticky='E', columnspan=2)
            # Label Homing Warning
        self.lbl_warning_x = tk.Label(self.lbl_frame_movements,text='Axis not homed!',fg=cfg.scaleChanged_color,bg=cfg.lblFrame_Movements_color)
        self.lbl_warning_x.grid(row=5,column=7,padx=(10,0),pady=(10,0), columnspan=2)
           # Button Steps Powder Bed (x)
        self.btn_bed_x_up = tk.Button(self.lbl_frame_movements,text='^',bg=cfg.moveBeds_color,width=cfg.BTN_WIDTH_SMALL,command=self.btn_step_bed_x_up_fnc)
        self.btn_bed_x_up.grid(row=6,column=5,padx=(10,0),pady=(10,0))
        self.btn_bed_x_down = tk.Button(self.lbl_frame_movements,text='v',bg=cfg.moveBeds_color,width=cfg.BTN_WIDTH_SMALL,command=self.btn_step_bed_x_down_fnc)
        self.btn_bed_x_down.grid(row=6,column=6,padx=(0,0),pady=(10,0))
            # Label output "10mm"
        self.strvar_bed_x_step = tk.StringVar()
        self.strvar_bed_x_step.set(str(self.prntr.bed_x_step)+' mm')
        self.lbl_bed_x_step = tk.Label(self.lbl_frame_movements, textvariable=self.strvar_bed_x_step, width=cfg.BTN_WIDTH, bg=cfg.lblFrame_Movements_color)
        self.lbl_bed_x_step.grid(row=6,column=7,padx=(0,0),pady=(10,0), columnspan=2, sticky='W')
            # Apply Button
        tk.Button(self.lbl_frame_movements,text='Apply',command=self.btn_set_bed_x_step,width=cfg.BTN_WIDTH_SMALL).grid(row=7,column=6,padx=(0,0),pady=(0,0)) 
            # Entry
        self.bed_x_step_entry = tk.Entry(self.lbl_frame_movements,width=cfg.BTN_WIDTH)
        self.bed_x_step_entry.grid(row=7,column=7,padx=(0,0), pady=(0,0), columnspan=2, sticky='W')
        self.bed_x_step_entry.bind('<Return>', self.btn_set_bed_x_step )


        # ********************************************************************************************************************************************#
        # Macros                                                                                                                          #
        # ********************************************************************************************************************************************#
            # Mode Secure
        tk.Label(self.lbl_frame_macros,text='Secure Mode: ',bg=cfg.lblFrame_Movements_color).grid(row=0,column=2, pady=(10,0))
        self.strvar_mode_secure = tk.StringVar()
        if (self.prntr.mode_secure):
            self.strvar_mode_secure.set('on')
        else:
            self.strvar_mode_secure.set('off')
        #self.strvar_mode_secure.set(str(self.prntr.mode_secure))
        self.lbl_mode_secure = tk.Label(self.lbl_frame_macros,textvariable=self.strvar_mode_secure,bg=cfg.lblFrame_Movements_color)
        self.lbl_mode_secure.grid(row=0,column=3,padx=(10,0),pady=(10,0))
        self.btn_mode = tk.Button(self.lbl_frame_macros, text = 'Turn off', command=self.btn_switch_on_off, width=cfg.BTN_WIDTH-2)
        self.btn_mode.grid(row=0,column=5,pady=(10,0))
                  
            # Leerzeile
        tk.Label(self.lbl_frame_macros,bg=cfg.lblFrame_Movements_color).grid(row=1,column=1, pady=(10,0))
            
            # Label "Sledge Speed"
        tk.Label(self.lbl_frame_macros,text='Sledge Speed [mm/s]:',bg=cfg.lblFrame_Movements_color).grid(row=2,column=2,padx=(10,0), pady=(10,0))
            # Label output "100mm/s"
        self.strvar_sledge_speed = tk.StringVar()
        self.strvar_sledge_speed.set(str(self.prntr.sledge_speed))
        self.lbl_sledge_speed = tk.Label(self.lbl_frame_macros,textvariable=self.strvar_sledge_speed,bg=cfg.lblFrame_Movements_color)
        self.lbl_sledge_speed.grid(row=2,column=3,padx=(10,0),pady=(10,0))
            # Entry
        self.sledge_speed_entry = tk.Entry(self.lbl_frame_macros,width=cfg.BTN_WIDTH)
        self.sledge_speed_entry.grid(row=2,column=4,pady=(10,0))
        self.sledge_speed_entry.bind('<Return>', self.btn_set_sledge_speed )
            # Apply Button
        tk.Button(self.lbl_frame_macros,text='Apply',command=self.btn_set_sledge_speed,width=cfg.BTN_WIDTH-2).grid(row=2,column=5,pady=(10,0))     
        
            # Label "Bed Speed"
        tk.Label(self.lbl_frame_macros,text='Bed Speed [mm/s]:',bg=cfg.lblFrame_Movements_color).grid(row=3,column=2,padx=(10,0), pady=(10,0))
            # Label output "100mm/s"
        self.strvar_bed_speed = tk.StringVar()
        self.strvar_bed_speed.set(str(self.prntr.bed_speed))
        self.lbl_bed_speed = tk.Label(self.lbl_frame_macros,textvariable=self.strvar_bed_speed,bg=cfg.lblFrame_Movements_color)
        self.lbl_bed_speed.grid(row=3,column=3,padx=(10,0),pady=(10,0))
            # Entry
        self.bed_speed_entry = tk.Entry(self.lbl_frame_macros,width=cfg.BTN_WIDTH)
        self.bed_speed_entry.grid(row=3,column=4,pady=(10,0))
        self.bed_speed_entry.bind('<Return>', self.btn_set_bed_speed )
            # Apply Button
        tk.Button(self.lbl_frame_macros,text='Apply',command=self.btn_set_bed_speed,width=cfg.BTN_WIDTH-2).grid(row=3,column=5,pady=(10,0))
        
            # Leerzeile
        tk.Label(self.lbl_frame_macros,bg=cfg.lblFrame_Movements_color).grid(row=4,column=1, pady=(10,0))
  
            # Button Smooth Powder
        self.btn_smooth = tk.Button(self.lbl_frame_macros,text='Smooth powder',width=cfg.BTN_WIDTH,command=self.btn_smooth_powder_fnc,state=tk.DISABLED)
        self.btn_smooth.grid(row=5,column=1,padx=(10,0),pady=(10,0))
            # Label "layer thickness"
        tk.Label(self.lbl_frame_macros,text='Layer Thickness [mm]:',bg=cfg.lblFrame_Movements_color).grid(row=5,column=2,padx=(10,0), pady=(10,0))
            # Label output "0.002mm"
        self.strvar_LT_smoothing = tk.StringVar()
        self.strvar_LT_smoothing.set(str(self.prntr.layer_thickness_smoothing))
        self.lbl_layer_thickness_smoothing = tk.Label(self.lbl_frame_macros,textvariable=self.strvar_LT_smoothing,bg=cfg.lblFrame_Movements_color)
        self.lbl_layer_thickness_smoothing.grid(row=5,column=3,padx=(10,0),pady=(10,0))
            # Entry
        self.lt_smoothing_entry = tk.Entry(self.lbl_frame_macros,width=cfg.BTN_WIDTH)
        self.lt_smoothing_entry.grid(row=5,column=4,pady=(10,0))
        self.lt_smoothing_entry.bind('<Return>', self.btn_set_layer_thickness_smoothing )
            # Apply Button
        tk.Button(self.lbl_frame_macros,text='Apply',command=self.btn_set_layer_thickness_smoothing, width=cfg.BTN_WIDTH-2).grid(row=5,column=5,pady=(10,0))
        
            # Button Add Layer
        self.btn_addLayer = tk.Button(self.lbl_frame_macros,text='Add layer',width=cfg.BTN_WIDTH,command=self.btn_apply_powder_fnc,state=tk.DISABLED)
        self.btn_addLayer.grid(row=6,column=1,padx=(10,0),pady=(10,0))  
            # Label "layer thickness"
        tk.Label(self.lbl_frame_macros,text='Layer Thickness [mm]:',bg=cfg.lblFrame_Movements_color).grid(row=6,column=2,padx=(10,0), pady=(10,0))
            # Label output "0.002mm"
        self.strvar_LT = tk.StringVar()
        self.strvar_LT.set(str(self.prntr.layer_thickness))
        self.lbl_layer_thickness = tk.Label(self.lbl_frame_macros,textvariable=self.strvar_LT,bg=cfg.lblFrame_Movements_color)
        self.lbl_layer_thickness.grid(row=6,column=3,padx=(10,0),pady=(10,0))
            # Entry
        self.lt_entry = tk.Entry(self.lbl_frame_macros,width=cfg.BTN_WIDTH)
        self.lt_entry.grid(row=6,column=4,pady=(10,0))
        self.lt_entry.bind('<Return>', self.btn_set_layer_thickness )
            # Apply Button
        tk.Button(self.lbl_frame_macros,text='Apply',command=self.btn_set_layer_thickness,width=cfg.BTN_WIDTH-2).grid(row=6,column=5,pady=(10,0))


        # ********************************************************************************************************************************************#
        # Heating                                                                                                                                     #
        # ********************************************************************************************************************************************#
#         self.scale_temp1 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp1.place(x='0',y='0')
#         self.scale_temp2 = tk.Scale(self.lbl_frame_heating, orient='horizontal', bg='sienna1')
#         self.scale_temp2.place(x='140',y='0')
        
        # ********************************************************************************************************************************************#
        # Input                                                                                                                                       #
        # ********************************************************************************************************************************************#
        self.input_entry = tk.Entry(self.lbl_frame_input)
        self.input_entry.pack(side=tk.LEFT,expand='yes',fill='x')
        self.input_entry.focus()
        self.input_entry.bind('<Return>', self.btn_send_fnc)
        tk.Button(self.lbl_frame_input,text='Send',command=self.btn_send_fnc,width=cfg.BTN_WIDTH).pack(side=tk.RIGHT)
                
        # ********************************************************************************************************************************************#
        # Output                                                                                                                                      #
        # ********************************************************************************************************************************************#
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
                
        # ********************************************************************************************************************************************#
        # Start, Pause, Stop Button                                                                                                                   #
        # ********************************************************************************************************************************************#
        # start button:
        self.btn_start = tk.Button(self.master,text='START (proceed external signals)',command=self.btn_start_fnc,bg=cfg.startButton_color,state=tk.DISABLED)
        self.btn_start.pack(fill='both', expand='yes',side=tk.LEFT,padx='10',pady='10')
        # pause button:
        self.btn_pause = tk.Button(self.master,text='PAUSE',command=self.btn_pause_fnc,bg=cfg.pauseButton_color)
        self.btn_pause.pack(fill='both', expand='yes',side=tk.LEFT,padx='10',pady='10')      
        # stop button
        #self.btn_stop = tk.Button(self.master,text='STOP',command=self.btn_stop_fnc,bg=cfg.stopButton_color)
        #self.btn_stop.pack(fill='both', expand='yes',side=tk.RIGHT,padx='10',pady='10')
        
                
# **********************************************************************************************
#                                                                                              *
#                                 Printer properties - functions                               *
#                                                                                              *
# **********************************************************************************************
    def btn_set_layer_thickness(self, event=None):
        strval=str(self.lt_entry.get())
        floatval=float(self.lt_entry.get())
        if (floatval <= cfg.LAYER_THICKNESS_MAX) & (floatval > 0):
            self.prntr.layer_thickness = floatval
            self.update_strvars()
            self.lt_entry.delete(0,'end')
            self.write_gui_output_text('Changed layer thickness to '+strval+'mm',False)
        else:
            self.lt_entry.delete(0,'end')
            self.write_gui_output_text('MAXIMUM '+str(cfg.LAYER_THICKNESS_MAX)+'mm allowed',False)

    def btn_set_layer_thickness_smoothing(self, event=None):
        strval=str(self.lt_smoothing_entry.get())
        floatval=float(self.lt_smoothing_entry.get())
        if (floatval <= cfg.LAYER_THICKNESS_MAX) & (floatval > 0):
            self.prntr.layer_thickness_smoothing = floatval
            self.update_strvars()
            self.lt_smoothing_entry.delete(0,'end')
            self.write_gui_output_text('Changed layer thickness for smoothing to '+strval+'mm',False)
        else:
            self.lt_smoothing_entry.delete(0,'end')
            self.write_gui_output_text('MAXIMUM '+str(cfg.LAYER_THICKNESS_MAX)+'mm allowed',False)
            
    def btn_set_bed_speed(self, event=None):
        strval=str(self.bed_speed_entry.get())
        floatval=float(self.bed_speed_entry.get())
        if (floatval <= cfg.BED_SPEED_MAX) & (floatval >= cfg.BED_SPEED_MIN):
            self.prntr.bed_speed = floatval
            self.update_strvars()
            self.bed_speed_entry.delete(0,'end')
            send(self.prntr.ser,'G100X'+strval+'Y'+strval)
        else:
            self.bed_speed_entry.delete(0,'end')
            self.write_gui_output_text('MINIMUM '+str(cfg.BED_SPEED_MIN)+'mm/s and MAXIMUM '+str(cfg.BED_SPEED_MAX)+'mm/s',False)
            
    def btn_set_sledge_speed(self, event=None):
        strval=str(self.sledge_speed_entry.get())
        floatval=float(self.sledge_speed_entry.get())
        if (floatval <= cfg.SLEDGE_SPEED_MAX) & (floatval >= cfg.SLEDGE_SPEED_MIN):
            self.prntr.sledge_speed = floatval
            self.update_strvars()
            self.sledge_speed_entry.delete(0,'end')
            send(self.prntr.ser,'G100Z'+strval)
        else:
            self.sledge_speed_entry.delete(0,'end')
            self.write_gui_output_text('MINIMUM '+str(cfg.SLEDGE_SPEED_MIN)+'mm/s and MAXIMUM '+str(cfg.SLEDGE_SPEED_MAX)+'mm/s',False)

    def btn_endstops_fnc(self):
        send(self.prntr.ser,GC_Endstops)
        
    def btn_macros_fnc(self):
        self.write_gui_output_text('Macro 0 (Homing all axes):',False)
        temp = GC_Homing(self.prntr)
        self.write_gui_output_text('      '+temp[0:temp.index('\n')],False)
        self.write_gui_output_text('Macro 1 (Homing X axis):',False)
        temp = GC_Home_X(self.prntr)
        self.write_gui_output_text('      '+temp[0:temp.index('\n')],False)
        self.write_gui_output_text('Macro 2 (Homing Y axis):',False)
        temp = GC_Home_Y(self.prntr)
        self.write_gui_output_text('      '+temp[0:temp.index('\n')],False)
        self.write_gui_output_text('Macro 3 (Homing Z axis):',False)
        temp = GC_Home_Z(self.prntr)
        self.write_gui_output_text('      '+temp[0:temp.index('\n')],False)
        self.write_gui_output_text('Macro 4 (Smoothing powder):',False)
        temp = GC_Smooth(self.prntr)
        self.write_gui_output_text('      '+temp[0:temp.index('\n')],False)
        self.write_gui_output_text('Macro 5 (Adding layer):',False)
        temp = GC_Layer(self.prntr)
        self.write_gui_output_text('      '+temp[0:temp.index('\n')],False)
            
            
# **********************************************************************************************
#                                                                                              *
#                                 Movement - functions                                         *
#                                                                                              *
# **********************************************************************************************
    def btn_disable_motors(self):
        send(self.prntr.ser,'M18\n')
    
    def btn_enable_motors(self):
        send(self.prntr.ser,'M17\n')
        
    def scale_sledge_fnc(self,var):        
        self.scale_sledge.configure(bg=cfg.scaleChanged_color)
        self.btn_moveBeds.configure(bg=cfg.scaleChanged_color)                 
        
    def scale_powder_bed_fnc(self,var):
        self.scale_bed1.configure(bg=cfg.scaleChanged_color)
        self.btn_moveBeds.configure(bg=cfg.scaleChanged_color)
        
    def scale_workpiece_bed_fnc(self,var):
        self.scale_bed2.configure(bg=cfg.scaleChanged_color)
        self.btn_moveBeds.configure(bg=cfg.scaleChanged_color)
        
    def btn_homing_fnc(self):
        send(self.prntr.ser,GC_Homing(self.prntr))
    
    def btn_homing_x_fnc(self):
        send(self.prntr.ser,GC_Home_X(self.prntr))
        self.prntr.powder_bed_position = 0
        
    def btn_homing_y_fnc(self):
        send(self.prntr.ser,GC_Home_Y(self.prntr))
        self.prntr.workpiece_bed_position = 0
        
    def btn_homing_z_fnc(self):
        send(self.prntr.ser,GC_Home_Z(self.prntr))
        self.prntr.sledge_position = 0
        
    def btn_move_beds_fnc(self):
        self.write_gui_output_text('Movement command sent',False)
        x = self.scale_bed1.get()
        y = self.scale_bed2.get()
        z = self.scale_sledge.get()
#         send(self.prntr.ser,'G90\n')
        send(self.prntr.ser,GC_Move(x,y,z))
        self.btn_moveBeds.configure(bg=cfg.moveBeds_color)
        self.scale_sledge.configure(bg=cfg.moveBeds_color)
        self.scale_bed1.configure(bg=cfg.moveBeds_color)
        self.scale_bed2.configure(bg=cfg.moveBeds_color)
        
    def btn_undo_fnc(self):
        # set sledge positions back
        self.scale_sledge.set(self.prntr.sledge_position)
        self.scale_bed1.set(self.prntr.powder_bed_position)
        self.scale_bed2.set(self.prntr.workpiece_bed_position)
        # set color back
        self.btn_moveBeds.configure(bg=cfg.moveBeds_color)
        self.scale_sledge.configure(bg=cfg.moveBeds_color)
        self.scale_bed1.configure(bg=cfg.moveBeds_color)
        self.scale_bed2.configure(bg=cfg.moveBeds_color)
        
    def btn_step_sledge_left_fnc(self):
        send(self.prntr.ser,GC_Move_Relativ(0,0,self.prntr.sledge_step))
        # self.write_gui_output_text('step',False)
        
    def btn_step_sledge_right_fnc(self):
        send(self.prntr.ser,GC_Move_Relativ(0,0,-self.prntr.sledge_step))
    
    def btn_step_bed_x_up_fnc(self):
        send(self.prntr.ser,GC_Move_Relativ(self.prntr.bed_x_step,0,0))
        
    def btn_step_bed_x_down_fnc(self):
        send(self.prntr.ser,GC_Move_Relativ(-self.prntr.bed_x_step,0,0))
    
    def btn_step_bed_y_up_fnc(self):
        send(self.prntr.ser,GC_Move_Relativ(0,self.prntr.bed_y_step,0))
        
    def btn_step_bed_y_down_fnc(self):
        send(self.prntr.ser,GC_Move_Relativ(0,-self.prntr.bed_y_step,0))
        
        
    def btn_set_sledge_step(self, event=None):
        strval=str(self.sledge_step_entry.get())
        floatval=float(self.sledge_step_entry.get())
        max_val = float(cfg.SLEDGE_MAX_POS)-float(self.prntr.sledge_position)
        if (floatval <= max_val) & (floatval > 0):
            self.prntr.sledge_step = floatval
            self.update_strvars()
            self.sledge_step_entry.delete(0,'end')
            self.write_gui_output_text('Changed sledge step to '+strval+'mm',False)
        else:
            self.sledge_step_entry.delete(0,'end')
            self.write_gui_output_text('MAXIMUM '+str(max_val)+'mm in this position allowed',False)

    def btn_set_bed_x_step(self, event=None):
        strval=str(self.bed_x_step_entry.get())
        floatval=float(self.bed_x_step_entry.get())
        max_val = float(cfg.BED_MAX_POS)-float(self.prntr.powder_bed_position)
        if (floatval <= max_val) & (floatval > 0):
            self.prntr.bed_x_step = floatval
            self.update_strvars()
            self.bed_x_step_entry.delete(0,'end')
            self.write_gui_output_text('Changed powder bed step to '+strval+'mm',False)
        else:
            self.bed_x_step_entry.delete(0,'end')
            self.write_gui_output_text('MAXIMUM '+str(max_val)+'mm in this position allowed',False)

    def btn_set_bed_y_step(self, event=None):
        strval=str(self.bed_y_step_entry.get())
        floatval=float(self.bed_y_step_entry.get())
        max_val = float(cfg.BED_MAX_POS)-float(self.prntr.workpiece_bed_position)
        if (floatval <= max_val) & (floatval > 0):
            self.prntr.bed_y_step = floatval
            self.update_strvars()
            self.bed_y_step_entry.delete(0,'end')
            self.write_gui_output_text('Changed workpiece bed step to '+strval+'mm',False)
        else:
            self.bed_y_step_entry.delete(0,'end')
            self.write_gui_output_text('MAXIMUM '+str(max_val)+'mm in this position allowed',False)
        
    def btn_smooth_powder_fnc(self):
        send(self.prntr.ser,GC_Smooth(self.prntr))
        
    def btn_apply_powder_fnc(self):
        send(self.prntr.ser,GC_Layer(self.prntr))
        
    def btn_switch_on_off(self):
        if (str(self.prntr.mode_secure)==str(1)):
            send(self.prntr.ser,"M121\n")            
        else:
            send(self.prntr.ser,"M120\n")
            
    def btn_motor_on_off(self):
        if (str(self.prntr.motor_status)==str(1)):
            send(self.prntr.ser,"M17\n")            
        else:
            send(self.prntr.ser,"M18\n")   
                        
                
# **********************************************************************************************
#                                                                                              *
#                                 Input console - functions                                    *
#                                                                                              *
# **********************************************************************************************
    def btn_send_fnc(self, event=None):
        strval=str(self.input_entry.get())
        send(self.prntr.ser,strval+'\n')
        self.input_entry.delete(0,'end')
        
        
# **********************************************************************************************
#                                                                                              *
#                                 Output console - functions                                   *
#                                                                                              *
# **********************************************************************************************
    def write_gui_output_text(self,txt,from_arduino):
        self.output_text.insert(tk.END,txt)
        if from_arduino:
            self.output_text.itemconfig(tk.END,{'fg':cfg.arduino_msg_color})
        self.output_text.yview_moveto(1)
   
# **********************************************************************************************
#                                                                                              *
#                                 Start, pause & stop - functions                              *
#                                                                                              *
# **********************************************************************************************
    def btn_start_fnc(self):
        if self.prntr.ready:
            self.write_gui_output_text('PROCESS CANCELD! IGNORING EXTERNAL SIGNALS ...',False)
            self.prntr.ready = False
            self.btn_start['text'] = 'START (proceed external signals)'
        else:
            self.write_gui_output_text('PROCESS STARTED! WAITING FOR EXTERNAL SIGNAL ...',False)
            self.prntr.ready = True
            self.btn_start['text'] = 'CANCEL (ignore externel signals)'
        
    def btn_pause_fnc(self):
        send(self.prntr.ser,'pause\n')
        if self.process_paused:
            self.process_paused = False
            self.prntr.ready = True
            self.btn_pause['text'] = 'PAUSE'
        else:
            self.process_paused = True
            self.prntr.ready = False
            self.btn_pause['text'] = 'CONTINUE'
        
    #def btn_stop_fnc(self):
        #self.write_gui_output_text('PROCESS STOPPED! RESTART NEEDED...',False)
        #self.prntr.ready = False
        #send(self.prntr.ser,'stop\n')
        
# **********************************************************************************************
#                                                                                              *
#                                 Message boxes - functions                                    *
#                                                                                              *
# **********************************************************************************************
    def showInfoAfterHomed(self):
        messagebox.showinfo('All axes are homed!', 'Now please move the beds to certain positions to fill in the powder. Afterwards click ,Smooth powder´.')
        
#     def showInfoAfterSmoothed(self):
#         result = messagebox.askyesno('Smoothing powder done!', 'Was the smoothing successful?', icon='question')
#         if result == True:
#             self.prntr.smoothed = True
#         else:
#             self.prntr.smoothed = False