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
p.add('b', value=240)
p.add('c', value=100)
p.add('d', value=1000)

def residual(pars, xy, data):
    a = pars['a']
    b = pars['b']
    c = pars['c']
    d = pars['d']
    model = func(xy, a, b, c, d)
    return model - data




out = minimize(residual, p, args=(xy, z))

print(out.last_internal_values)


moy = (np.mean(out.residual))

RMS = np.sqrt(np.sum(np.square(np.absolute(z))))/len(z)
print('RMS =', RMS)

PV = max(z)-min(z)
print('PV =', PV)




fig = plt.figure()
ax = fig.add_subplot(projection='3d')

#surf = ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0)
surf = ax.plot_trisurf(x, y, out.residual, cmap=cm.jet, linewidth=0)
fig.colorbar(surf)

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))

ax.set_xlabel('[mm]')
ax.set_ylabel('[mm]')

fig.tight_layout()

plt.show()

