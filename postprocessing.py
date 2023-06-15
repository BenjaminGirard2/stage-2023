import meshio
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize


class PostProcessing():
    """Take a .vtk file and process it to take the values."""

    def __init__(self, file_name):
        """Create the class instance with the file name.
        Must be string and be a .vtk file"""

        self.mesh = meshio.read(file_name)

        self.u_field_x = self.mesh.point_data['u'][:,0]
        self.u_field_y = self.mesh.point_data['u'][:,1]
        self.u_field_z = self.mesh.point_data['u'][:,2]

        self.x_coors = self.mesh.points[:,0]
        self.y_coors = self.mesh.points[:,1]
        self.z_coors = self.mesh.points[:,2]

        self.is_polished = False


    def filter_coords_in_z(self, zmin=0.3):
        """Allows just the coordinates that have bigger z values than zmin"""
        
        new_x = new_y = new_z = new_ux = new_uy = new_uz = np.empty(0)

        for pos, coord in enumerate(self.z_coors):
            if coord > zmin:
                new_ux = np.append(new_ux, self.u_field_x[pos])
                new_uy = np.append(new_uy, self.u_field_y[pos])
                new_uz = np.append(new_uz, self.u_field_z[pos])

                new_x = np.append(new_x, self.x_coors[pos])
                new_y = np.append(new_y, self.y_coors[pos])
                new_z = np.append(new_z, self.z_coors[pos])

        if len(new_uz) < 1:
            raise ValueError('No value selected, probaly the zmin value is '
                             'wrong')
        
        self.u_field_x = new_ux
        self.u_field_y = new_uy
        self.u_field_z = new_uz

        self.x_coors = new_x
        self.y_coors = new_y
        self.z_coors = new_z


    def filter_coords_in_x(self, xmax, *xmin):
        
        """This fonction filter the coordinates to keep just the ones inside 
        the boundaries.
        Can accept one or two values, if two is given, the first one is the 
        max value, the second one is going to be the min value.
        If only one is given, the min is going to be -max."""


        if not xmin:
            xmin = -xmax
        else:
            xmin = xmin[0]

        new_x = new_y = new_z = new_ux = new_uy = new_uz = np.empty(0)

        for pos, coord in enumerate(self.x_coors):
            if coord > xmin and coord < xmax:
                new_ux = np.append(new_ux, self.u_field_x[pos])
                new_uy = np.append(new_uy, self.u_field_y[pos])
                new_uz = np.append(new_uz, self.u_field_z[pos])

                new_x = np.append(new_x, self.x_coors[pos])
                new_y = np.append(new_y, self.y_coors[pos])
                new_z = np.append(new_z, self.z_coors[pos])

        if len(new_ux) < 1:
            raise ValueError(' No value selected in x')
            
        self.u_field_x = new_ux
        self.u_field_y = new_uy
        self.u_field_z = new_uz

        self.x_coors = new_x
        self.y_coors = new_y
        self.z_coors = new_z


    def filter_coords_in_y(self, ymax, *ymin):

        """Keep only the y coordinates between the xmin and xmax values. 
        If only one value is given, the min is going to be -max"""


        if not ymin:
            ymin = -ymax
        else:
            ymin = ymin[0]

        new_x = new_y = new_z = new_ux = new_uy = new_uz = np.empty(0)

        for pos, coord in enumerate(self.y_coors):
            if (coord > ymin) and (coord < ymax):
                new_ux = np.append(new_ux, self.u_field_x[pos])
                new_uy = np.append(new_uy, self.u_field_y[pos])
                new_uz = np.append(new_uz, self.u_field_z[pos])

                new_x = np.append(new_x, self.x_coors[pos])
                new_y = np.append(new_y, self.y_coors[pos])
                new_z = np.append(new_z, self.z_coors[pos])
                
        if len(new_uy) < 1:
            raise ValueError('No value selected in y')
            
        self.u_field_x = new_ux
        self.u_field_y = new_uy
        self.u_field_z = new_uz

        self.x_coors = new_x
        self.y_coors = new_y
        self.z_coors = new_z


    def apply_flat_polishing(self, depth, *boundary):

        """Apply the polishing on the surface under stress.
        The depth given is the thickness you want to remove.
        We assume that the thickness of the plate start at z=0
        Additionnal argument can be given to do the polishing only on a 
        certain zone in x: first additional is the ymax and second is the
        ymin"""

        if self.is_polished:
            raise InterruptedError('Its already polished! What are you trying'
                                   'to do?')

        thickness = max(self.z_coors)
        if depth > thickness:
            raise ValueError('The depth is too much, the thickness of the '
                             'plate is the following:(%g)' % thickness)
        
        zmax = max(self.u_field_z) + max(self.z_coors)
        height_max = zmax - depth

        new_x = new_y = new_z = new_ux = new_uy = new_uz = np.empty(0)

        if not boundary:
            for pos, uz in enumerate(self.u_field_z):
                z_displaced = self.z_coors[pos]+uz

                if z_displaced >= height_max:
                    
                    height_cutted = z_displaced-height_max
                    new_z = np.append(new_z, self.z_coors[pos]-height_cutted)

                else:
                    new_z = np.append(new_z, self.z_coors[pos])

                new_ux = np.append(new_ux, self.u_field_x[pos])
                new_uy = np.append(new_uy, self.u_field_y[pos])
                new_uz = np.append(new_uz, self.u_field_z[pos])

                new_x = np.append(new_x, self.x_coors[pos])
                new_y = np.append(new_y, self.y_coors[pos])
        else:
            xmax = boundary[0]
            xmin = boundary[1]
            for pos, uz in enumerate(self.u_field_z):
                z_displaced = self.z_coors[pos]+uz

                if (z_displaced >= height_max) and (self.x_coors[pos] > xmin)\
                and (self.x_coors[pos] < xmax):
                    
                    height_cutted = z_displaced-height_max
                    new_z = np.append(new_z, self.z_coors[pos]-height_cutted)

                else:
                    new_z = np.append(new_z, self.z_coors[pos])

                new_ux = np.append(new_ux, self.u_field_x[pos])
                new_uy = np.append(new_uy, self.u_field_y[pos])
                new_uz = np.append(new_uz, self.u_field_z[pos])

                new_x = np.append(new_x, self.x_coors[pos])
                new_y = np.append(new_y, self.y_coors[pos])


        
        if len(new_z) < 1:
            raise ValueError('No value selected during the flatening')

        self.u_field_x = new_ux
        self.u_field_y = new_uy
        self.u_field_z = new_uz

        self.x_coors = new_x
        self.y_coors = new_y
        self.z_coors = new_z

        self.is_polished = True


    def apply_circular_symetric_polishing(self, function, *boundary):
        """Apply the polishing but with any function. The function must take a
        value in x and y and return a value of z. This will remove all values 
        that are greater than the curve given
        
        The function must have the following format:

        def func(x, y):
        
            z = x**2 +y**2 + 0.3

            return z
            """
        
        if self.is_polished:
            raise InterruptedError('Its already polished! What are you trying'
                                   'to do?')

        new_x = new_y = new_z = new_ux = new_uy = new_uz = np.empty(0)

        if not boundary:
            for pos, uz in enumerate(self.u_field_z):
                z_displaced = self.z_coors[pos]+uz
                value_of_fct = function(self.x_coors[pos], self.y_coors[pos])

                if z_displaced >= value_of_fct:
                    height_cutted = z_displaced-value_of_fct
                    new_z = np.append(new_z, self.z_coors[pos]-height_cutted)

                else:
                    new_z = np.append(new_z, self.z_coors[pos])

                new_ux = np.append(new_ux, self.u_field_x[pos])
                new_uy = np.append(new_uy, self.u_field_y[pos])
                new_uz = np.append(new_uz, self.u_field_z[pos])

                new_x = np.append(new_x, self.x_coors[pos])
                new_y = np.append(new_y, self.y_coors[pos])

        else:
            xmax = boundary[0]
            xmin = boundary[1]

            for pos, uz in enumerate(self.u_field_z):
                z_displaced = self.z_coors[pos]+uz
                value_of_fct = function(self.x_coors[pos], self.y_coors[pos])

                if (z_displaced >= value_of_fct) and (self.x_coors[pos] > xmin) \
                and (self.x_coors[pos] < xmax):
                    
                    height_cutted = z_displaced-value_of_fct
                    new_z = np.append(new_z, self.z_coors[pos]-height_cutted)

                else:
                    new_z = np.append(new_z, self.z_coors[pos])

                new_ux = np.append(new_ux, self.u_field_x[pos])
                new_uy = np.append(new_uy, self.u_field_y[pos])
                new_uz = np.append(new_uz, self.u_field_z[pos])

                new_x = np.append(new_x, self.x_coors[pos])
                new_y = np.append(new_y, self.y_coors[pos])

        if len(new_z) < 1:
            raise ValueError('No value selected during the flatening')

        self.u_field_x = new_ux
        self.u_field_y = new_uy
        self.u_field_z = new_uz

        self.x_coors = new_x
        self.y_coors = new_y
        self.z_coors = new_z

        self.is_polished = True


    def plot_xz(self, scissors=1):
        """Plot the values of the x coordinates with their coresponding z 
        coordinates"""

