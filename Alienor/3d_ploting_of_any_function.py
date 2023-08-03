import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from lmfit import Parameters, minimize



x = np.linspace(-5,5,50)
y = np.linspace(-5,5,50)
x2 = np.append(0,x.flatten())
y2 = np.append(0,y.flatten())

x2, y2 = np.meshgrid(x2, y2)

a = 0
b = 0
c = 0
d = 20
x = x2
y = y2
z = -a + (np.power(x, 3) - 3*x*np.square(y))/d

fig = plt.figure()
ax = fig.add_subplot(projection='3d')


surf = ax.plot_trisurf(x2.flatten(), y2.flatten(), z.flatten(), cmap=cm.jet, linewidth=0)
fig.colorbar(surf)

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))
ax.set_xlabel('x')
ax.set_ylabel('y')

fig.tight_layout()

plt.show()

