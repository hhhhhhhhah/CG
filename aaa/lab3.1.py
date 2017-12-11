from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

s = 1
while s == 1:
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    a = int(input("Enter accuracy of sphere: "))
    b = int(input("Enter lighting level: "))
    r = 1
    # Углы фи и тета, по которым строятся части сферы
    phi = np.linspace(0, 360, a) / 180.0 * np.pi
    theta = np.linspace(-90, 90, a) / 180.0 * np.pi

    # Вычисление цветов
    vars = []
    for i in range(len(phi) - 1):
        for j in range(len(theta) - 1):
            v = (j + 1) * b / 2 / a
            if v > 1:
                v = 1
            vars.append(v)

    # Присвоение граням цветов
    cols = []
    for var in vars:
        col = (var, var, var)
        cols.append(col)

    verts2 = []
    for i in range(len(phi) - 1):
        for j in range(len(theta) - 1):
            cp0 = r * np.cos(phi[i])
            cp1 = r * np.cos(phi[i + 1])
            sp0 = r * np.sin(phi[i])
            sp1 = r * np.sin(phi[i + 1])

            ct0 = np.cos(theta[j])
            ct1 = np.cos(theta[j + 1])
            st0 = r * np.sin(theta[j])
            st1 = r * np.sin(theta[j + 1])

            verts = []
            verts.append((cp0 * ct0, sp0 * ct0, st0))
            verts.append((cp1 * ct0, sp1 * ct0, st0))
            verts.append((cp1 * ct1, sp1 * ct1, st1))
            verts.append((cp0 * ct1, sp0 * ct1, st1))
            verts2.append(verts)

    ax.add_collection3d(Poly3DCollection(verts2, facecolor=cols, linewidths=1, edgecolors='blue', alpha=.9))
    ax.set_xlabel('X')
    ax.set_xlim3d(-1, 1)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-1, 1)
    ax.set_zlabel('Z')
    ax.set_zlim3d(-1, 1)

    plt.show()
    s = int(input("Change parameters? Press 1 to change and something else to exit: "))