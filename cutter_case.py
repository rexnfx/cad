from build123d import *
from ocp_vscode import *
import sys
from pathlib import Path

cutter_case_edges = Line((-10,0), (10,0)) 

#export_stl(left_logo_edges, str(Path(sys.argv[0]).parent) + "\\elite_magwell.stl")

show(cutter_case_edges )