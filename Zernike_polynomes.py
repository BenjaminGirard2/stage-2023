from sympy import symbols
from math import factorial


def Zernike_function(*args):

    """Create the zernike polynomial. If one argument is givent: return the N
    zernike polynome. If two argument is given, return the polynome of that 
    exacte order."""

    if len(args) == 1:
        N = 1
        n = 0
        m = 0
        while N < args[0]:
            if m+2 > n:
                n += 1
                m = -n
                N += 1
            else:
                m += 2
                N += 1

    if len(args) == 2:
        n = args[0]
        m = args[1]


    if abs(m) > n:
        raise ValueError("absolut of m is bigger than n")

    x, y = symbols('x y')
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

    return Z