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



xdata = data2[:,0]
xdata = xdata[23500:29700]

ydata = data2[:,1]
ydata = ydata[23500:29700]/1000

def func(x, a, b, c):
    return -np.sqrt(a-(x-b)**2) + c


p = Parameters()
p.add('a', value=30000)
p.add('b', value=27.5)
p.add('c', value=163)

def residual(pars, x, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    model = func(x, a, b, c)
    return model - data

out = minimize(residual, p, args=(xdata, ydata))
print(out.last_internal_values)

plt.plot(xdata, ydata*1000000)
plt.plot(xdata, (ydata+out.residual)*1000000)
plt.xlabel('Distance en x [mm]')
plt.ylabel('Hauteur [nm]')
plt.show()

