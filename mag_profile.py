from build123d import *
from ocp_vscode import *

rect = Rectangle(width = 17.1 + 58.8 + 4.5 + 1.4 + 12.5 + 8,
                 height=26.5 + 8,
                 align=(Align.MIN, Align.MIN)
                 )
rect = rect.move(Location((-4, -4, 0)))

line = Polyline([
    (0,26.5/2),
    (0, (26.5-18.4)/2 ), 
    (10.7,(26.5-21.7)/2), 
    (12.1,(26.5-21.7)/2), 
    (12.1,(26.5-19.5)/2),
    (12.1+2.6,(26.5-19.5)/2),
    (12.1+2.6,(26.5-20.9)/2),
    (12.1+5,(26.5-20.9)/2),
    (17.1, 0), 
    (17.1 + 58.8, 0),
    (17.1 + 58.8, (26.5-19.5)/2),
    (17.1 + 58.8 + 4.5,(26.5-19.5)/2),
    (17.1 + 58.8 + 4.5,(26.5-21.7)/2),
    (17.1 + 58.8 + 4.5 + 1.4,(26.5-21.7)/2),
    (17.1 + 58.8 + 4.5 + 1.4 + 12.5,(26.5-18.4)/2),
    (17.1 + 58.8 + 4.5 + 1.4 + 12.5, 26.5/2)
    ], close=False)
line2 = mirror(line, Plane.XZ.offset(-26.5/2))
line += line2

profile = make_face(line.edges())
sketch = rect - profile
box = extrude(sketch, amount =20)

#box = box
export_stl(box, "C:\\Code\\Python\\cad\\elite_magwell.stl")

show(box)
#show(line, rect)