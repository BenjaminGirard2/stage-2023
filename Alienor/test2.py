import numpy as np
from sympy import symbols, Function, lambdify



x = symbols('x')
y = symbols('y')

h = symbols('h')


Z = 2*x**2+y

test = np.linspace(-10,10,100)
t2 = 2*np.ones(100)


Zuk = lambdify(x, Z)
Zuk = Zuk(test)

Tuk = lambdify(y, Zuk)

print(Tuk.subs(y, 2))



