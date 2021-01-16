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
        self.sledge_position = 10
        self.powder_bed_position = 0
        self.workpiece_bed_position = 0
        self.ready = False