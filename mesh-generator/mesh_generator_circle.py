import gmsh
import sys
from math import pi, cos, sin


gmsh.initialize()

gmsh.model.add("try_1")

r = 5
m_size = 0.25
number_points = 20

spacing_angle = (2*pi) / number_points

mesh = gmsh.model.geo

mesh.addPoint(0, 0, 0, m_size, 1)

theta = 0
for i in range(number_points):
    
    x = r*cos(theta)
    y = r*sin(theta)
    theta += spacing_angle

    mesh.addPoint(x, y, 0, m_size, i+2)


for i in range(number_points):
    if i==(number_points-1):
        mesh.addCircleArc(i+2, 1, 2, i+1)
        break
    mesh.addCircleArc(i+2, 1, i+3, i+1)

list_pt = []
for i in range(number_points):
    list_pt.append(i+1)


mesh.addCurveLoop(list_pt, 1)

mesh.addPlaneSurface([1], 2)






mesh.extrude([(2, 2)], 0, 0, 0.25)

#gmsh.option.setNumber("Mesh.Algorithm", 1)
#gmsh.option.setNumber("Mesh.RecombineAll", 1)

mesh.synchronize()

gmsh.model.mesh.generate(3)
#gmsh.write("circular_mince.mesh")


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()