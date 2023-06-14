from turning import x_res_filtered_x, z_res_filtered_x
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Parameters, minimize


with open(r'mesures\plaque Al machine.txt') as file:
    data = np.loadtxt(file, delimiter=',')
#    plt.plot(data2[:,0], data2[:,1]-250, 'red', label='Après polissage, sans contraintes')
    file.close()



xdata = data[:,0]
xdata = xdata[23500:29700]-26.53

ydata = data[:,1]
ydata = ydata[23500:29700]/1000+0.123

def func(x, a, b, c):
    return a*x**2 + b*x + c


p = Parameters()
p.add('a', value=0.2)
p.add('b', value=-10)
p.add('c', value=100)

def residual(pars, x, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    model = func(x, a, b, c)
    return model - data

out = minimize(residual, p, args=(xdata, ydata))

out2 = minimize(residual, p, args=(x_res_filtered_x*5, z_res_filtered_x-0.293))


plt.plot(xdata, ydata, 'r')
#plt.plot(xdata, ydata+out.residual, 'green')
plt.xlabel('Distance en x [mm]')
plt.ylabel('Hauteur [\u03BCm]')
plt.scatter(x_res_filtered_x*5, z_res_filtered_x-0.293)
#plt.scatter(x_res_filtered_x*5, z_res_filtered_x-0.293+out2.residual)
plt.show()










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



