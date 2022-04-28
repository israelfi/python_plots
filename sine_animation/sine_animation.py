import numpy as np
from math import atan2
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

t = np.linspace(0, 4 * np.pi, 200)
amplitude = 2
y = amplitude * np.sin(t)
angles = np.zeros(t.shape[0])

for k in range(1, t.shape[0]):
    angles[k] = atan2(y[k] - y[k - 1], t[k] - t[k - 1])

rect_width = 0.4
rect_height = 0.2


def my_function(i):
    ax.cla()
    ax2.cla()
    ax.grid()
    ax2.grid()

    ax.plot(t[:i], y[:i])
    rectangle_update = patches.Rectangle(xy=(t[i - 1] + (rect_height / 2 * np.sin(angles[i - 1])),
                                             y[i - 1] - rect_height / 2 * np.cos(angles[i - 1])),
                                         width=rect_width, height=rect_height, angle=np.rad2deg(angles[i - 1]),
                                         color='green')

    ax.set_title('Sine Wave')
    ax.add_patch(rectangle_update)
    ax.set_xlim([t[0], t[-1]])
    ax.set_ylim([1.1 * min(y), 1.1 * max(y)])
    ax.set_aspect('equal', adjustable='box')

    ax2.set_title('Rectangle Angle (rad)')
    ax2.plot(t[:i], angles[:i], c='orange', linewidth=2)
    ax2.set_xlim([t[0], t[-1]])
    ax2.set_ylim([1.1 * min(angles), 1.1 * max(angles)])
    ax2.set_aspect('equal', adjustable='box')

    plt.tight_layout()


fig = plt.figure(figsize=(8, 6), facecolor='#DEDEDE')
ax = fig.add_subplot(211)
plt.grid()
ax2 = fig.add_subplot(212)
plt.grid()

rectangle = patches.Rectangle(xy=(0, 0), width=0.2, height=0.1, angle=np.rad2deg(angles[0]))
ax.add_patch(rectangle)

ax.set_title('Sine Wave')
ax.set_xlim([t[0], t[-1]])
ax.set_ylim([1.1 * min(y), 1.1 * max(y)])
ax.set_aspect('equal', adjustable='box')

ax2.set_title('Rectangle Angle (rad)')
ax2.set_xlim([t[0], t[-1]])
ax2.set_ylim([1.1 * min(angles), 1.1 * max(angles)])
ax2.set_aspect('equal', adjustable='box')

plt.tight_layout()

ani = FuncAnimation(fig, my_function, interval=50, frames=t.shape[0])
ani.save('matplot003.gif', writer='imagemagick')
plt.show()
