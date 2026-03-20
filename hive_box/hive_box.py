from build123d import *
from ocp_vscode import *
import math
import copy
from pathlib import Path
import sys

thickness = 12
width = 43
big_width = 48


def make_hex(w):
    step = 360.0/6.0

    sides = None
    fx = 0
    fy = w/2.0
    px = math.nan
    py = math.nan
    
    for c in range(1,7):
        a = math.radians(c * step)
        x = math.cos(a) * (w/2.0)
        y = math.sin(a) * (w/2.0)
        line = None
        if px is math.nan:
            fx = x
            fy = y
        else:
            line= Line((px, py), (x, y))
        if sides is None:
            sides = line
        else:            
            sides += line  
        px = x
        py = y
    sides += Line((px, py), (fx, fy))
    return sides

offsets = [(0, 0), (0, big_width), (0, big_width * 2),
        (-0.85 * big_width, big_width * 0.5), (-0.85 * big_width, big_width * 1.5),
        (0.85 * big_width, big_width * 0.5), (0.85 * big_width, big_width * 1.5)]

sections = []
for r in range(7):
    section = make_hex(big_width)
    section = Pos(offsets[r][0], offsets[r][1]) * section
    sections.append(section)

big_hex= Pos(0,big_width) * make_hex(big_width * 3 + 30)
bigger_hex= Pos(0,big_width) * make_hex(big_width * 3 + 40)

squares = [ 
        Pos(big_width - 10,  -10)                * Rectangle(10, 10),
        Pos(big_width - 10,  2 * big_width + 10) * Rectangle(10, 10),
        Pos(-big_width + 10, -10)                * Rectangle(10, 10),
        Pos(-big_width + 10, 2 * big_width + 10) * Rectangle(10, 10)
        ]

show(sections, big_hex, bigger_hex, squares)

# show( outter_race)   

#export_stl(inner_race, str(Path(sys.argv[0]).parent) + "\\inner_race.stl")


