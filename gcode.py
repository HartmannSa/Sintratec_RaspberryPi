import config as cfg

# G-Code für Ausgabe des Zustands der Endstops
GC_Endstops = 'M119\n'

# Makro hinter den ^, v , < und > Buttons
# G91: Relative Positionierung
# G0 X.. Y.. Z..: Lineare Bewegung der Achsen um die Werte .. (default 0)
def GC_Move_Relativ(x,y,z):
    return 'G91\n'\
       'G0'\
       ' X'+str(x)+\
       ' Y'+str(y)+\
       ' Z'+str(z)+'\n'

# Makro hinter den Schiebereglern für Rakel und Betten
# G90: Absolute Positionierung
# G0 X.. Y.. Z..: Lineare Bewegung der Achsen um die Werte .. (default aktueller Positionswert)
def GC_Move(x,y,z):
    return 'G90\n'\
           'G0'\
           ' X'+str(x)+\
           ' Y'+str(y)+\
           ' Z'+str(z)+'\n'

# Makro für das Setzen der Geschwindikeiten von Betten und Rakel
# G100 X.. Y.. Z..: X und Y(Betten) werden immer auf die gleiche Geschwindigkeit gesetzt
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
    
# Homing aller Achsen
# M810: Name des Makros und Beginn der Makrodefinition
# M92 X.. Y.. Z.. : Setzt die Schrittweiten
# G28: Homen aller Achsen
# G90: Absolute Positionierung als default Einstellung wählen
# M810: Ende der Makrodefinition
def GC_Homing(printer):
    return 'M810 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28'\
            '|G90\n'\
            'M810\n'

# Homing nur von der X-Achsen
# M811: Name des Makros und Beginn der Makrodefinition
# M92 X.. Y.. Z.. : Setzt die Schrittweiten
# G28 X: Homen der X -Achse
# G90: Absolute Positionierung als default Einstellung wählen
# M811: Ende der Makrodefinition
def GC_Home_X(printer):
    return 'M811 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28 X'\
            '|G90\n'\
            'M811\n'

# Homing nur von der Y-Achse (Analog zur X-Achse)
def GC_Home_Y(printer):
    return 'M812 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28 Y'\
            '|G90\n'\
            'M812\n'

# Homing nur von der Z-Achse (Analog zur X-Achse)
def GC_Home_Z(printer):
    return 'M813 M92 X'+str(printer.step_size_x)+' Y'+str(printer.step_size_y)+' Z'+str(printer.step_size_z)+\
            '|G28 Z'\
            '|G90\n'\
            'M813\n'

# Makro für Pulver glatt streichen
# (Beide Betten fahren nach oben, Rakel fährt von rechts nach links und streicht das Pulver beider Betten glatt)
# M814:             Name des Makros und Beginn der Makrodefinition
# G90:              Absolute Positionierung
# GC_setSpeed(..) = G100 Z..: Setzt die Geschwindigkeit des Rakels hoch
# G0 Z1:            Rakel fährt nach rechts (Startposition)
# G91:              Relative Positionierung
# GC_setSpeed(..) = G100 X..: Setzt die Geschwindigkeit der Betten hoch
# G0 X0.5 Y0.5:     Beide Betten fahren um gewählte Schichtdicke nach oben
# GC_setSpeed(..) = G100 Z..: Setzt die Geschwindigkeit des Rakels auf niedrig für Pulverauftrag
# G0 Z272:          Rakel fährt nach links und glättet Pulver
# GC_setSpeed(..) = G100 X..: Setzt die Geschwindigkeit der Betten runter
# G0 X-0.1 Y-0.1:   Beide Betten fahren um kleine(!) Schichtdicke nach unten
# GC_setSpeed(..) = G100 Z..: Setzt die Geschwindigkeit des Rakels hoch
# G0 Z-272:         Rakel fährt nach rechts (Startposition)
# GC_setSpeed(..) = G100 X..: Setzt die Geschwindigkeit der Betten runter (nicht zwingend nötig)
# G0 X0.1 Y0.1:     Beide Betten fahren um kleine(!) Schichtdicke nach oben
# M814:             Ende der Makrodefinition
def GC_Smooth (printer):
    return 'M814 G90'\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
           '|G0 Z' + str(cfg.SLEDGE_START_POS)+\
           '|G91'+\
           '|'+GC_setSpeed(cfg.BED_SPEED_FAST,-1)+\
           '|G0 X'+str(printer.layer_thickness_smoothing)+' Y'+str(printer.layer_thickness_smoothing)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
           '|G0 Z'+str(cfg.SLEDGE_END_POS - cfg.SLEDGE_START_POS)+\
           '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
           '|G0 X'+str(-printer.layer_thickness)+' Y'+str(-printer.layer_thickness)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
           '|G0 Z'+str(-cfg.SLEDGE_END_POS + cfg.SLEDGE_START_POS)+\
           '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
           '|G0 X'+str(printer.layer_thickness)+' Y'+str(printer.layer_thickness)+'\n'\
           'M814\n'

