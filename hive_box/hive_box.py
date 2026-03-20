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

inside_big_hex= Pos(0,big_width) * make_hex(big_width * 3 + 26)
big_hex= Pos(0,big_width) * make_hex(big_width * 3 + 30)
bigger_hex= Pos(0,big_width) * make_hex(big_width * 3 + 40)

def get_squares(h, w):
    squares = [ 
            Pos(big_width - 10,  -10)                * Rectangle(w, h),
            Pos(big_width - 10,  2 * big_width + 10) * Rectangle(w, h),
            Pos(-big_width + 10, -10)                * Rectangle(w, h),
            Pos(-big_width + 10, 2 * big_width + 10) * Rectangle(w, h)
            ]
    return squares

def make_bottom(bigger_hex, big_hex, sections):
    bottom_shape = make_face(bigger_hex.edges())

    squares = get_squares(10, 25)
    for r in range(4):
        bottom_shape -= squares[r]
    bottom = extrude(bottom_shape, 5)

    big_hex = Pos(0,0,5) * big_hex
    big_hex_face = make_face(big_hex.edges())

    for r in range(7):
        section = Pos(0,0,5) * sections[r]
        section_face = make_face(section.edges())
        big_hex_face -= section_face

    squares = get_squares(10, 10)
    for r in range(4):
        sqr = Pos(0,0,5) * squares[r]
        big_hex_face -= sqr

    big_hex_ex = extrude(big_hex_face, 50)

    bottom += big_hex_ex
    return bottom

show(sections, big_hex, inside_big_hex, bigger_hex, make_bottom(bigger_hex, big_hex, sections))

# show( outter_race)   

#export_stl(inner_race, str(Path(sys.argv[0]).parent) + "\\inner_race.stl")


