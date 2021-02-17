import config as cfg

# Variables Makro "Move"
def GC_Move(x,y,z):
    return 'G90\n'\
           'G0'\
           ' X'+str(x)+\
           ' Y'+str(y)+\
           ' Z'+str(z)+'\n'
def GC_setSpeed(bedSpeed = -1,sledgeSpeed = -1):
    if(bedSpeed>0 and sledgeSpeed >0):
        return 'G100'\
               ' X'+str(bedSpeed)+\
               ' Y'+str(bedSpeed)+\
               ' Z'+str(sledgeSpeed)+'\n'
    elif(bedSpeed>0 and sledgeSpeed<0):
        return 'G100'\
               ' X'+str(bedSpeed)+\
               ' Y'+str(bedSpeed)+'\n'
    elif(bedSpeed<0 and sledgeSpeed>0):
        return 'G100'\
               ' Z'+str(sledgeSpeed)+'\n'
    else:
        return ''

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
               '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
               '|G0 Z0'\
               '|G91'+\
               '|'+GC_setSpeed(cfg.BED_SPEED_FAST,-1)+\
               '|G0 X'+str(cfg.LAYER_SMOOTHING_THICKNESS)+' Y'+str(cfg.LAYER_SMOOTHING_THICKNESS)+\
               '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
               '|G0 Z'+str(cfg.SLEDGE_END_POS)+\
               '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
               '|G0 X'+str(-cfg.LAYER_THICKNESS)+' Y'+str(-cfg.LAYER_THICKNESS)+\
               '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
               '|G0 Z'+str(-(cfg.SLEDGE_END_POS-cfg.SLEDGE_MID_POS))+\
               '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
               '|G0 Y'+str(cfg.LAYER_THICKNESS)+'\n'
GC_Macro6 = 'M815 G90'\
               '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
               '|G0 Z0'\
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


