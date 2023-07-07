from postprocessing import PostProcessing
from numpy import sqrt

filename = r'C:\Users\Benjamin\Desktop\stage 2023\circular_mince.vtk'
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


post.filter_coords_in_z(0.2)
post.filter_coords_in_y(0.4)
post.curve_fit_parapola(use_displacement=True, scissors=2)
post.curve_fit_circular()

#post.apply_circular_symetric_polishing(parabola)


#post.curve_fit_parapola()
