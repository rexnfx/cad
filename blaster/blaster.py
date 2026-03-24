from build123d import *
from ocp_vscode import *
import math
import copy
from pathlib import Path
import sys
from mag_profile import *

def make_rear():
    line = Line((0,0), (150, 0))
    line += Line((150,0), (150, 70))
    line += Line((150, 70), (0, 70))
    line += Line((0, 70), (0, 0))
    rear = make_face(line) 
    rear = Pos(70, 0) * extrude(rear, 4)  
    return rear

def make_receiver():
    line = Line((0,0), (70, 0))
    line += Line((70,0), (150, 70))
    line += Line((150, 70), (0, 70))
    line += Line((0, 70), (0, 0))
    receiver = make_face(line) 
    receiver = Pos(70, 0) * extrude(receiver, 4)    
    return receiver



rear = make_rear()
receiver = make_receiver()

show(rear, receiver)
