from build123d import *
from ocp_vscode import *

e_ch_l = 10.7 #end chamfer length
efl = 1.4 #end flat length
ecc = efl + e_ch_l #end chamfer combined
fgl = 5 #front groove length
ecl = e_ch_l + fgl # end combined length
ew = 18.4 #end width
rw = 26.5
rl = 45.8

rect = Rectangle(width = ecl + rl + 4.5 + 1.4 + 12.5 + 8,
                 height = rw + 8,
                 align =(Align.MIN, Align.MIN)
                 )
rect = rect.move(Location((-4, -4, 0)))

line = Polyline([
    (0,rw/2),
    (0, (rw - ew) / 2 ), 
    (10.7, (rw - 21.7) / 2), 
    (ecc, (rw - 21.7) / 2), 
    (ecc, (rw - 19.5) / 2),
    (ecc + 2.6, (rw - 19.5) / 2),
    (ecc + 2.6, (rw - 20.9) / 2),
    (e_ch_l + fgl, (rw - 20.9) / 2),
    (ecl, 0), 
    (ecl + rl, 0),
    (ecl + rl, (rw - 19.5) / 2),
    (ecl + rl + 4.5, (rw - 19.5) / 2),
    (ecl + rl + 4.5, (rw - 21.7) / 2),
    (ecl + rl + 4.5 + 1.4, (rw - 21.7)/2),
    (ecl + rl + 4.5 + 1.4 + 12.5, (rw - ew) / 2),
    (ecl + rl + 4.5 + 1.4 + 12.5, rw / 2)
    ], close = False)

line_mir = mirror(line, Plane.XZ.offset(-rw /2))
line += line_mir

profile = make_face(line.edges())
sketch = rect - profile
box = extrude(sketch, amount =20)

#box = box
export_stl(box, "C:\\Code\\Python\\cad\\elite_magwell.stl")

show(box)
#show(line, rect)