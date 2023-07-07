from __future__ import absolute_import
from sfepy.mechanics.matcoefs import stiffness_from_youngpoisson
from math import pi, sin, cos


filename_mesh = r'circular_mince.mesh'



young = 210000.0 # Young's modulus [MPa]
poisson = 0.3  # Poisson's ratio



options = {
    'output_format' : 'vtk',
    'nls' : 'newton',
    'ls' : 'ls'
}


fields = {
    'displacement' : ('real', 3, 'Omega', 1)
}


materials = {
    'Aluminum': ({'D': stiffness_from_youngpoisson(3, young, poisson)},),
    'Load_g'  : ({'.val' : [3000, 0.0, 0.0]},),
    'Load'    : ({'.val' : [0, 0.0, 4]},),
    'Load_m'  : ({'.val' : [0.0, 0.0, 100.0]},),
}


variables = {
    'u' : ('unknown field', 'displacement', 0),
    'v' : ('test field', 'displacement', 'u'),
}


regions = {
    'Omega' : 'all',
    'pt_1' : ('vertex 1', 'vertex'),
    'pt_2' : ('vertex 2', 'vertex'),
    'pt_3' : ('vertex 3', 'vertex'),
    'pt_4' : ('vertex 4', 'vertex'),
    'pt_5' : ('vertex 5', 'vertex'),
    'pt_6' : ('vertex 6', 'vertex'),
    'pt_7' : ('vertex 7', 'vertex'),
    'pt_8' : ('vertex 8', 'vertex'),
    'pt_9' : ('vertex 9', 'vertex'),
    'pt_10' : ('vertex 10', 'vertex'),
    'pt_11' : ('vertex 11', 'vertex'),
    'pt_12' : ('vertex 12', 'vertex'),
    'pt_13' : ('vertex 13', 'vertex'),
    'pt_14' : ('vertex 14', 'vertex'),
    'pt_15' : ('vertex 15', 'vertex'),
    'pt_16' : ('vertex 16', 'vertex'),
    'pt_17' : ('vertex 17', 'vertex'),
    'pt_18' : ('vertex 18', 'vertex'),
    'pt_19' : ('vertex 19', 'vertex'),
    'pt_20' : ('vertex 20', 'vertex'),
}

d = -1
ebcs = {'p1': ('pt_1', {'u.0': d*0.1, 'u.1': d*0.0, 'u.2': 0}), 
        'p2': ('pt_2', {'u.0': d*0.09510565162951536, 'u.1': d*0.03090169943749474, 'u.2': 0}), 
        'p3': ('pt_3', {'u.0': d*0.08090169943749476, 'u.1': d*0.058778525229247314, 'u.2': 0}), 
        'p4': ('pt_4', {'u.0': d*0.058778525229247314, 'u.1': d*0.08090169943749476, 'u.2': 0}), 
        'p5': ('pt_5', {'u.0': d*0.030901699437494747, 'u.1': d*0.09510565162951536, 'u.2': 0}), 
        'p6': ('pt_6', {'u.0': d*6.123233995736766e-18, 'u.1': d*0.1, 'u.2': 0}), 
        'p7': ('pt_7', {'u.0': d*-0.030901699437494736, 'u.1': d*0.09510565162951537, 'u.2': 0}), 
        'p8': ('pt_8', {'u.0': d*-0.05877852522924731, 'u.1': d*0.08090169943749476, 'u.2': 0}), 
        'p9': ('pt_9', {'u.0': d*-0.08090169943749474, 'u.1': d*0.05877852522924733, 'u.2': 0}),
        'p10': ('pt_10', {'u.0': d*-0.09510565162951536, 'u.1': d*0.030901699437494753, 'u.2': 0}), 
        'p11': ('pt_11', {'u.0': d*-0.1, 'u.1': d*1.2246467991473533e-17, 'u.2': 0}), 
        'p12': ('pt_12', {'u.0': d*-0.09510565162951537, 'u.1': d*-0.03090169943749473, 'u.2': 0}),
        'p13': ('pt_13', {'u.0': d*-0.08090169943749476, 'u.1': d*-0.05877852522924731, 'u.2': 0}),
        'p14': ('pt_14', {'u.0': d*-0.05877852522924733, 'u.1': d*-0.08090169943749474, 'u.2': 0}),
        'p15': ('pt_15', {'u.0': d*-0.030901699437494757, 'u.1': d*-0.09510565162951536, 'u.2': 0}),
        'p16': ('pt_16', {'u.0': d*-1.8369701987210297e-17, 'u.1': d*-0.1, 'u.2': 0}), 
        'p17': ('pt_17', {'u.0': d*0.030901699437494726, 'u.1': d*-0.09510565162951537, 'u.2': 0}), 
        'p18': ('pt_18', {'u.0': d*0.05877852522924729, 'u.1': d*-0.08090169943749476, 'u.2': 0}), 
        'p19': ('pt_19', {'u.0': d*0.08090169943749474, 'u.1': d*-0.05877852522924734, 'u.2': 0}), 
        'p20': ('pt_20', {'u.0': d*0.09510565162951536, 'u.1': d*-0.030901699437494767, 'u.2': 0})
        }


equations = {
   'balance_of_forces' :
   """dw_lin_elastic.3.Omega(Aluminum.D, v, u)
      = 0""",
}


solvers = {
    'ls' : ('ls.scipy_direct', {}),
    'newton' : ('nls.newton', {
        'i_max' : 1,
        'eps_a' : 1e-6,
    }),
}


