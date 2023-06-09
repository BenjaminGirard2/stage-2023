import meshio
import numpy as np
import matplotlib.pyplot as plt

mesh = meshio.read(r'vtk-files\centr_true_size_4-3.vtk')
u_field = mesh.point_data['u']
u_field_z = u_field[:,2]
x = mesh.points[:,0]
y = mesh.points[:,1]
z = mesh.points[:,2]

xmax = 0.6
ymax = 0.07
h = 0.4

x_res = y_res = z_res = x_res_filtered = y_res_filtered = z_res_filtered = np.empty(0)


#----------------------------------CAN BE DELETED----------------------------------#
x = y = z = u_field_z = np.empty(0)
u_field_raw = mesh.point_data['u']
u_field_raw_z = u_field_raw[:,2]
x_raw = mesh.points[:,0]
y_raw = mesh.points[:,1]
z_raw = mesh.points[:,2]
for pos, coord in enumerate(z_raw):
    if coord > 0.3:
        u_field_z = np.append(u_field_z, u_field_raw_z[pos])
        x = np.append(x, x_raw[pos])
        y = np.append(y, y_raw[pos])
        z = np.append(z, z_raw[pos])
#----------------------------------CAN BE DELETED----------------------------------#


for pos, u in enumerate(u_field_z):
    k = z[pos]+u-h

    if k > 0:
        z_res = np.append(z_res, z[pos]-k)

    else:
        z_res = np.append(z_res, z[pos])

    x_res = np.append(x_res, x[pos])
    y_res = np.append(y_res, y[pos])



for pos, item in enumerate(y_res):
    if abs(item) < ymax:
        x_res_filtered = np.append(x_res_filtered, x_res[pos])
        y_res_filtered = np.append(y_res_filtered, y_res[pos])
        z_res_filtered = np.append(z_res_filtered, z_res[pos])


z_res_filtered = z_res_filtered[7:]
x_res_filtered = x_res_filtered[7:]

x_res_filtered_x = y_res_filtered_x =  z_res_filtered_x = np.empty(0)

for pos, item in enumerate(x_res_filtered):
    if abs(item) < xmax:
        x_res_filtered_x = np.append(x_res_filtered_x, x_res_filtered[pos])
        y_res_filtered_x = np.append(y_res_filtered_x, y_res_filtered[pos])
        z_res_filtered_x = np.append(z_res_filtered_x, z_res_filtered[pos])



