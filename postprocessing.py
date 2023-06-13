import meshio
import numpy as np
import matplotlib.pyplot as plt


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
            raise ValueError(' No value selected, probaly the zmin value is \
                             wrong ')
        
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


    def apply_flat_polishing(self, depth):

        """Apply the polishing on the surface under stress.
        The depth given is the thickness you want to remove.
        We assume that the thickness of the plate start at z=0"""


        thickness = max(self.z_coors)
        if depth > thickness:
            raise ValueError('The depth is too much, the thickness of the \
                             plate is the following:(%g)' % thickness)
        
        zmax = max(self.u_field_z) + max(self.z_coors)
        height_max = zmax - depth

        new_x = new_y = new_z = new_ux = new_uy = new_uz = np.empty(0)

        for pos, uz in enumerate(self.u_field_z):
            z_displaced = self.z_coors[pos]+uz

            if z_displaced > height_max:
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
            raise ValueError(' No value selected during the flatening')

        self.u_field_x = new_ux
        self.u_field_y = new_uy
        self.u_field_z = new_uz

        self.x_coors = new_x
        self.y_coors = new_y
        self.z_coors = new_z


    def plot_xz(self):
        """Plot the values of the x coordinates with their coresponding z 
        coordinates"""

        plt.scatter(self.x_coors, self.z_coors)
        plt.show()


    def plot_displacement(self):
        """Plot the values of the x coordinates with their coresponding z 
        coordinates but with the displacement added. One more argument can
        be given to cut the values because sometime there is a wrong value at
        the start."""
        
        scissors = 1

        plt.scatter(self.x_coors[scissors:] + self.u_field_x[scissors:], 
                    self.z_coors[scissors:] + self.u_field_z[scissors:])
        plt.show()
