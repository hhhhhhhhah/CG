from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

s = 1
while s == 1:
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    a=int(input("Enter accuracy of sphere: "))
    b=int(input("Enter lighting level: "))
    r=1
    #Углы фи и тета, по которым строятся части сферы
    phi = np.linspace(0,360,a)/180.0*np.pi

    r1 = int(input("Radius: "))
    r2 = int(input("Top radius: "))
    h = int(input("Height: "))

    #Вычисление цветов
    vars1=[]
    if (a % 2 == 0):
        v_range = int(len(phi) / 2)
    else:
        v_range = int((len(phi)-1) / 2)

    for i in range(v_range):
        #for j in range(len(theta)-1):
        v=(i+1)*b/2/a
        if v>1:
            v=1
        vars1.append(v)
    v_length = len(phi) - 1


    for i in range(int(v_length / 2), 0, -1):
        vars1.append(vars1[i-1])

    #Присвоение граням цветов
    cols=[]
    for var in vars1:
        col=(var, var, var)
        cols.append(col)
    cols.append((1, 1 ,1))
    cols.append((1, 1 ,1))

    verts2 = []
    bcircle = []
    tcircle = []
    for i in range(len(phi)-1):
            xb0= r1*np.cos(phi[i])
            xb1= r1*np.cos(phi[i+1])
            yb0= r1*np.sin(phi[i])
            yb1= r1*np.sin(phi[i+1])

            xt0= r2*np.cos(phi[i])
            xt1= r2*np.cos(phi[i+1])
            yt0= r2*np.sin(phi[i])
            yt1= r2*np.sin(phi[i+1])

            bcircle.append((xb0, yb0, 0))
            tcircle.append((xt0, yt0, h))

            verts=[]
            verts.append((xb0, yb0, 0))
            verts.append((xb1, yb1, 0))
            verts.append((xt1, yt1, h))
            verts.append((xt0, yt0, h))
            verts2.append(verts)

    verts2.append(bcircle)
    verts2.append(tcircle)
    ax.add_collection3d(Poly3DCollection(verts2 ,facecolor=cols, linewidths=1, edgecolors='blue', alpha=.9))
    ax.set_xlabel('X')
    ax.set_xlim3d(-10, 10)
    ax.set_ylabel('Y')
    ax.set_ylim3d(-10, 10)
    ax.set_zlabel('Z')
    ax.set_zlim3d(-10, 10)

    plt.show()
    s=int(input("Change parameters? Press 1 to change and something else to exit: "))