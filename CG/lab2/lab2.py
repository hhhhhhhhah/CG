from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import numpy as np
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource

#a = int(input("Please enter a: "))
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

ls = LightSource(270, 45)
#rgb = ls.shade(ax ,cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')

face_color = [0.5, 0.5, 1]
collection = Poly3DCollection(gr, edgecolors='red', linewidths=1, facecolors='white', alpha=1, shade=True, antialiaseds=True)#, face_color=rgb)
#collection.set_facecolor(face_color)
# Добавление на график клина
ax.add_collection3d(collection)
#ax.add_collection3d(Poly3DCollection(gr, facecolors=face_color, linewidths=1, edgecolors='red', alpha=0.1))

plt.show()
