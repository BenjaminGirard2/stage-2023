import gmsh
import sys



gmsh.initialize()

gmsh.model.add("try_1")

c = 10
m_size = 0.25

number_points = 10

spacing = c/number_points
mesh = gmsh.model.geo

a = 0
for x in [0, c]:
    y = 0

    if x == c:
        y = c - spacing
        spacing = -spacing

    for i in range(number_points):
        
        a += 1
        mesh.addPoint(x, y, 0, m_size, a)
        y += spacing


for i in range(a):
    if i==(a-1):
        mesh.addLine(i+1, 1, i+1)
        break
    mesh.addLine(i+1, i+2, i+1)


list_pt = []
for i in range(a):
    list_pt.append(i+1)


mesh.addCurveLoop(list_pt, 1)

mesh.addPlaneSurface([1], 2)


mesh.synchronize()



mesh.extrude([(2, 2)], 0, 0, 0.25)

gmsh.option.setNumber("Mesh.Algorithm", 1)
#gmsh.option.setNumber("Mesh.RecombineAll", 1)

mesh.synchronize()

gmsh.model.mesh.generate(3)
gmsh.write("carre_v2_mince.mesh")


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()