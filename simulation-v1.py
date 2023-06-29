from __future__ import absolute_import
from sfepy.mechanics.matcoefs import stiffness_from_lame
from sfepy.discrete.fem.utils import refine_mesh
import numpy as np
from math import sin, cos, pi


filename_mesh = r'C:\Users\Benjamin\Desktop\stage 2023\mesh\centr_true_size_4.mesh'

refinement_level = 0
filename_mesh = refine_mesh(filename_mesh, refinement_level)



young = 69000.0 # Young's modulus [MPa]
poisson = 0.33  # Poisson's ratio



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
    'Aluminum' : ({'D': stiffness_from_lame(3, lamb, mu)},),
    'Load' : ({'.val' : [0.0, 0.0, 0.075]},),
}

variables = {
    'u' : ('unknown field', 'displacement', 0),
    'v' : ('test field', 'displacement', 'u'),
}

exterior_radius = 4
interior_radius = 0.25

sceew_radius = 0.2
distance_from_center = 4.2
number_of_supports= 2

radius_off_center = 0.3
radius_off_center_distance = 3


regions = {
    'Omega' : 'all',
    'center_0' : ('vertices by select_circ_in'),
    'center_offset' : ('vertices by select_circ_off_center'),
    'supported' : 'vertices by select_supports',
}

ebcs = {
    'fixed' : ('supported', {'u.all' : 0.0}),
}

equations = {
   'balance_of_forces' :
   """dw_lin_elastic.3.Omega(Aluminum.D, v, u)
      = dw_point_load.0.center_0(Load.val, v)""",
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
    'select_supports': (lambda coors, domain=None:
                    select_supports(coors[:,0], coors[:,1], 0, [sceew_radius, distance_from_center, number_of_supports]),),
    'select_circ_off_center': (lambda coors, domain=None:
                    select_circ_off_center(coors[:,0], coors[:,1], 0, [radius_off_center, radius_off_center_distance]),),
}

def select_circ_off_center( x, y, z, params ):
    """Select disk subdomain of a given radius offcentered."""
    r = np.sqrt( np.square(x-params[1]), np.square(y) )

    out = np.where(r < params[0])[0]

    n = out.shape[0]
    if n <= 3:
        raise ValueError( 'too few vertices selected! (%d)' % n )

    return out


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


def select_supports( x, y, z, parameters ):

    res = np.empty(0)
    for i in range(parameters[2]):  
        
        angle = (2 * i * pi)/parameters[2]
        a = parameters[1] * cos(angle)
        b = parameters[1] * sin(angle)

        value = np.sqrt(np.square(x-a) + np.square(y-b))


        out = np.where(value <= parameters[0])[0]
        res = np.append(res, out)
        
    n = out.shape[0]
    if n <= 2 * parameters[2]:
        
        raise ValueError( 'too few vertices selected! (%d)' % n )


    return np.intp(res)