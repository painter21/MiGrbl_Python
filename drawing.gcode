G00 S1; endstops
G00 E0; no extrusion
G01 S1; endstops
G01 E0; no extrusion
G21; millimeters
G91 G0 F300.0 Z20.000; pen park !!Zsafe
G90; absolute
G28 X; home
G28 Y; home
G28 Z; home
G00 F300.0 Z35.000; pen park !!Zpark
G00 F2400.0 Y0.000; !!Ybottom
G00 F2400.0 X0.000; !!Xleft
G00 F2400.0 X57.157 Y233.693; move !!Xleft+57.157 Ybottom+233.693
G00 F300.0 Z15.000; pen down !!Zwork
G01 F2100.0 X103.100 Y233.693; draw !!Xleft+103.100 Ybottom+233.693
G01 F2100.0 X103.100 Y176.898; draw !!Xleft+103.100 Ybottom+176.898
G01 F2100.0 X57.157 Y176.898; draw !!Xleft+57.157 Ybottom+176.898
G01 F2100.0 X57.157 Y233.693; draw !!Xleft+57.157 Ybottom+233.693
G01 F2100.0 X58.157 Y233.693; draw !!Xleft+58.157 Ybottom+233.693
G00 F300.0 Z35.000; pen park !!Zpark
