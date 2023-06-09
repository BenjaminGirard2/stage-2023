from __future__ import absolute_import
from sfepy.mechanics.matcoefs import stiffness_from_lame
from sfepy.discrete.fem.utils import refine_mesh
import numpy as np
from math import sin, cos, pi


filename_mesh = r'C:\Users\Benjamin/Desktop/stage 2023/mesh\test_mesh2.mesh'

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

k = 1e5
f0 = 1e-2

materials = {
    'Aluminum' : ({'D': stiffness_from_lame(3, lamb, mu)},),
    'Load' : ({'.val' : [0.0, 0.0, 100.0]},),
    'cs': ({'f' : [k, f0], '.c': [0, 0, 1/4], '.r': 1/8,}),
}

variables = {
    'u' : ('unknown field', 'displacement', 0),
    'v' : ('test field', 'displacement', 'u'),
}

exterior_radius = 0.1
interior_radius = 0.02

sceew_radius = 0.05  
distance_from_center = 0.8
number_of_supports= 6


regions = {
    'Omega' : 'all',
    'circonference': 'vertices by select_circ_out',
    'center_0' : ('vertices by select_circ_in'),
    'supported' : 'vertices by select_supports',
    'bottom' : 'vertices in (z < 0.05)'
}

ebcs = {
    'fixed' : ('supported', {'u.all' : 0.0}),
}

equations = {
   'balance_of_forces' :
   """dw_lin_elastic.2.Omega(Aluminum.D, v, u)
   + dw_contact_sphere.2.bottom(cs.f, cs.c, cs.r, v, u)
      = 0""",
}

solvers = {
    'ls' : ('ls.scipy_direct', {}),
    'newton' : ('nls.newton', {
        'i_max' : 1,
        'eps_a' : 1e-1,
        'delta' : 1e-6,
    }),
}



functions = {
    'select_circ_out': (lambda coors, domain=None:
                    select_circ_out(coors[:,0], coors[:,1], 0, exterior_radius),),
    'select_circ_in': (lambda coors, domain=None:
                    select_circ_in(coors[:,0], coors[:,1], 0, interior_radius),),
    'select_supports': (lambda coors, domain=None:
                    select_supports(coors[:,0], coors[:,1], 0, [sceew_radius, distance_from_center, number_of_supports]),),
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



def main():
    import os

    import numpy as nm
    import matplotlib.pyplot as plt

    from sfepy.discrete.fem import MeshIO
    import sfepy.linalg as la
    from sfepy.mechanics.contact_bodies import ContactSphere, plot_points

    conf_dir = "disque_3d_copy.py"
    filename_mesh = r'C:\Users\Benjamin/Desktop/stage 2023/mesh\test_mesh2.mesh'
    io = MeshIO.any_from_filename(filename_mesh, prefix_dir=conf_dir)
    bb = io.read_bounding_box()
    outline = [vv for vv in la.combine(list(zip(*bb)))]

    print(materials['cs'])

    ax = plot_points(None, nm.array(outline), 'r*')
    csc = materials['cs']
    cs = ContactSphere(csc['.c'], csc['.r'])

    pps = (bb[1] - bb[0]) * nm.random.rand(5000, 3) + bb[0]
    mask = cs.mask_points(pps, 0.0)

    ax = plot_points(ax, cs.centre[None, :], 'b*', ms=30)
    ax = plot_points(ax, pps[mask], 'kv')
    ax = plot_points(ax, pps[~mask], 'r.')

    plt.show()

if __name__ == '__main__':
    pass
    #   main()