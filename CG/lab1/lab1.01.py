import numpy as np
import matplotlib.pyplot as plt


a = int(input("Please enter a: "))

theta = np.arange(0, 2*np.pi, 0.01)
r = np.sqrt(2 * a**2 * np.cos(theta))

ax = plt.subplot(111, projection='polar')

ax.plot(theta, r)

plt.show()
