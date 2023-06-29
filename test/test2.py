import gmsh
import sys



gmsh.initialize()

gmsh.model.add("try_1")

c = 20
nb_segment = 20
m_size = c/nb_segment


mesh = gmsh.model.geo


mesh.addPoint(10, 10, 0, m_size, 2) 
mesh.addPoint(10, -10, 0, m_size, 3) 
mesh.addPoint(-10, -10, 0, m_size, 4) 
mesh.addPoint(-10, 10, 0, m_size, 5)

mesh.addLine(2, 3, 1)
mesh.addLine(3, 4, 2)
mesh.addLine(4, 5, 3)
mesh.addLine(5, 2, 4)

mesh.addCurveLoop([1,2,3,4], 1)

mesh.addPlaneSurface([1], 2)


mesh.synchronize()



mesh.extrude([(2, 2)], 0, 0, 0.5, recombine=True)

gmsh.option.setNumber("Mesh.Algorithm", 8)
#gmsh.option.setNumber("Mesh.RecombineAll", 1)

mesh.synchronize()

gmsh.model.mesh.generate(3)
gmsh.write("carre.mesh")


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()