import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from lmfit import Parameters, minimize
from sympy import symbols
from math import factorial

import time
t0 = time.time()

with open(r'Alienor\FreeformAnalysis.txt') as file:
    data = np.loadtxt(file, delimiter='\t')
    file.close()


bond = 1
longueur = 632

x = data[::bond,0]
y = data[::bond,1]
z = data[::bond,2]

x -= np.mean(x)
y -= np.mean(y)

x = x/np.max(x)
y = y/np.max(y)

xy = np.concatenate(([x], [y]), axis=0)

Zernike_coef = {}

zernike = [5]

for nombre in range(36):
    nombre += 1

    def func(xy, a, h):
        x, y = xy

        N = 1
        n = 0
        m = 0
        while N < nombre:
            if m+2 > n:
                n += 1
                m = -n
                N += 1
            else:
                m += 2
                N += 1

        Z = symbols('Z')
        Z = 0

        m = -m
        M = int( (n - abs(m) )/2)
        p = 0
        if m > 0:
            p = 1

        if n%2 == 0 and m > 0:
            q = abs(m/2)-1
        elif n%2 == 0 and m <= 0:
            q = abs(m)/2
        else:
            q = (abs(m) - 1)/2
        q = int(q)

        for i in range(q+1):

            for j in range(M+1):

                for k in range(M-j+1):

                    xi = int( 2*(i + k) + p )
                    eta = int( n - 2*(i+j+k) - p )

                    if abs(m) < (2*i+p):
                        A = 0
                    else:
                        A = int( factorial(abs(m)) / (factorial(2*i+p) * 
                                                    factorial(abs(m)-2*i - p)))

                    if (M-j) < k:
                        B = 0
                    else:
                        B = int(factorial(M-j) / (factorial(k)*factorial(M-j-k)))

                    C = int( factorial(n-j) / (factorial(j)*
                                            factorial(M-j)*factorial(n-M-j)) )

                    Z += int((-1)**(i+j)) * A * B * C * x**xi * y**eta

        return a*Z - h


    p = Parameters()
    p.add('a', value=1)
    p.add('h', value=1)

    def residual(pars, xy, data):
        a = pars['a']
        h = pars['h']
        model = func(xy, a, h)
        return model - data
    
    try:
        z = out.residual
    except:
        pass
    out = minimize(residual, p, args=(xy, z))

    Zernike_coef[f'{nombre}'] = out.last_internal_values[0]

print(Zernike_coef)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')


surf = ax.plot_trisurf(x[::20], y[::20], out.residual[::20], cmap=cm.jet, linewidth=0)
fig.colorbar(surf)

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))

ax.set_xlabel('x')
ax.set_ylabel('y')
Nombre_de_polynomes_enlevés = len(Zernike_coef)
ax.set_title(f'Nombre de polynomes enlevés: {Nombre_de_polynomes_enlevés}')
fig.tight_layout()

t1 = time.time()
print("Temps d'exécution:", t1-t0)

plt.show()

#test = list(Zernike_coef.values())


#plt.plot(test[7:])
#plt.show()