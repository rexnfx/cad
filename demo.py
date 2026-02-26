from build123d import *
from ocp_vscode import *
import py_gearworks as pgw

def gear_and_rack():
    gear1 = pgw.HelicalGear(
        number_of_teeth=13,
        helix_angle=pgw.PI / 6,
        height=10,
        profile_shift=0.3,
        herringbone=True,
    )
    gear2 = pgw.HelicalGear(
        number_of_teeth=13,
        helix_angle=pgw.PI / 6,
        height=10,
        profile_shift=0.3,
        herringbone=True,
    )
    rack1 = pgw.HelicalRack(
        number_of_teeth=80,
        helix_angle=pgw.PI / 6,
        height=10,
        herringbone=True,
    )
    rack2 = pgw.HelicalRack(
        number_of_teeth=80,
        helix_angle=pgw.PI / 6,
        height=10,
        herringbone=True,
    )
    # racks can mesh to gears, but gears can't (yet) mesh to racks
    rack1.mesh_to(gear1, target_dir=pgw.RIGHT)
    rack2.mesh_to(gear1, target_dir=pgw.LEFT)
    rack1.mesh_to(gear2, target_dir=pgw.RIGHT )


    gear_part_1 = gear1.build_part()
    rack_part_1 = rack1.build_part()
    rack_part_2 = rack2.build_part()
    gear_part_2 = gear2.build_part()
    gear_part_2 = gear_part_2.moved(Location((0, 137.8, 0)))
    #gear_part_2 = gear2.build_part()
    #rack_part_2 = rack2.build_part()
    return (gear_part_1, rack_part_1, rack_part_2, gear_part_2)#, gear_part_2, rack_part_2)

parts = gear_and_rack()
show(parts)