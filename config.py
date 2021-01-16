# ********************************************************
# IMPORTANT: Powder bed = X, workpiece bed = Y, sledge = Z
# 
# ********************************************************

# Movements
POWDER_BED_MAX_HEIGHT = 125  # [mm]
SLEDGE_END_POS = 280         # [mm]
SLEDGE_MID_POS = 118         # [mm]
STEP_SIZE_X = 32             # [mm/s]
STEP_SIZE_Y = 32             # [mm/s]
STEP_SIZE_Z = 32             # [mm/s]
BED_SPEED_SLOW = 30          # [mm/s]
BED_SPEED_FAST = 200         # [mm/s]
SLEDGE_SPEED_SLOW  = 200     # [mm/s]
SLEDGE_SPEED_FAST  = 500     # [mm/s] 

# Printer properties
LAYER_THICKNESS = 0.002       # [mm]
LAYER_THICKNESS_MAX = 0.1     # [mm]
LAYER_SMOOTHING_THICKNESS = 5 # [mm]
# POWDER_FILL_HEIGHT = 100      # [mm]

# Communication
VERBOSE = True
BAUDRATE = 250000

# GUI
BTN_WIDTH = 10 # Button width used for every button except start, pause and stop
FRAME_HEIGHT = 200
GUI_WIDTH = 750
GUI_HEIGHT = 1000