#TODO: add graph title, axis and fancy it
        plt.scatter(self.x_coors[scissors:], self.z_coors[scissors:])
        plt.show()


    def plot_displacement(self, scissors=1):
        """Plot the values of the x coordinates with their coresponding z 
        coordinates but with the displacement added. One more argument can
        be given to cut the values because sometime there is a wrong value at
        the start."""
        
#TODO: add graph title, axis and fancy it
        plt.scatter(self.x_coors[scissors:] + self.u_field_x[scissors:], 
                    self.z_coors[scissors:] + self.u_field_z[scissors:])
        plt.show()


    def curve_fit_parapola(self, show_residual=False, use_displacement=False, scissors=1):

        """Apply a parabolic curve fit the the values on the x axis and show 
        it. The values must a short variation in the y direction or else 
        there's going to be a lot of noice."""

        xdata = self.x_coors[scissors:]
        zdata = self.z_coors[scissors:]

        if use_displacement:
            xdata = xdata + self.u_field_x[scissors:]
            zdata = zdata + self.u_field_z[scissors:]

        def parapola(x, a, b, c):
            return a*x**2 + b*x + c

        p = Parameters()
        p.add('a', value=0.2)
        p.add('b', value=0)
        p.add('c', value=0.25)

        def residual(pars, x, data):
            a = pars['a']
            b = pars['b']
            c = pars['c']
            model = parapola(x, a, b, c)
            return model - data

        out = minimize(residual, p, args=(xdata, zdata))

        self.results = out
