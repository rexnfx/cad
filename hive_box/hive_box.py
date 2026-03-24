from build123d import *
from ocp_vscode import *
import math
import copy
from pathlib import Path
import sys
import trimesh
import numpy as np

thickness = 12
width = 48
clip_depth = 64.3

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

offsets = [(0, 0), (0, width), (0, width * 2),
        (-0.85 * width, width * 0.5), (-0.85 * width, width * 1.5),
        (0.85 * width, width * 0.5), (0.85 * width, width * 1.5)]

sects = []
for r in range(7):
    sect = make_hex(width)
    sect = Pos(offsets[r][0], offsets[r][1]) * sect
    sects.append(sect)

holes = []
for r in range(7):
    hole = make_hex(width / 1.8)
    hole = Pos(offsets[r][0], offsets[r][1]) * hole
    holes.append(hole)

outside_big_hex= Pos(0,width) * make_hex(width * 3 + 32)
big_hex= Pos(0,width) * make_hex(width * 3 + 30)
bigger_hex= Pos(0,width) * make_hex(width * 3 + 42)

def get_squares(h, w):
    squares = [ 
            Pos(width - 10,  -10)                * Rectangle(w, h),
            Pos(width - 10,  2 * width + 10) * Rectangle(w, h),
            Pos(-width + 10, -10)                * Rectangle(w, h),
            Pos(-width + 10, 2 * width + 10) * Rectangle(w, h)
            ]
    return squares

def make_bottom(bigger_hex, big_hex, sects, holes):
    bottom_shape = make_face(bigger_hex.edges())

    squares = get_squares(10, 22)
    for r in range(4):
        bottom_shape -= squares[r]

    for r in range(7):
        hole_face = make_face(holes[r].edges())
        bottom_shape -= hole_face

    bottom = extrude(bottom_shape, 5)

    big_hex = Pos(0,0,5) * big_hex
    big_hex_face = make_face(big_hex.edges())

    for r in range(7):
        sect = Pos(0,0,5) * sects[r]
        sect_face = make_face(sect.edges())
        big_hex_face -= sect_face

    squares = get_squares(10, 10)
    for r in range(4):
        sqr = Pos(0,0,5) * squares[r]
        big_hex_face -= sqr

    big_hex_ex = extrude(big_hex_face, 50)
    bottom += big_hex_ex
    
    return bottom

def make_top(bigger_hex, big_hex):
    top_shape = make_face(bigger_hex.edges())

    squares = get_squares(10, 10)
    square_holes = get_squares(10, 22)
    for r in range(4):
        top_shape -= squares[r]
        squares[r] = Pos(0,0,4) * squares[r]
        squares[r] = make_face(squares[r].edges())
        squares[r] = extrude(squares[r], 4)
        
    top = extrude(top_shape, 8)

    big_hex = Pos(0,0,8) * big_hex
    bigger_hex = Pos(0,0,8) * bigger_hex
    bigger_hex_face = make_face(bigger_hex.edges())
    bigger_hex_face -= make_face(big_hex.edges())
    
    big_hex_ex = extrude(bigger_hex_face, 50)
    top += big_hex_ex
    for r in range(4):
        square_holes[r] = make_face(square_holes[r].edges())
        squares[r] = extrude(square_holes[r], 4)
        top -= squares[r]
    return top

def make_clip(depth):
    depth -= 9
    line = Line((0,0), (0,depth))
    line += Line((0,depth), (2, depth))
    line += Line((2,depth), (2, depth + 5))
    line += Line((2,depth+5), (-2.5, depth + 5))
    line += Line((-2.5,depth+5), (-2.5, depth/4))
    line += Line((-2.5,depth/4), (-7, depth/4))
    line += Line((-7,depth/4), (-7, depth+5))
    line += Line((-7,depth+5), (-11.5, depth + 5))
    line += Line((-11.5,depth+5), (-11.5, depth))
    line += Line((-11.5,depth), (-9.5, depth))
    line += Line((-9.5,depth), (-9.5, 0))
    line += Line((-9.5,0), (-14.5, 0))
    line += Line((-14.5,0), (-14.5, -4))
    line += Line((-14.5,-4), (5, -4))
    line += Line((5,-4), (5,0))
    line += Line((5,0), (0,0))
    clip_face = make_face(line)
    clip = Pos (0, -190, 0) * extrude(clip_face, 9.5)
    return clip
    
bottom = Pos(190,0,0) * make_bottom(bigger_hex, big_hex, sects, holes)

importer = Mesher()
bee = importer.read(str(Path(sys.argv[0]).parent) + "\\Bee_Insert.stl")[0]
bee = scale(bee, (4,4,3))

# Load mesh
mesh = trimesh.load(str(Path(sys.argv[0]).parent) + "\\Bee_Insert.stl")
# Inflate by moving vertices along normals
offset = 0.22
mesh.vertices += mesh.vertex_normals * offset
# Export inflated mesh
mesh.export(str(Path(sys.argv[0]).parent) + "\\inflatedBee_Insert.stl")
importer2 = Mesher()
bee_cut = importer2.read(str(Path(sys.argv[0]).parent) + "\\inflatedBee_Insert.stl")[0]
bee_cut = Pos(0,190,-6) * scale(bee_cut, (4,4,3))

top = Pos(0,145,0) * make_top(bigger_hex, outside_big_hex)
top -= bee_cut

clip = make_clip(clip_depth)

show(top, bottom, bee, clip)

export_stl(bottom, str(Path(sys.argv[0]).parent) + "\\hive_box_bottom.stl")
export_stl(top, str(Path(sys.argv[0]).parent) + "\\hive_box_top.stl")
export_stl(bee, str(Path(sys.argv[0]).parent) + "\\bee.stl")
export_stl(clip, str(Path(sys.argv[0]).parent) + "\\clip.stl")


# show( outter_race)   

#export_stl(inner_race, str(Path(sys.argv[0]).parent) + "\\inner_race.stl")


