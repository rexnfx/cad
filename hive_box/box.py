from build123d import *
from ocp_vscode import *
import math
import copy
from pathlib import Path
import sys

thickness = 12
width = 43
big_width = 48


def make_section(big_width, thickness):
    step = 360.0/6.0
    big_circ = Circle(radius = scale_f * 8 - clearance * 4, align=Align.CENTER)
    circ_face = make_face(big_circ)

    mid_circ = Circle(radius= scale_f * 3.9 + clearance * 4, align=Align.CENTER)
    circ_face -= mid_circ

    circ_face_base = copy.copy(circ_face)

    sides = None
    fx = 0
    fy = big_width/2.0
    px = math.nan
    py = math.nan
    
    for c in range(1,7):
        a = math.radians(c * step)
        x = math.cos(a) * (big_width/2.0)
        y = math.sin(a) * (big_width/2.0)
        if px is math.nan:
            sides = Line((fx, py), (x, y))
        else:
            sides += Line((px, py), (x, y))

    return sides



section = make_section(big_width, thickness)


show(section)
# show( outter_race)   

#export_stl(inner_race, str(Path(sys.argv[0]).parent) + "\\inner_race.stl")


