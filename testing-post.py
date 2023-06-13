from postprocessing import PostProcessing

filename = r'C:\Users\Benjamin\Desktop\stage 2023\vtk-files\al_test_1.vtk'
post = PostProcessing(filename)


def func(x,y):
    a = 0.0005
    z = a*x**2 + a*y**2 + 0.305
    return z

post.filter_coords_in_z()
post.filter_coords_in_y(0.2)
post.apply_circular_symetric_polishing(func)

post.plot_displacement()
post.plot_xz()

