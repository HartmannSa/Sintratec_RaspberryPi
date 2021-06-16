import config as cfg

class Printer:
    def __init__(self,NAME,ser):
        self.name = NAME
        self.ser = ser
        self.homed = False # default False
        self.x_homed = False # default False
        self.y_homed = False # default False
        self.z_homed = False # default False
        self.smoothed = False # default False
        self.layer_thickness = cfg.LAYER_THICKNESS
        self.step_size_x = cfg.STEP_SIZE_X
        self.step_size_y = cfg.STEP_SIZE_Y
        self.step_size_z = cfg.STEP_SIZE_Z
        self.bed_speed = cfg.BED_SPEED_SLOW
        self.sledge_speed = cfg.SLEDGE_SPEED_SLOW
        self.sledge_step = cfg.SLEDGE_STEP
        self.bed_x_step = cfg.BED_X_STEP
        self.bed_y_step = cfg.BED_Y_STEP
        self.powder_bed_position = 10 #X nur für Initialisierung der Anzeige. Dies wird von den "wahren" Werten vom Arduino überschrieben
        self.workpiece_bed_position = 110 #Y nur für Initialisierung der Anzeige. Dies wird von den "wahren" Werten vom Arduino überschrieben
        self.sledge_position = 0 #Z nur für Initialisierung der Anzeige. Dies wird von den "wahren" Werten vom Arduino überschrieben
        self.ready = False # default FALSE
        self.ready_to_send_signal_back = False