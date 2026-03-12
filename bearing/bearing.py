from build123d import *
from ocp_vscode import *
import math
import copy
from pathlib import Path
import sys

rollers = 6
clearance = 0.1
scale_f = 2

def make_spacer(scale_f, clearance, rollers):
    clearance = clearance *2
    step = 360.0/rollers
    big_circ = Circle(radius = scale_f * 8 - clearance * 4, align=Align.CENTER)
    circ_face = make_face(big_circ)

    mid_circ = Circle(radius= scale_f * 3.9 + clearance * 4, align=Align.CENTER)
    circ_face -= mid_circ

    circ_face_base = copy.copy(circ_face)

    little_circs = [Circle(radius = scale_f * 2 + 4 * clearance, align = Align.CENTER) for c in range(rollers)]
    for c in range(rollers):
        a = math.radians(c * step)
        x = math.cos(a) * (scale_f * 6 - clearance)
        y = math.sin(a) * (scale_f * 6 - clearance)
        little_circs[c] = Pos(x, y) * little_circs[c] 
        circ_face -= little_circs[c]

    spacer = Pos(0, 0, scale_f ) * extrude(circ_face, scale_f * 6)
    spacer_base = extrude(circ_face_base, scale_f )
    return spacer + spacer_base

def make_rollers(scale_f, clearance, rollers):
    step = 360.0/rollers
    little_circs = [Circle(radius = scale_f * 2 + clearance, align = Align.CENTER) for c in range(rollers)]
    for c in range(rollers):
        a = math.radians(c * step)
        x = math.cos(a) * (scale_f * 6 - clearance)
        y = math.sin(a) * (scale_f * 6 - clearance)
        little_circs[c] = Pos(x, y, scale_f  + clearance) * little_circs[c] 
        little_circs[c] = extrude(little_circs[c], (scale_f * 6 - 2 * clearance))
    return little_circs

def make_outter_race(scale_f, clearance):
    big_circ = Pos(0,0,scale_f *-1) * Circle(radius = scale_f * 10, align=Align.CENTER)
    circ_face = make_face(big_circ)

    mid_circ = Pos(0,0,scale_f *-1) *Circle(radius= scale_f * 6, align=Align.CENTER)
    circ_face -= mid_circ

    base =  extrude(circ_face, scale_f * -1)

    ring_face = make_face(big_circ)
    ring_circ = Pos(0,0,scale_f *-1) *Circle(radius= scale_f * 8 , align=Align.CENTER)
    ring_face -= ring_circ
    ring = extrude(ring_face, scale_f * 7)

    race = base + ring

    return race

def make_inner_race(scale_f, clearance):
    big_circ = Pos(0,0,scale_f *-1) * Circle(radius = scale_f * 5.5 - clearance, align=Align.CENTER)
    circ_face = make_face(big_circ)

    mid_circ = Pos(0,0,scale_f *-1) *Circle(radius = scale_f * 2, align=Align.CENTER)
    circ_face -= mid_circ

    base =  extrude(circ_face, scale_f * -1)

    ring_circ = Pos(0,0,scale_f *-1) *Circle(radius=scale_f * 3.95  - clearance, align=Align.CENTER)
    ring_face = make_face(ring_circ)
    ring_face -= mid_circ
    ring = extrude(ring_face, scale_f * 7)

    race = base + ring
    return race

spacer = make_spacer(scale_f, clearance, rollers)
rollers = make_rollers(scale_f, clearance, rollers)
outter_race = make_outter_race(scale_f, clearance)
inner_race = make_inner_race(scale_f, clearance)

show(spacer, rollers, outter_race, inner_race)
# show( outter_race)   

export_stl(spacer, str(Path(sys.argv[0]).parent) + "\\spacer.stl")
export_stl(rollers[0], str(Path(sys.argv[0]).parent) + "\\roller.stl")
export_stl(outter_race, str(Path(sys.argv[0]).parent) + "\\outter_race.stl")
export_stl(inner_race, str(Path(sys.argv[0]).parent) + "\\inner_race.stl")


