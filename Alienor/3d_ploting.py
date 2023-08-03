import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from lmfit import Parameters, minimize



# Met le chemin pour accéder au fichier là
#                   ↓↓↓
with open(r'Alienor\FreeformAnalysis.txt') as file:
    data = np.loadtxt(file, delimiter='\t')
    file.close()

# Tu peux augmenter le bond pour que ça bug moins
bond = 20

x = data[::bond,0]
y = data[::bond,1]
z = data[::bond,2]

xy = np.concatenate(([x], [y]), axis=0)


def func(xy, a, b, c, d):
    x, y = xy
    return -a + (x - b)**2/(4*d) + (y - c)**2/(4*d)

p = Parameters()
p.add('a', value=5)
p.add('b', value=1)
p.add('c', value=1)
p.add('d', value=1)

def residual(pars, xy, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    model = func(xy, a, b, c, d)
    return model - data




out = minimize(residual, p, args=(xy, z))

#print(out.last_internal_values)


#moy = (np.mean(out.residual))

#RMS = np.sqrt(np.sum(np.square(np.absolute(z))))/len(z)
#print('RMS =', RMS)

#PV = max(z)-min(z)
#print('PV =', PV)

def func2(xy, a, b, c, d):
    x, y = xy
    return -a + (x - b)**2/(d) - (y - c)**2/(d)

p2 = Parameters()
p2.add('a', value=0.001)
p2.add('b', value=100)
p2.add('c', value=100)
p2.add('d', value=10000)

def residual2(pars, xy, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    model = func2(xy, a, b, c, d)
    return model - data


out2 = minimize(residual2, p2, args=(xy, out.residual))



def func3(xy, a, b, c, d):
    x, y = xy
    x = x - b
    y = y - c
    return -a + (-np.power(y, 3) + 3*y*np.square(x))/d

p3 = Parameters()
p3.add('a', value=0.001)
p3.add('b', value=100)
p3.add('c', value=100)
p3.add('d', value=10000)

def residual3(pars, xy, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    model = func3(xy, a, b, c, d)
    return model - data


out3 = minimize(residual3, p3, args=(xy, out2.residual))


def func4(xy, a, b, c, d):
    x, y = xy
    x = x - b
    y = y - c
    return -a + (np.power(x, 3) - 3*x*np.square(y))/d

p4 = Parameters()
p4.add('a', value=0.001)
p4.add('b', value=100)
p4.add('c', value=100)
p4.add('d', value=10000)

def residual4(pars, xy, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    model = func4(xy, a, b, c, d)
    return model - data


out4 = minimize(residual4, p4, args=(xy, out3.residual))















fig = plt.figure()
ax = fig.add_subplot(projection='3d')

#surf = ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0)
surf = ax.plot_trisurf(x, y, out4.residual, cmap=cm.jet, linewidth=0)
fig.colorbar(surf)

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))

ax.set_xlabel('[mm]')
ax.set_ylabel('[mm]')

fig.tight_layout()

plt.show()

