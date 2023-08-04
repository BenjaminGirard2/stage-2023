import numpy as np
from sympy import symbols
from math import factorial


def Zernike_function(n, m):
    print("n =", n, '\t', "m =", m)

    if abs(m) > n:
        raise ValueError


    x, y = symbols('x y')
    Z = symbols('Z')
    Z = 0
    
    

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

    #overrite:   ---------------------------------------------------------
    #M = 0
    #p = 0
    #q = 1
    #overrite:   ---------------------------------------------------------

    print('M =', M)
    print('p =', p)
    print('q =', q,'\n')

    for i in range(q+1):
        print('i', i)

        for j in range(M+1):
            print('j', j)

            for k in range(M-j+1):
                print('k', k, '\n')

                xi = int( n - 2*(i+j+k) - p )
                eta = int( 2*(i + k) + p )
                print('xi', xi)
                print('eta', eta, '\n')

                if abs(m) < (2*i+p):
                    A = 0
                else:
                    A = int( factorial(abs(m)) / (factorial(2*i+p) * factorial(abs(m) - 2*i - p)) )
                print('A', A)

                if (M-j) < k:
                    B = 0
                else:
                    B = int(factorial(M-j) / (factorial(k)*factorial(M - j - k)))
                print('B', B)

                C = int( factorial(n-j) / (factorial(j)*factorial(M-j)*factorial(n-M-j)) )
                print('C', C)

                test = int((-1)**(i+j)) * A * B * C * x**xi * y**eta
                print('result:', test, '\n')

                Z += int((-1)**(i+j)) * A * B * C * x**xi * y**eta

    print('Z =', Z, '\n')


Zernike_function(2, 2)
