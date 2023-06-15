from lmfit import Parameters, minimize



order = 9



def polynomial_func(*args):

    if isinstance(args[0], list):
        args = args[0]

    x = args[0]
    result = 0

    for pos, value in enumerate(args[1:]):
        result += value*x**pos

    return result



p2 = Parameters()
for i in range(order+1):
    p2.add(chr(97+i), value=1)



def residual2(pars, x, data):
    params_list = []
    for i in range(order+1):
        params_list.append(pars[chr(97+i)])

    model = polynomial_func(x, params_list)
    return model - data

for i in range(256):

    print(chr(i))