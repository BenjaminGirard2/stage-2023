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

#plt.xlabel('Distance en x [\u03BCm]')
#plt.ylabel('Hauteur [\u03BCm]')
#plt.legend()
#plt.show()


xdata = data2[:,0]
xdata = xdata[8500:45500]

ydata = data2[:,1]
ydata = ydata[8500:45500]

def func(x, a, b, c):
    return a*x**2 + b*x + c


plt.plot(xdata, ydata)
p0 = np.array([0.2, -10, -100])
model = func(xdata, *p0)
plt.plot(xdata, model)
plt.show()

popt, pcov = curve_fit(f=func, xdata=xdata, ydata=ydata, p0=p0)

plt.plot(xdata, ydata)
model = func(xdata, *popt)
plt.plot(xdata, model)
plt.show()