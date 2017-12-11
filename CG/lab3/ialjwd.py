import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.subplots_adjust(left=0.25, bottom=0.25)
"""
x = np.arange(0.0, 1.0, 0.1)
a0 = 5
b0 = 1
y = a0 * x + b0
z = np.zeros(10)
"""
a0 = 5
b0 = 1

f, a, b, c = 3, 1, 1, 1

t = np.linspace(0, np.pi, f)
g = np.linspace(0, 2*np.pi, f)

th, ph = np.meshgrid(t, g)
r = 0.2
X, Y, Z = a*np.sin(th)*np.cos(ph),b*np.sin(th)*np.sin(ph),c*np.cos(th)

l, = plt.plot(X, Y, Z)

# Set size of Axes
plt.axis([0, 1, -10, 10])

# Place Sliders on Graph
ax_a = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_b = plt.axes([0.25, 0.15, 0.65, 0.03])

# Create Sliders & Determine Range
sa = Slider(ax_a, 'a', 0, 10.0, valinit=a0)
sb = Slider(ax_b, 'b', 0, 10.0, valinit=b0)


def update(val):
    a = sa.val
    b = sb.val
    l.set_data(f, a * f + b)
    l.set_3d_properties(Z)
    fig.canvas.draw_idle()

sa.on_changed(update)
sb.on_changed(update)

plt.show()