from build123d import *
from ocp_vscode import *
import sys
from pathlib import Path

e_ch_l = 11.8 #end chamfer length
efl = 1.4 #end flat length
ecc = efl + e_ch_l #end chamfer combined
fgl = 5 #front groove length
fgw = 20.9 #front groove width
ecl = ecc + fgl # end combined length
eww = 21.9 #end wide width
ew = 18.9 #end width
gw = 19.8
gl = 4.5 #groove length
rw = 26.7 #retainer width
rl = 45.8 #retainer length
ovr_len = ecl + rl + gl + ecc


def make_profile( edges = []):
    rect = RectangleRounded(ovr_len + 6,
                        height = rw + 6,
                        radius=2,
                        align =(Align.MIN, Align.MIN)
                        )
    rect = rect.move(Location((-3, -3, 0)))

    line = Polyline([
        (0,rw/2),
        (0, (rw - ew) / 2 ), 
        (e_ch_l, (rw - eww) / 2), 
        (ecc, (rw - eww) / 2), 
        (ecc, (rw - gw) / 2),
        (ecc + 2.6, (rw - gw) / 2),
        (ecc + 2.6, (rw - fgw) / 2),
        (ecc+ fgl , (rw - fgw) / 2),
        (ecl, 0), 
        (ecl + rl, 0),
        (ecl + rl, (rw - gw) / 2),
        (ecl + rl + gl, (rw - gw) / 2),
        (ecl + rl + gl, (rw - eww) / 2),
        (ecl + rl + gl + 1.4, (rw - eww)/2),
        (ecl + rl + gl + ecc, (rw - ew) / 2),
        (ecl + rl + gl + ecc, rw / 2)
        ], close = False)

    line_mir = mirror(line, Plane.XZ.offset(-rw /2))
    line += line_mir
    edges.append(line)
    edges.append(rect.edges())

    profile = make_face(line.edges())
    sketch = rect - profile
    box = extrude(sketch, amount =10)
    return box

edges = []
box= make_profile(edges=edges)

drafting_options = Draft(font_size=3.5, decimal_precision=1, display_units=False)
d3 = ExtensionLine(
    border=edges[0].sort_by(Axis.Y)[-1], offset=-5 * MM, draft=drafting_options
)

export_stl(box, str(Path(sys.argv[0]).parent) + "\\elite_magwell.stl")

show(edges)
#show(line, rect)