from lmfit import Parameters, minimize
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


with open(r'mesures\plaque Al depart.txt') as file:
    data0 = np.loadtxt(file, delimiter=',')
#    plt.plot(data0[:,0], data0[:,1], 'k', label='|Avant polissage, sous contraintes')
    file.close()

with open(r'mesures\plaque Al machine monte.txt') as file:
    data1 = np.loadtxt(file, delimiter=',')
#    plt.plot(data1[:,0], data1[:,1]-74, 'blue', label='Après polissage, sous contraintes')
    file.close()

with open(r'mesures\plaque Al machine.txt') as file:
    data2 = np.loadtxt(file, delimiter=',')
#    plt.plot(data2[:,0], data2[:,1]-250, 'red', label='Après polissage, sans contraintes')
    file.close()



xdata = data0[:,0]
xdata = xdata[:]

ydata = data0[:,1]
ydata = ydata[:]

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

plt.plot(xdata, ydata, label='before')
#plt.plot(xdata, ydata+out.residual, label='before-fit')


xdata = data2[:,0]
xdata = xdata[:]

ydata = data2[:,1]
ydata = ydata[:]



p = Parameters()
p.add('a', value=0.2)
p.add('b', value=-10)
p.add('c', value=100)


#out = minimize(residual, p, args=(xdata, ydata))


plt.plot(xdata, -ydata, label='after')
#plt.plot(xdata, ydata+out.residual, label='after-fit')
plt.xlabel('Distance en x [mm]')
plt.ylabel('Hauteur [\u03BCm]')
plt.legend()
plt.show()