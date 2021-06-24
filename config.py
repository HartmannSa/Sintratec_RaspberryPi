# ********************************************************
# IMPORTANT: Powder bed = X, workpiece bed = Y, sledge = Z
# 
# ********************************************************

# Movements
BED_MAX_POS = 140.0           # [mm]
SLEDGE_MAX_POS = 274.0        # [mm]
SLEDGE_END_POS = 273.0        # [mm] Hit Endstop at 274.5
SLEDGE_MID_POS = 98.0         # [mm] 
SLEDGE_START_POS = 1.0        # [mm] Hit Endstop at 0
STEP_SIZE_X = 1612.5          # [mm/s]
STEP_SIZE_Y = 1612.5          # [mm/s]
STEP_SIZE_Z = 33              # [mm/s]

BED_SPEED_MAX = 40            # [mm/s]
BED_SPEED_MIN = 0.5           # [mm/s]
BED_SPEED_SLOW = 2            # [mm/s]
BED_SPEED_FAST = 8            # [mm/s]
SLEDGE_SPEED_MAX   = 250      # [mm/s]
SLEDGE_SPEED_MIN   = 1        # [mm/s]
SLEDGE_SPEED_SLOW  = 70       # [mm/s]
SLEDGE_SPEED_FAST  = 170      # [mm/s]

HOMING_SPEED_BED = 5          # [mm/s]
HOMING_SPEED_SLEDGE = 20      # [mm/s]

SLEDGE_STEP = 10.0            # [mm]
BED_X_STEP = 5.0              # [mm]
BED_Y_STEP = 5.0              # [mm]

LAYER_THICKNESS = 0.1         # [mm] default 0.05
LAYER_THICKNESS_MAX = 10      # [mm]
LAYER_SMOOTHING_THICKNESS = 5 # [mm]
# Die folgenden beiden Faktoren werden nur im Makro "Apply Powder" für das Pulverbett genutzt
LAYER_RANGE_EXTEND = 4 # Bett wird um diese Anzahl MEHR als nur eine Schichtdicke hoch&runter gefahren. Vermeidet, dass das Rakel beim zurückfahren ungewollt Pulver nach rechts streicht
LAYER_OVERHANG = 0.05   # Es wird (Factor*Schichtdicke) MEHR Pulver aufgetragen, um zu garantieren, dass keine Lücken in der Pulverschicht im Bauteilbett entstehen

MODE_SECURE = True
MOTOR_STATUS = False

# Communication
BAUDRATE = 250000

# Laser controller communication
time_output_signal = 0.5 #sec, # duration for how long a voltage of 3.3V is sent to the laser controller,
pin_laser_input = 12 # 
pin_laser_output = 13 #
pin_error_output = 19 # 

# GUI
BTN_WIDTH = 10 # default Button width
BTN_WIDTH_SMALL = 5 # default Button width
FRAME_HEIGHT = 200
GUI_WIDTH = 1275
GUI_HEIGHT = 990
GUI_POS_X = 1 # Position der Gui von linkerer unterer Bildschirmecke aus
GUI_POS_Y = 1 # Position der Gui von linkerer unterer Bildschirmecke aus
pad_x = 10
pad_y = 10

# GUI colors
lblFrame_First_color = 'gray'
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


