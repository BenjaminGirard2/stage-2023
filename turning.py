import meshio
import numpy as np
import matplotlib.pyplot as plt

mesh = meshio.read(r'vtk-files\centr_true_size_4-3.vtk')
u_field = mesh.point_data['u']
x = mesh.points[:,0]
y = mesh.points[:,1]
z = mesh.points[:,2]

ymax = 0.07
h = 0.4



def under_function(uz):
    if uz > h:
        return True
    else:
        return False


x_res = y_res = z_res = x_res_filtered = y_res_filtered = z_res_filtered = np.empty(0)




for pos, u in enumerate(u_field):
    k = z[pos]+u[2]-h

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

plt.scatter(x_res_filtered, z_res_filtered)
plt.show()

plt.scatter(x, u_field[:,2])
plt.show()



