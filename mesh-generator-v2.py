import gmsh
import sys
from math import tan, pi


h = 0.635
L = 10
theta = 45

theta = theta/180*pi
l = L/2
p = l - h/tan(theta)

m_size = 20e-02

gmsh.initialize()

gmsh.model.add("try_1")

mesh = gmsh.model.geo


mesh.addPoint(0, 0, 0, m_size, 1)
mesh.addPoint(0, 0, h, m_size, 2)
mesh.addPoint(p, 0, h, m_size, 3)
mesh.addPoint(l, 0, 0, m_size, 4)

#mesh.addPoint(-p, 0, h, m_size, 5)
#mesh.addPoint(-l, 0, 0, m_size, 6)

mesh.addLine(1, 2, 1)
mesh.addLine(2, 3, 2)
mesh.addLine(3, 4, 3)
mesh.addLine(4, 1, 4)


#mesh.addLine(2, 5, 5)
#mesh.addLine(5, 6, 6)
#mesh.addLine(6, 1, 7)

mesh.addCurveLoop([1,2,3,4],1)
#mesh.addCurveLoop([1,5,6,7],2)

mesh.addPlaneSurface([1], 2)
#mesh.addPlaneSurface([2], 3)

mesh.revolve([(2, 2)], 0,0,0, 0,0,1, 2*pi/3)
mesh.revolve([(2, 21)], 0,0,0, 0,0,1, 2*pi/3)
mesh.revolve([(2, 38)], 0,0,0, 0,0,1, 2*pi/3)

mesh = gmsh.model.geo



mesh.synchronize()

gmsh.model.mesh.generate(3)
gmsh.write("v2test.mesh")


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()