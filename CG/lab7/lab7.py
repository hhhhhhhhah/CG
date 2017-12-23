import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

print("Enter points: ")
ax = float(input("First point x: "))
ay = float(input("y: "))
bx = float(input("Second point x: "))
by = float(input("y: "))

angle1 = float(input("Enter angle of rotation for first tangent: "))
angle2 = float(input("Enter angle of rotation for second tangent: "))
angle1 = angle1/57
angle2 = angle2/57

tangent11_x = 0.3 * np.cos(angle1) + ax
tangent11_y = 0.3 * np.sin(angle1) + ay
tangent12_x = 0.3 * np.cos(angle1+180/57) + ax
tangent12_y = 0.3 * np.sin(angle1+180/57) + ay
tangent21_x = 0.3 * np.cos(angle2) + bx
tangent21_y = 0.3 * np.sin(angle2) + by
tangent22_x = 0.3 * np.cos(angle2+180/57) + bx
tangent22_y = 0.3 * np.sin(angle2+180/57) + by

a0x = (ax + 0.01 * tangent12_x) / (1 + 0.01)
a0y = (ay + 0.01 * tangent12_y) / (1 + 0.01)
points = [(a0x, a0y), (ax, ay), (bx, by)]

b0x = (bx + 0.01 * tangent22_x) / (1 + 0.01)
b0y = (by + 0.01 * tangent22_y) / (1 + 0.01)
points = points + [(b0x, b0y)]

data = np.array(points)

tck, u = interpolate.splprep(data.transpose(), s=0)
unew = np.arange(0, 1, 0.01)
out = interpolate.splev(unew, tck)

plt.figure()
plt.plot([tangent11_x, tangent12_x], [tangent11_y, tangent12_y], 'green')
plt.plot([tangent21_x, tangent22_x], [tangent21_y, tangent22_y], 'green')

for i in (1, 2, 3):
    plt.plot(out[0], out[1], color='orange')
    plt.plot(data[i, 0], data[i, 1], 'ob')
plt.show()
