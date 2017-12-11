from numba import cuda
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.pyplot import (axes,axis,title,legend,figure,
                               xlabel,ylabel,xticks,yticks,
                               xscale,yscale,text,grid,
                               plot,scatter,errorbar,hist,polar,
                               contour,contourf,colorbar,clabel,
                               imshow)
from mpl_toolkits.mplot3d import Axes3D
from numpy import (linspace,logspace,zeros,ones,outer,meshgrid,
                   pi,sin,cos,sqrt,exp)
from matplotlib.colors import LightSource
from matplotlib.cbook import get_sample_data


"""print('точность апроксимаций:')
f = int(input())
print('параметры элипса:')
a = int(input())
b = int(input())
c = int(input())
"""
print('яркость освещения 0-5')
m = int(input())

f,a,b,c = 20, 1, 2, 3

D = max(a,b,c)




fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.


t=np.linspace(0,pi,f)
g=np.linspace(0,2*pi,f)

th,ph=meshgrid(t,g)
r=0.2
X,Y,Z=a*sin(th)*cos(ph),b*sin(th)*sin(ph),c*cos(th)

#plt.axis('off')

# Plot the surface.

if m == 4:
    ls = LightSource(170,90 )
    rgb= ls.shade(Z, cmap=cm.gist_gray, vert_exag=(0), blend_mode='soft')
    surf = ax.plot_surface(X, Y, -Z , rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=True, shade=True)
elif m ==5:
        surf = ax.plot_surface(X, Y, Z , rstride=1, cstride=1, color='w',
                       linewidth=0, antialiased=False, shade=False)
elif m == 3:
    ls = LightSource(123, 90)
    rgb= ls.shade(Z, cmap=cm.binary, vert_exag=(0.1), blend_mode='soft')
    surf = ax.plot_surface(X, Y, Z , rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)
elif m == 2:
    ls = LightSource(250, 300)
    rgb= ls.shade(Z, cmap=cm.binary, vert_exag=(0.1), blend_mode='soft')
    surf = ax.plot_surface(X, Y, Z , rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)
elif m == 1:
    ls = LightSource(90, 190)
    rgb= ls.shade(Z, cmap=cm.binary, vert_exag=(0.1), blend_mode='soft')
    surf = ax.plot_surface(X, Y, Z , rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=True)
elif m ==0:
        surf = ax.plot_surface(X, Y, Z , rstride=1, cstride=1, color='k',
                       linewidth=0, antialiased=False, shade=False)

# Customize the z axis.

ax.set_zlim(-(D+1), (D+1))
ax.set_xlim(-(D+1), (D+1))
ax.set_ylim(-(D+1), (D+1))



plt.show()





