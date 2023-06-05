from lmfit import Parameters, minimize
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit



with open(r'mesures\plaque Al machine.txt') as file:
    data = np.loadtxt(file, delimiter=',')
#    plt.plot(data2[:,0], data2[:,1]-250, 'red', label='Après polissage, sans contraintes')
    file.close()



xdata = data[:,0]
xdata = xdata[8500:45500]

ydata = data[:,1]
ydata = ydata[8500:45500]

def func(x, a, b, c, d):
    return np.sqrt(b**2*(1+(x-c)**2)/a**2)+d


p = Parameters()
p.add('a', value=1)
p.add('b', value=-1)
p.add('c', value=1)
p.add('d', value= 1)

def residual(pars, x, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    model = func(x, a, b, c, d)
    return model - data

out = minimize(residual, p, args=(xdata, ydata))
print(out.last_internal_values)

plt.plot(xdata, ydata)
plt.plot(xdata, ydata+out.residual)
plt.xlabel('Distance en x [mm]')
plt.ylabel('Hauteur [\u03BCm]')
plt.show()
