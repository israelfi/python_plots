import numpy as np
import matplotlib.pyplot as plt


def configure_axis(axis, grid=True):
    ax.set_facecolor('#36454f')

    axis.tick_params(axis='x', colors='white')
    axis.tick_params(axis='y', colors='white')

    axis.spines['bottom'].set_color('white')
    axis.spines['left'].set_color('white')

    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)

    axis.xaxis.label.set_color('white')
    axis.yaxis.label.set_color('white')
    ax.title.set_color('white')

    if grid:
        ax.grid(visible=True, which='major', color='white', linestyle='-', alpha=0.2)
        ax.minorticks_on()
        ax.grid(visible=True, which='minor', color='white', linestyle='-', alpha=0.1)


x = np.linspace(0, 5)
y = np.tanh(x)

fig = plt.figure(facecolor='#36454f', figsize=(9, 6))
ax = fig.add_subplot()

ax.plot(x, y, linewidth=2.5)

ax.set_title('Plot Title')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')

configure_axis(ax)

plt.show()
