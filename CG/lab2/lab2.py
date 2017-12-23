from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np

a = 1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.axis('off')
# Вершины клина
v = np.array([[a, a, 0], [-a, a, 0], [-a, -a, 0], [a, -a, 0], [0, 0, -2*a/np.sqrt(2)], [0, 0, 2*a/np.sqrt(2)]])
ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

# Генерация граней клина
gr = [[v[0], v[1], v[4]], [v[0], v[3], v[4]], [v[2], v[1], v[4]], [v[2], v[3], v[4]], [v[0], v[1], v[5]], [v[0], v[3], v[5]],\
      [v[2], v[1], v[5]], [v[2], v[3], v[5]]]

face_color = [0.5, 0.5, 1]
# Добавление на график клина
ax.add_collection3d(Poly3DCollection(gr, facecolors=face_color, linewidths=1, edgecolors='red', alpha=0.1))

plt.show()
