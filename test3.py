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