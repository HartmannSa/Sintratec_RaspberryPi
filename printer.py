import config as cfg

class Printer:
    def __init__(self,NAME,ser):
        self.name = NAME
        self.ser = ser
        self.homed = True
        self.x_homed = False
        self.y_homed = False
        self.z_homed = False
        self.smoothed = True
        self.layer_thickness = cfg.LAYER_THICKNESS
        self.step_size_x = cfg.STEP_SIZE_X
        self.step_size_y = cfg.STEP_SIZE_Y
        self.step_size_y = cfg.STEP_SIZE_Z
        self.bed_speed = cfg.BED_SPEED_SLOW
        self.sledge_speed = cfg.SLEDGE_SPEED_SLOW
        self.powder_bed_position = 0 #X
        self.workpiece_bed_position = 0 #Y
        self.sledge_position = 0 #Z
        self.ready = False