# Makro für Auftragen einer Schicht
# M815              Name des Makros und Beginn der Makrodefinition
# G90:              Absolute Positionierung wird gewählt
# GC_setSpeed(..) = G100 Z..: Setzt die Geschwindigkeit der Z-Achse (Rakel) auf hoch
# G0 Z1:            Rakel fährt nach rechts (Startposition)
# G91:              relative Positionsangaben werden gewählt
# GC_setSpeed(..) = G100 X..:  Geschwindigkeit der Betten wird auf niedrig eingestellt
# G0 X0.66 Y-0.1:   Bauteilbett(Y) fährt um Schichtdicke nach unten, Pulverbett(X) fährt hoch mit extra Faktor:
#                   -> X fährt min. um 2*Schichtdicke hoch (da von einer Startposition unter der Nulllinie ausgegangen wird)
#                   -> LAYER_OVERHANG gibt an wie viel mehr einer Schichtdicke aufgetragen wird, als eig benötigt, um komplette Bedeckung zu garantieren
#                   -> LAYER_RANGE_EXTEND ist ein Faktor um den das Pulverbett mehr ausgelenkt wird, damit beim Zurückfahren des Rakels kein Pulver nach rechts geschoben wird
# GC_setSpeed(..) = G100 Z..: Geschwindigkeit Rakel (Z) wird auf niedrig gesetzt für Pulverauftrag
# G0 Z272:          Rakel fährt nach links und schiebt dabei Pulver rüber
# G0 X-0.5 Y-0.1:   Bauteilbett(Y) fährt um Schichtdicke nach unten, Pulverbett(X) fährt um Faktor*Schichtdicke nach unten:
#                   -> X fährt min. um eine Schichtdicke nach unten, damit Startposition für nächsten Durchlauf unter der "Nulllinie" liegt
#                   -> LAYER_RANGE_EXTEND noch nach unten, da dies auch in dem nächsten Durchlauf nach oben gefahren wird
# GC_setSpeed(..) = G100 Z..: Geschwindigkeit des Rakels wird hoch gesetzt für Rückweg
# G0 Z-175:         Rakel fährt auf mittlere Halteposition
# G0 Y0.1:          Nur das Bauteilbett fährt wieder nach oben. Das Pulverbett bleibt also unter der "Nulllinie",
#                   sodass das Rakel im nächsten Schichtauftrag drüber fahren kann, ohne Pulver zu verschieben            
# M815:             Ende der Makrodefinition
def GC_Layer (printer):
    return 'M815 G90'\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
           '|G0 Z'+ str(cfg.SLEDGE_START_POS)+\
           '|G91'\
           '|' + GC_setSpeed(cfg.BED_SPEED_SLOW,-1)+\
           '|G0 X'+str((2+cfg.LAYER_RANGE_EXTEND+cfg.LAYER_OVERHANG)*printer.layer_thickness)+' Y'+str(-printer.layer_thickness)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_SLOW)+\
           '|G0 Z'+str(cfg.SLEDGE_END_POS - cfg.SLEDGE_START_POS)+\
           '|G0 X'+str(-(1+cfg.LAYER_RANGE_EXTEND)*(printer.layer_thickness))+' Y'+str(-printer.layer_thickness)+\
           '|' + GC_setSpeed(-1,cfg.SLEDGE_SPEED_FAST)+\
           '|G0 Z'+str(-(cfg.SLEDGE_END_POS-cfg.SLEDGE_MID_POS))+\
           '|G0 Y'+str(printer.layer_thickness)+'\n'\
           'M815\n'



