
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Grab some test data.
X, Y, Z = axes3d.get_test_data(0.5)

# Plot a basic wireframe.
ax.plot_wireframe(X, Y, Z, rstride=100, cstride=10)

plt.show()
