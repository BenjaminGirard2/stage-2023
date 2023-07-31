import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from lmfit import Parameters, minimize


with open(r'Alienor\FreeformAnalysis.txt') as file:
    data = np.loadtxt(file, delimiter='\t')
    file.close()

cut = 20

x = data[::cut,0]
y = data[::cut,1]
z = data[::cut,2]

xy = np.concatenate(([x], [y]), axis=0)


def func(xy, a, b, c, d, e):
    #print(len(xy))
    x, y = xy
    return a + (x/b + c)**2 + (y/d + e)**2

p = Parameters()
p.add('a', value=-5.28)
p.add('b', value=63.93)
p.add('c', value=-3.86)
p.add('d', value=60.15)
p.add('e', value=-1.61)

def residual(pars, xy, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    e = pars['e']
    model = func(xy, a, b, c, d, e)
    return model - data

out = minimize(residual, p, args=(xy, z))
#print(out.last_internal_values)



fig = plt.figure()
ax = fig.add_subplot(projection='3d')

surf = ax.plot_trisurf(x, y, out.residual, cmap=cm.jet, linewidth=0)
fig.colorbar(surf)

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))

fig.tight_layout()

plt.show()

