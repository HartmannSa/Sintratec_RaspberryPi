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
LAYER_THICKNESS = 0.05       # [mm]
LAYER_THICKNESS_MAX = 1     # [mm]
LAYER_SMOOTHING_THICKNESS = 5 # [mm]
# POWDER_FILL_HEIGHT = 100      # [mm]

# Communication
# VERBOSE = True
BAUDRATE = 250000

# GUI
BTN_WIDTH = 10 # Button width used for every button except start, pause and stop
FRAME_HEIGHT = 200
GUI_WIDTH = 760
GUI_HEIGHT = 1000

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