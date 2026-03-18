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

    sides = None
    fx = 0
    fy = big_width/2.0
    px = math.nan
    py = math.nan
    
    for c in range(1,7):
        a = math.radians(c * step)
        x = math.cos(a) * (big_width/2.0)
        y = math.sin(a) * (big_width/2.0)
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

sections = []
for r in range(7):
    section = make_section(big_width, thickness)
    sections.append(section)

section = sections[0]
section = Pos(0, big_width) * section

show(section, sections[1])
# show( outter_race)   

#export_stl(inner_race, str(Path(sys.argv[0]).parent) + "\\inner_race.stl")


