from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np

print('Enter parameter a:')
a = int(input())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', facecolor='grey')

#Вершины клина
v = np.array([[a, a, a], [-a, a, a], [-a, -a, a], [a, -a, a], [0, 0, -3*a]])
ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

#Генерация граней клина
gr = [ [v[0],v[1],v[4]], [v[0],v[3],v[4]], [v[2],v[1],v[4]], [v[2],v[3],v[4]], [v[0],v[1],v[2],v[3]]]

#Добавление на график клина
ax.add_collection3d(Poly3DCollection(gr, facecolors='red', linewidths=1, edgecolors='blue', alpha=.25))

plt.show()