#TODO: add graph title, axis and fancy it
        plt.scatter(xdata, zdata)
        plt.scatter(xdata, zdata + out.residual)
        plt.xlabel('Distance en x [mm]')
        plt.ylabel('Hauteur [\u03BCm]')
        plt.show()

        if show_residual:
            plt.scatter(xdata,out.residual)
            plt.show()


    def find_polishing_parameters_parabola(self, order, apply_it=False, scissors=1,
                                          verbose=True):
        """This function find the best curve than fit the values. Use 
        polynomial curve fitting"""

        xdata = self.x_coors[scissors:]
        zdata = self.z_coors[scissors:]

        if order > 25:
            raise ValueError('Cant have a grater value than for now.')

        def parapola(x, a, b, c):
            return a*x**2 + b*x + c

        parabola_parameters = Parameters()
        parabola_parameters.add('a', value=0.2)
        parabola_parameters.add('b', value=0)
        parabola_parameters.add('c', value=0.25)

        def residual_from_parabola(pars, x, data):
            a = pars['a']
            b = pars['b']
            c = pars['c']
            model = parapola(x, a, b, c)
            return model - data

        parabola_out = minimize(residual_from_parabola, parabola_parameters, 
                                args=(xdata, zdata))

        def polynomial_func(*args):
            
            x = args[0]
            result = 0

            for pos, value in enumerate(args[1:][0]):
                result += value*x**pos
            return result

        p2 = Parameters()
        for i in range(order+1):
            p2.add(chr(97+i), value=0.01)

        def residual2(pars, x, data):
            params_list = []
            for i in range(order+1):
                params_list.append(pars[chr(97+i)])

            model = polynomial_func(x, params_list)
            return model - data
                
        out2 = minimize(residual2, p2, args=(xdata, parabola_out.residual))

        self.last_inter_values = out2.last_internal_values
   
        if apply_it:
            self.apply_polishing(verbose=True)



        if verbose:
            print(out2.last_internal_values)

            plt.scatter(xdata, parabola_out.residual + out2.residual)
            plt.scatter(xdata, parabola_out.residual)
            plt.show() 



    def apply_polishing(self, verbose=True):

        if 'self.last_inter_values' not in locals():
            raise AttributeError('You have to find the parameters first using'
                                 ' the find_polishing_parameters_parabola'
                                 'function.')
        
        




    def curve_fit_circular(self, use_displacement=False, scissors=1):
    
        """BROKEN
        
        Apply a shepric curve fit the the values on the x axis and show 
        it. The values must a short variation in the y direction or else 
        there's going to be a lot of noice."""

        xdata = self.x_coors[scissors:]
        zdata = self.z_coors[scissors:]

        if use_displacement:
            xdata = xdata + self.u_field_x[scissors:]
            zdata = zdata + self.u_field_z[scissors:]

        def circle(x, a, b, c):
            return -np.sqrt(a-(x-b)**2) + c

        p = Parameters()
        p.add('a', value=30000)
        p.add('b', value=0)
        p.add('c', value=0.3)

        def residual(pars, x, data):
            a = pars['a']
            b = pars['b']
            c = pars['c']
            model = circle(x, a, b, c)
            return model - data

        out = minimize(residual, p, args=(xdata, zdata))
        
#TODO: add graph title, axis and fancy it
        plt.scatter(xdata, zdata)
        plt.scatter(xdata, zdata + out.residual)
        plt.xlabel('Distance en x [mm]')
        plt.ylabel('Hauteur [\u03BCm]')
        plt.show()

