import numpy as np
from sympy import symbols



x = symbols('x')
y = symbols('y')
y = 0

for i in range(10):
    if i%2 == 0:

        print(i, 'paire')
    else:
        print(i, 'impaire')

