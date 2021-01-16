import config as cfg

# Macros
GC_Macro1 = 'M810 M92 X'+str(cfg.STEP_SIZE_X)+' Y'+str(cfg.STEP_SIZE_Y)+' Z'+str(cfg.STEP_SIZE_Z)+\
               '|G28'\
               '|G90\n'
GC_Macro2 = 'M811 M92 X'+str(cfg.STEP_SIZE_X)+' Y'+str(cfg.STEP_SIZE_Y)+' Z'+str(cfg.STEP_SIZE_Z)+\
               '|G28 X'\
               '|G90\n'
GC_Macro3 = 'M812 M92 X'+str(cfg.STEP_SIZE_X)+' Y'+str(cfg.STEP_SIZE_Y)+' Z'+str(cfg.STEP_SIZE_Z)+\
               '|G28 Y'\
               '|G90\n'
GC_Macro4 = 'M813 M92 X'+str(cfg.STEP_SIZE_X)+' Y'+str(cfg.STEP_SIZE_Y)+' Z'+str(cfg.STEP_SIZE_Z)+\
               '|G28 Z'\
               '|G90\n'
GC_Macro5 = 'M814 G90'\
               '|G0 Z0 F'+str(cfg.SLEDGE_SPEED_SLOW)+\
               '|G91'\
               '|G0 X'+str(cfg.LAYER_SMOOTHING_THICKNESS)+' Y'+str(cfg.LAYER_SMOOTHING_THICKNESS)+' F'+str(cfg.BED_SPEED_FAST)+\
               '|G0 Z'+str(cfg.SLEDGE_END_POS)+' F'+str(cfg.SLEDGE_SPEED_SLOW)+\
               '|G0 X'+str(-cfg.LAYER_THICKNESS)+' Y'+str(-cfg.LAYER_THICKNESS)+' F'+str(cfg.BED_SPEED_SLOW)+\
               '|G0 Z'+str(-(cfg.SLEDGE_END_POS-cfg.SLEDGE_MID_POS))+' F'+str(cfg.SLEDGE_SPEED_FAST)+\
               '|G0 Y'+str(cfg.LAYER_THICKNESS)+' F'+str(cfg.BED_SPEED_SLOW)+'\n'
GC_Macro6 = 'M815 G90'\
               '|G0 Z0 F'+str(cfg.SLEDGE_SPEED_FAST)+\
               '|G91'\
               '|G0 X'+str(2*cfg.LAYER_THICKNESS)+' Y'+str(-cfg.LAYER_THICKNESS)+' F'+str(cfg.BED_SPEED_SLOW)+\
               '|G0 Z'+str(cfg.SLEDGE_END_POS)+' F'+str(cfg.SLEDGE_SPEED_SLOW)+\
               '|G0 X'+str(-cfg.LAYER_THICKNESS)+' Y'+str(-cfg.LAYER_THICKNESS)+' F'+str(cfg.BED_SPEED_SLOW)+\
               '|G0 Z'+str(-(cfg.SLEDGE_END_POS-cfg.SLEDGE_MID_POS))+' F'+str(cfg.SLEDGE_SPEED_FAST)+\
               '|G0 Y'+str(cfg.LAYER_THICKNESS)+' F'+str(cfg.BED_SPEED_SLOW)+'\n' 

# Executable G-Code
GC_Endstops = 'M119\n'
GC_Homing = 'M810\n'
GC_Home_X = 'M811\n'
GC_Home_Y = 'M812\n'
GC_Home_Z = 'M813\n'
GC_Smooth = 'M814\n'
GC_Layer  = 'M815\n'

