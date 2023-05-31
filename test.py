from __future__ import absolute_import
from sfepy.mechanics.matcoefs import stiffness_from_youngpoisson
from sfepy.discrete.fem.utils import refine_mesh
from sfepy import data_dir
import numpy as np

filename_mesh = r'C:\Users\Benjamin\Desktop\stage 2023\carre.mesh'

refinement_level = 0
filename_mesh = refine_mesh(filename_mesh, refinement_level)

output_dir = '.' 

young = 69000.0 # Young's modulus [MPa]
poisson = 0.33  # Poisson's ratio

options = {
    'output_dir' : output_dir,
}
#vertex 160 et 83 sont proche de (0,0)

exterior_radius = 0.89
interior_radius = 0.15

regions = {
    'Omega' : 'all',
    'disk' : ('vertices by select_circ_out', 'facet'),
    'center_0' : ('vertices by select_circ_in'),
    'center_1' : ('vertex 160', 'vertex'),
    'certer_2' : ('vertex 83', 'vertex'),
}

materials = {
    'Aluminum' : ({'D': stiffness_from_youngpoisson(2, young, poisson)},),
    'Load' : ({'.val' : [0.0, 1.0]},),
}

fields = {
    'displacement': ('real', 3, 'Omega', 1),
}

equations = {
   'balance_of_forces' :
   """dw_lin_elastic.2.Omega(Aluminum.D, v, u)
      = dw_point_load.0.Omega(Load.val, v)""",
}

variables = {
    'u' : ('unknown field', 'displacement', 0),
    'v' : ('test field', 'displacement', 'u'),
}

ebcs = {
    'fixed' : ('disk', {'u.all' : 0.0}),
}

solvers = {
    'ls' : ('ls.scipy_direct', {}),
    'newton' : ('nls.newton', {
        'i_max' : 1,
        'eps_a' : 1e-6,
    }),
}



functions = {
    'select_circ_out': (lambda coors, domain=None:
                    select_circ_out(coors[:,0], coors[:,1], 0, exterior_radius),),
    'select_circ_in': (lambda coors, domain=None:
                    select_circ_in(coors[:,0], coors[:,1], 0, interior_radius),),
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



#---------------------Post processing---------------------


