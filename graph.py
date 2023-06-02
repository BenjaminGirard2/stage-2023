import numpy as np
import matplotlib.pyplot as plt


with open(r'mesures\plaque Al depart.txt') as file:
    data = np.loadtxt(file, delimiter=',')
    print(data[:,0])
    plt.plot(data[:,0], data[:,1])

with open(r'mesures\plaque Al depart.txt') as file:
    data = np.loadtxt(file, delimiter=',')
    print(data[:,0])
    plt.plot(data[:,0], data[:,1])

with open(r'mesures\plaque Al depart.txt') as file:
    data = np.loadtxt(file, delimiter=',')
    print(data[:,0])
    plt.plot(data[:,0], data[:,1])


    plt.show()
    file.close()


