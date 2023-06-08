import meshio
import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters, minimize

mesh = meshio.read(r'results\true_size.vtk')
u = mesh.point_data['u']
ux = u[:,0]
uy = u[:,1]
uz = u[:,2]
x = mesh.points[:,0]
y = mesh.points[:,1]
z = mesh.points[:,2]


xf = xff = uf = uff = zf = yf = ui = uii = x_final = z_final = np.empty(0)
for count, coord in enumerate(z):
    if coord > 0.3:
        uf = np.append(uf, uz[count])
        ui = np.append(ui, ux[count])
        xf = np.append(xf, x[count])
        yf = np.append(yf, y[count])
        zf = np.append(zf, z[count])


ymax = 0.2
xmax = 0.7

for count, item in enumerate(yf):
    if abs(item) < ymax:
        uff = np.append(uff, uf[count])
        xff = np.append(xff, xf[count])
        uii = np.append(uii, ui[count])

for count, item in enumerate(uii+xff):
    if abs(item) < xmax:
        x_final = np.append(x_final, item)
        z_final = np.append(z_final, uff[count])



xdata = x_final[1:]

ydata = z_final[1:]

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
#print(out.last_internal_values)

plt.scatter(xdata, ydata)
plt.scatter(xdata, ydata+out.residual)
plt.xlabel('Distance en x [mm]')
plt.ylabel('Hauteur [\u03BCm]')
plt.show()