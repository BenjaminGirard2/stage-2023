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
bond = 1

res = np.empty(0)


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

np.savetxt('Erreur.txt', out.residual)


    #RMS = np.sqrt(np.sum(np.square(out.residual)))/len(out.residual)

    #res = np.append(res, RMS)

