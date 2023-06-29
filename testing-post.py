from postprocessing import PostProcessing
from numpy import sqrt

filename = r'C:\Users\Benjamin\Desktop\stage 2023\vtk-files\centr_true_size_4-3.vtk'
post = PostProcessing(filename)


def absolut(x,y):
    a = 0.006
    z = a*abs(x) + a*abs(y) + 0.31
    return z

def parabola(x,y):
    a = 0.001
    z = a*x**2 + a*y**2 + 0.31
    return z

def circular(x,y):
    a = 10000
    z = -sqrt(a-x**2-y**2) + sqrt(a)+0.28
    return z


post.filter_coords_in_z()
post.filter_coords_in_y(0.1)
post.plot_displacement()
post.filter_coords_in_x(3)
post.apply_flat_polishing(0.1)
#post.apply_circular_symetric_polishing(parabola)

post.plot_displacement()
post.curve_fit_parapola()

post.find_polishing_parameters_parabola(16)

post.apply_corrected_polishing()
post.curve_fit_parapola()
