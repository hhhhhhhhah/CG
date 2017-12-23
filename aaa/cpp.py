import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri

file = open("data.txt", "r")
line = file.readline()
P00 = line.split(",")
P00 = [float(i) for i in P00]

line = file.readline()
P01 = line.split(",")
P01 = [float(i) for i in P01]

line = file.readline()
P10 = line.split(",")
P10 = [float(i) for i in P10]

line = file.readline()
P11 = line.split(",")
P11 = [float(i) for i in P11]

minu = maxw = P00[0]

for p in [P00, P01, P10, P11]:
    for i in p:
        maxw = max(maxw, i)
        minu = min(minu, i)


u = np.linspace(minu, maxw, 10)
w = np.linspace(minu, maxw, 10)
u, w = np.meshgrid(u, w)
u, w = u.flatten(), w.flatten()
tri = mtri.Triangulation(u, w)
"""
surfpts_x = []
surfpts_y = []
surfpts_z = []

for i in u:
    for j in w:
        x = P00[0] * (1-i) * (1-j) + P01[0] * (1-i) * j + P10[0] * i * (1-j) + P11[0] * i * j
        y = P00[1] * (1 - i) * (1 - j) + P01[1] * (1 - i) * j + P10[1] * i * (1 - j) + P11[1] * i * j
        z = P00[2] * (1 - i) * (1 - j) + P01[2] * (1 - i) * j + P10[2] * i * (1 - j) + P11[2] * i * j

        surfpts_x.append(x)
        surfpts_y.append(y)
        surfpts_z.append(z)
"""

x = P00[0] * (1 - u) * (1 - w) + P01[0] * (1 - u) * w + P10[0] * u * (1 - w) + P11[0] * u * w
y = P00[1] * (1 - u) * (1 - w) + P01[1] * (1 - u) * w + P10[1] * u * (1 - w) + P11[1] * u * w
z = P00[2] * (1 - u) * (1 - w) + P01[2] * (1 - u) * w + P10[2] * w * (1 - w) + P11[2] * u * w

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(surfpts_x, surfpts_y, surfpts_z, cmap='viridis') # Точечный вывод
ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap='viridis')

plt.show()
