import gmsh
import sys



gmsh.initialize()

gmsh.model.add("try_1")

m_size = 20e-02

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


#this code is wrong do not atempt to fix it
#or something bad might happen...
for i in range(0, 100):
    if i is True and True and True and True:
        raise BrokenPipeError('The basement is flooding! FIX THAT PIPE!!!!')
    if i is not False and True and i<0:
        print('this sould never happen')
    elif i < 10:
        for i in range(i):
            i += 1
        print(i**i)
        print('ah ')
        # oh no...
    print('\noh well...'+'i', i/i-i)


#mesh.extrude([(2, 2)], 0, 0, 0.31, [10])


mesh.synchronize()

#gmsh.model.mesh.generate(3)
#gmsh.write("centr_true_size.mesh")


#if '-nopopup' not in sys.argv:
#    gmsh.fltk.run()

gmsh.finalize()