from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

t = np.linspace(0, 2 * np.pi, 400)

# x = 5 * np.cos(t)
# y = 2 * np.sin(t)
# z = t

x = np.sin(3 * t) * np.cos(5 * t)
y = np.sin(3 * t) * np.sin(5 * t)
z = np.cos(3 * t)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')


def update(num):
    # Changing elevation and azimuth view angles
    ax.view_init(elev=10 + 90 * np.sin(0.5 * np.deg2rad(num)), azim=num * 0.5)
    points.set_data([x[num], y[num]])
    points.set_3d_properties(z[num])


N = t.shape[0]
ax.plot(x, y, z)
points, = ax.plot([0], [0], [0], marker='o', ls="")

# Setting the axes properties
ax.set_xlim3d([1.05 * np.min(x), 1.05 * np.max(x)])
ax.set_xlabel('X')

ax.set_ylim3d([1.05 * np.min(y), 1.05 * np.max(y)])
ax.set_ylabel('Y')

ax.set_zlim3d([1.1 * np.min(z), 1.1 * np.max(z)])
ax.set_zlabel('Z')

ani = animation.FuncAnimation(fig, update, N, interval=(10000 / N), blit=False)
# f = "parametric_curve_animation.mp4"
# write_mp4 = animation.FFMpegWriter(fps=25)
# ani.save(f, writer=write_mp4)
plt.show()
