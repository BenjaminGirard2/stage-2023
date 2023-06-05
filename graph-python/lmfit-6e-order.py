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

def func(x, a, b, c, d, e, f, g):
    return a*x**6 + b*x**5 + c*x**4 + d*x**3 + e*x**2 + f*x +g


p = Parameters()
p.add('a', value=0.2)
p.add('b', value=-10)
p.add('c', value=100)
p.add('d', value=100)
p.add('e', value=100)
p.add('f', value=100)
p.add('g', value=100)

def residual(pars, x, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    e = pars['e']
    f = pars['f']
    g = pars['g']
    model = func(x, a, b, c, d, e, f, g)
    return model - data

out = minimize(residual, p, args=(xdata, ydata))
print(out.last_internal_values)

plt.plot(xdata, ydata)
plt.plot(xdata, ydata+out.residual)
plt.show()
