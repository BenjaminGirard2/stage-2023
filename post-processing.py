import meshio
import matplotlib.pyplot as plt

mesh = meshio.read(r'results\true_size.vtk')
u = mesh.point_data['u']
x = mesh.points[:,0]
y = mesh.points[:,1]
z = mesh.points[:,2]

plt.scatter(x, u[:,2])



from lmfit import Parameters, minimize
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



with open(r'mesures\plaque Al machine.txt') as file:
    data = np.loadtxt(file, delimiter=',')
#    plt.plot(data2[:,0], data2[:,1]-250, 'red', label='Après polissage, sans contraintes')
    file.close()



xdata = data[:,0]
xdata = xdata[23500:29700]

ydata = data[:,1]
ydata = ydata[23500:29700]/1000

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

#out = minimize(residual, p, args=(xdata, ydata))
#print(out.last_internal_values)

plt.plot((xdata-26.6)/1.5, (-ydata*4.5-0.350), 'red')
#plt.plot(xdata, ydata+out.residual)
plt.xlabel('Distance en x [cm]')
plt.ylabel('Hauteur [\u03BCm]')
plt.show()
