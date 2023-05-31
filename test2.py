import matplotlib.pyplot as plt
from math import pi, cos, sin, sqrt
import numpy as np

np.random.seed(1)

#x = np.array([1, 0.9, 0.8, 0.7, 0.8, 0.1, -0.9, 0.4, -0.4])
#y = np.array([0, 0, 0, 0.1, 1, 2, 0, 0.7, 0.7])

x = np.random.rand(500)
x = np.append(x, np.random.rand(500))
x = np.append(x, -np.random.rand(500))
x = np.append(x, -np.random.rand(500))

y = np.random.rand(500)
y = np.append(y, -np.random.rand(500))
y = np.append(y, -np.random.rand(500))
y = np.append(y, np.random.rand(500))

coords = np.array([x,y])
print(coords)
exterior_radius = 0.1
interior_radius = 0.05

sceew_radius = 0.04     
distance_from_center = 0.8
number_of_supports= 1

functions = {
    'select_circ_out': (lambda coors, domain=None:
                    select_circ_out(coors[:,0], coors[:,1], 0, exterior_radius),),
    'select_circ_in': (lambda coors, domain=None:
                    select_circ_in(coors[:,0], coors[:,1], 0, interior_radius),),
    'select_supports': (lambda coors, domain=None:
                    select_supports(coors[:,0], coors[:,1], 0, sceew_radius, distance_from_center, number_of_supports),),
}


def select_circ_out( x, y, z, radius ):
    """Select disk subdomain of a given radius."""
    r = np.sqrt( x**2 + y**2 )

    out = np.where(r > radius)[0]

    n = out.shape[0]
    if n <= 3:
        raise ValueError( 'too few vertices selected! (%d)' % n )

    return out


def select_circ_in( x, y, z, radius ):
    """Select circular subdomain of a given radius."""
    r = np.sqrt( x**2 + y**2 )

    out = np.where(r < radius)[0]

    n = out.shape[0]
    if n <= 3:
        raise ValueError( 'too few vertices selected! (%d)' % n )

    return out


def select_supports( x, y, z, small_radius, big_radius, number_of_supports ):

    res = np.empty(0)
    for i in range(number_of_supports):
        
        angle = (2 * i * pi)/number_of_supports
        a = big_radius * cos(angle)
        b = big_radius * sin(angle)

        value = np.sqrt(np.square(x-a) + np.square(y-b))


        out = np.where(value <= small_radius)[0]
        res = np.append(res, out)
        


    return np.intp(res)





for i in res:
    plt.scatter(x[i], y[i])

plt.show()
