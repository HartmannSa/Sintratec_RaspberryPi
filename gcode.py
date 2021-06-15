import config as cfg


GC_Endstops = 'M119\n'

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
               ' Z'+str(sledgeSpeed)
    elif(bedSpeed>0 and sledgeSpeed<0):
        return 'G100'\
               ' X'+str(bedSpeed)+\
               ' Y'+str(bedSpeed)
    elif(bedSpeed<0 and sledgeSpeed>0):
        return 'G100'\
               ' Z'+str(sledgeSpeed)
    else:
        return ''

def GC_Homing(printer):
    return 'M810 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28'\
            '|G90\n'\
            'M810\n'

def GC_Home_X(printer):
    return 'M811 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28 X'\
            '|G90\n'\
            'M811\n'

def GC_Home_Y(printer):
    return 'M812 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28 Y'\
            '|G90\n'\
            'M812\n'

def GC_Home_Z(printer):
    return 'M813 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28 Z'\
            '|G90\n'\
            'M813\n'

def GC_Smooth (printer):
    return 'M814 G90'\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
           '|G0 Z0'\
           '|G91'+\
           '|'+GC_setSpeed(cfg.BED_SPEED_FAST,-1)+\
           '|G0 X'+str(cfg.LAYER_SMOOTHING_THICKNESS)+' Y'+str(cfg.LAYER_SMOOTHING_THICKNESS)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
           '|G0 Z'+str(cfg.SLEDGE_END_POS)+\
           '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
           '|G0 X'+str(-printer.layer_thickness)+' Y'+str(-printer.layer_thickness)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
           '|G0 Z'+str(-(cfg.SLEDGE_END_POS-cfg.SLEDGE_MID_POS))+\
           '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
           '|G0 Y'+str(printer.layer_thickness)+'\n'\
           'M814\n'

def GC_Layer (printer):
    return 'M815 G90'\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
           '|G0 Z0'\
           '|G91'\
           '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
           '|G0 X'+str(2*printer.layer_thickness)+' Y'+str(-printer.layer_thickness)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
           '|G0 Z'+str(cfg.SLEDGE_END_POS)+\
           '|G0 X'+str(-printer.layer_thickness)+' Y'+str(-printer.layer_thickness)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
           '|G0 Z'+str(-(cfg.SLEDGE_END_POS-cfg.SLEDGE_MID_POS))+\
           '|G0 Y'+str(printer.layer_thickness)+'\n'\
           'M815\n'


