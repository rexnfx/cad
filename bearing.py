from build123d import *
from ocp_vscode import *
import math
import copy

rollers = 6
clearance = 0.1
scale_f = 2

def make_spacer(scale_f, clearance, rollers):
    step = 360.0/rollers
    big_circ = Circle(radius = scale_f * 8 - clearance * 2, align=Align.CENTER)
    circ_face = make_face(big_circ)

    mid_circ = Circle(radius= scale_f * 4 + clearance * 2, align=Align.CENTER)
    circ_face -= mid_circ

    circ_face_base = copy.copy(circ_face)

    little_circs = [Circle(radius = scale_f * 2 + 2 * clearance, align = Align.CENTER) for c in range(rollers)]
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
    big_circ = Circle(radius = scale_f * 10, align=Align.CENTER)
    circ_face = make_face(big_circ)

    mid_circ = Circle(radius= scale_f * 6, align=Align.CENTER)
    circ_face -= mid_circ

    base = Pos(0, 0, scale_f ) * extrude(circ_face, scale_f * 2)

    ring_face = make_face(big_circ)
    ring_circ = Circle(radius= scale_f * 8 + clearance, align=Align.CENTER)
    ring_face -= ring_circ
    ring = extrude(ring_face, scale_f * 7)

    race = base + ring

    return race

def make_inner_race(scale_f, clearance):
    big_circ = Circle(radius = scale_f * 5.5 - clearance, align=Align.CENTER)
    circ_face = make_face(big_circ)

    mid_circ = Circle(radius = scale_f * 2, align=Align.CENTER)
    circ_face -= mid_circ

    base = Pos(0, 0, scale_f ) * extrude(circ_face, scale_f * 2)

    ring_circ = Circle(radius=scale_f * 4  - clearance, align=Align.CENTER)
    ring_face = make_face(ring_circ)
    ring_face -= mid_circ
    ring = extrude(ring_face, scale_f * 7)

    race = base + ring
    return race

show(
    make_spacer(scale_f, clearance, rollers), 
    make_rollers(scale_f, clearance, rollers), 
    make_outter_race(scale_f, clearance), 
    make_inner_race(scale_f, clearance))
#show(make_inner_race())
