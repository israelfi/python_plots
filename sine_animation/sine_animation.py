import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt

t = np.linspace(0, 2 * np.pi, 100)
x = 5 * np.cos(t)
y = 2 * np.sin(t)
z = t


def my_function(i):
    ax.cla()
    plt.grid()
    ax.set_xlim([0, t[-1]])
    ax.set_ylim([np.min(y) - 0.1, np.max(y) + 0.1])
    ax.plot(t[:i], y[:i])


fig = plt.figure(figsize=(12, 6), facecolor='#DEDEDE')
ax = plt.subplot()
plt.grid()
ax.set_xlim([0, t[-1]])
ax.set_ylim([np.min(y) - 0.1, np.max(y) + 0.1])

ani = FuncAnimation(fig, my_function, interval=200)
# ani.save('matplot003.gif', writer='imagemagick')
plt.show()
