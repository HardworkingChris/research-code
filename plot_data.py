from sys import argv
import pickle
import matplotlib.pyplot as plt


filename = argv[1]

(s,j,m) = pickle.load(open(filename,'r'))
plt.contourf(s,j,m)
plt.show()
