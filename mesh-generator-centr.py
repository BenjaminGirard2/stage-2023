import gmsh
import sys



gmsh.initialize()

gmsh.model.add("try_1")

m_size = 17.5e-02
m_size2 = 4e-02

mesh = gmsh.model.geo

mesh.addPoint(0, 0, 0, m_size, 1) 

mesh.addPoint(5, 0, 0, m_size, 2) 
mesh.addPoint(0, 5, 0, m_size, 3) 
mesh.addPoint(-5, 0, 0, m_size, 4) 
mesh.addPoint(0, -5, 0, m_size, 5)

mesh.addPoint(0.4, 0, 0, m_size, 6) 
mesh.addPoint(0, 0.4, 0, m_size, 7) 
mesh.addPoint(-0.4, 0, 0, m_size, 8) 
mesh.addPoint(0, -0.4, 0, m_size, 9)

mesh.addCircleArc(2, 1, 3, 1)
mesh.addCircleArc(3, 1, 4, 2)
mesh.addCircleArc(4, 1, 5, 3)
mesh.addCircleArc(5, 1, 2, 4)

mesh.addCircleArc(6, 1, 7, 5)
mesh.addCircleArc(7, 1, 8, 6)
mesh.addCircleArc(8, 1, 9, 7)
mesh.addCircleArc(9, 1, 6, 8)

mesh.addCurveLoop([1,2,3,4], 1)

mesh.addCurveLoop([5,6,7,8], 3)

mesh.addPlaneSurface([1, 3], 2)

mesh.addPlaneSurface([3], 4)

mesh.synchronize()


mesh.extrude([(2, 2)], 0, 0, 0.31)
mesh.extrude([(2, 4)], 0, 0, 0.31, [10], recombine=True)


mesh.synchronize()

gmsh.model.mesh.generate(3)
gmsh.write("mesh\centr_true_size_5.mesh")


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()