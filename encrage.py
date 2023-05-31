import matplotlib.pyplot as plt
from math import pi, cos, sin, sqrt
import numpy as np



xx = np.array([1, 0.9, 0.8, 0.7, 0.8, 0.1, -0.9])
yy = np.array([0, 0, 0, 0.1, 1, 2, 0])

def selection_supports( x, y, z, small_radius, big_radius, number_of_supports ):

    res = np.empty(0)
    for i in range(number_of_supports):
        
        angle = (2 * i * pi)/number_of_supports
        a = big_radius * cos(angle)
        b = big_radius * sin(angle)

        value = np.sqrt((x-a)**2 + (y-b)**2)


        out = np.where(value <= small_radius)[0]
        res = np.append(res, out)

    return np.intp(res)