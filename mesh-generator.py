import gmsh
import sys



gmsh.initialize()

gmsh.model.add("try_1")

m_size = 10e-02

mesh = gmsh.model.geo

mesh.addPoint(0, 0, 0, m_size, 1) 

mesh.addPoint(5, 0, 0, m_size, 2) 
mesh.addPoint(0, 5, 0, m_size, 3) 
mesh.addPoint(-5, 0, 0, m_size, 4) 
mesh.addPoint(0, -5, 0, m_size, 5)

mesh.addCircleArc(2, 1, 3, 1)
mesh.addCircleArc(3, 1, 4, 2)
mesh.addCircleArc(4, 1, 5, 3)
mesh.addCircleArc(5, 1, 2, 4)

mesh.addCurveLoop([1,2,3,4], 1)

mesh.addPlaneSurface([1], 2)

mesh.synchronize()


mesh.extrude([(2, 2)], 0, 0, 0.31)


mesh.synchronize()

gmsh.model.mesh.generate(3)
gmsh.write("mid_true_size.mesh")


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()