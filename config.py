# ********************************************************
# IMPORTANT: Powder bed = X, workpiece bed = Y, sledge = Z
# 
# ********************************************************

# Movements
# POWDER_BED_MAX_HEIGHT = 125  # [mm]
SLEDGE_END_POS = 280         # [mm]
SLEDGE_MID_POS = 118         # [mm]
STEP_SIZE_X = 1600           # [mm/s]
STEP_SIZE_Y = 1600           # [mm/s]
STEP_SIZE_Z = 32             # [mm/s]
BED_SPEED_SLOW = 3           # [mm/s]
BED_SPEED_FAST = 10          # [mm/s]
SLEDGE_SPEED_SLOW  = 100     # [mm/s]
SLEDGE_SPEED_FAST  = 120     # [mm/s] 

# Printer properties
LAYER_THICKNESS = 1       # [mm] default 0.05
LAYER_THICKNESS_MAX = 10     # [mm]
LAYER_SMOOTHING_THICKNESS = 5 # [mm]
# POWDER_FILL_HEIGHT = 100      # [mm]

# Communication
# VERBOSE = True
BAUDRATE = 250000

# GUI
BTN_WIDTH = 10 # default Button width
BTN_WIDTH_SMALL = 5 # default Button width
FRAME_HEIGHT = 200
GUI_WIDTH = 1275
GUI_HEIGHT = 990
GUI_POS_X = 1 # Position der Gui von linkerer unterer Bildschirmecke aus
GUI_POS_Y = 1 # Position der Gui von linkerer unterer Bildschirmecke aus

# GUI colors
lblFrame_PrinterProperties_color = 'gray'
lblFrame_Movements_color = 'gray70'
lblFrame_Heating_color = 'coral1'
lblFrame_Input_color = 'white'
lblFrame_Output_color = 'white'
moveBeds_color = 'antique white'
startButton_color = 'DarkOliveGreen1'
pauseButton_color = 'yellow2'
stopButton_color = 'red'
scaleChanged_color = 'red2'
arduino_msg_color = 'light sea green'

# Laser controller communication
# duration for how long a voltage of 3.3V is sent to the laser controller,
# as soon as the layer was added:
time_output_signal = 0.5 #sec
pin_laser_input = 23 # ein Kabel in Pin-No. 16, das andere in Pin-No. 14
pin_laser_output = 17 # ein Kabel in Pin-No. 11, das andere in Pin-No. 9
