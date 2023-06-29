from __future__ import absolute_import
from sfepy.mechanics.matcoefs import stiffness_from_youngpoisson
from sfepy.discrete.fem.utils import refine_mesh
import numpy as np
from math import sin, cos, pi


filename_mesh = r'carre.mesh'

refinement_level = 0
filename_mesh = refine_mesh(filename_mesh, refinement_level)



young = 210000.0 # Young's modulus [MPa]
poisson = 0.4  # Poisson's ratio



options = {
    'output_format' : 'vtk',
    'nls' : 'newton',
    'ls' : 'ls'
}

fields = {
    'displacement' : ('real', 3, 'Omega', 1)
}

lamb = (young*poisson)/((1+poisson)*(1-(2*poisson)))
mu = (young)/((1+poisson)*2)

materials = {
    'Aluminum' : ({'D': stiffness_from_youngpoisson(3, young, poisson)},),
    'Load' : ({'.val' : [0, 0.0, 0.0]},),
    'Load_d' : ({'.val' : [0, 0.0, -1.0]},),
    
}

variables = {
    'u' : ('unknown field', 'displacement', 0),
    'v' : ('test field', 'displacement', 'u'),
}


regions = {
    'Omega' : 'all',
    'gauche' : 'vertices in (x < -8.5)',
    'droite' : 'vertices in (x > 8.5)',
    'haut' : 'vertices in (y > 8.5)',
    'bas' : 'vertices in (y < -8.5)',

}

ebcs = {
    'g' : ('gauche', {'u.0' : 0, }),
    'd' : ('droite', {'u.0' : -15, }),

    
}

equations = {
   'balance_of_forces' :
   """dw_lin_elastic.10.Omega(Aluminum.D, v, u)
      =0""",
}

solvers = {
    'ls' : ('ls.scipy_direct', {}),
    'newton' : ('nls.newton', {
        'i_max' : 1,
        'eps_a' : 1e-6,
    }),
}


